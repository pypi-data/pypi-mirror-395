"""
Video-related operations for the NomadicML SDK.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
import time
import logging
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional, Union, Mapping
from urllib.parse import urlparse
import random
from .client import NomadicML
from .types import (
    VideoSource,
    RapidReviewEvent,
    UIEvent,
    OverlayFieldPair,
    StructuredOddColumn,
    StructuredOddResult,
)
from .utils import (
    format_error_message, infer_source,
    get_file_mime_type, get_filename_from_path
)
from .exceptions import VideoUploadError, NomadicMLError, ValidationError, APIError

logger = logging.getLogger("nomadicml")
from pathlib import Path
from typing import Sequence, Union, List, Dict, Any, Optional, overload, Literal, Mapping
# ──────────────────────────────────────────────────────────────────────────────
# Type aliases
# ──────────────────────────────────────────────────────────────────────────────
VideoInput   = Union[str, Path]           # paths or URLs/video IDs as str
MetadataInput = Union[str, Path, bytes]  # JSON file path, JSON string, or raw bytes
VideoWithMetadata = tuple[VideoInput, MetadataInput]  # (video, metadata) pair
VideoInputs  = Union[VideoInput, VideoWithMetadata, Sequence[Union[VideoInput, VideoWithMetadata]]]
VideoID      = str
VideoIDList  = Sequence[VideoID]
FolderScopeLiteral = Literal["user", "org", "sample"]
CloudProviderLiteral = Literal["gcs", "s3"]

CLOUD_ALLOWED_EXTENSIONS = {".mp4"}


def _detect_cloud_provider(value: Any) -> CloudProviderLiteral | None:
    """Return the cloud provider inferred from a URI, if any."""
    if isinstance(value, Path):
        candidate = str(value)
    elif isinstance(value, str):
        candidate = value
    else:
        return None

    lowered = candidate.strip().lower()
    if lowered.startswith("gs://"):
        return "gcs"
    if lowered.startswith("s3://"):
        return "s3"
    return None

class AnalysisType(str, Enum):
    """Canonical analysis types exposed by the SDK."""

    ASK = "rapid_review"  # public surface calls this "Ask"

    # Agent families surfaced in the product UI
    GENERAL_AGENT = "edge_case_agent"
    LANE_CHANGE = "lane_change_agent"
    TURN = "turn_agent"
    RELATIVE_MOTION = "relative_motion_agent"
    DRIVING_VIOLATIONS = "violation_agent"
    CUSTOM_AGENT = "custom_agent"

    # Deprecated / legacy aliases kept temporarily for compatibility
    AGENT_GENERAL = GENERAL_AGENT
    LANE_CHANGE_AGENT = LANE_CHANGE
    TURN_AGENT = TURN
    RELATIVE_MOTION_AGENT = RELATIVE_MOTION
    VIOLATION_AGENT = DRIVING_VIOLATIONS
    EDGE_CASE_AGENT = GENERAL_AGENT

    SEARCH = "search"  # DEPRECATED - kept for backwards compatibility

class CustomCategory(str, Enum):
    DRIVING        = "driving"
    ROBOTICS       = "robotics"
    AERIAL         = "aerial"
    SECURITY       = "security"
    ENVIRONMENT  = "environment"

class OverlayMode(str, Enum):
    """Overlay extraction modes for telemetry data."""
    TIMESTAMPS = "timestamps"
    GPS = "gps"
    CUSTOM = "custom"

# Helper ----------------------------------------------------------------------

def _is_iterable(obj):
    """True for list / tuple / set but *not* for strings or Path."""
    return isinstance(obj, Sequence) and not isinstance(obj, (str, Path))


class VideoClient:
    """
    Client for video upload and analysis operations.
    
    This class extends the base NomadicML client with video-specific operations.
    
    Args:
        client: An initialized NomadicML client.
    """
    _status_ranks = {
        "NOT_STARTED": 0,
        "PREPARE_IN_PROGRESS": 0.5,
        "PREPARE_COMPLETED": 1,
        "UPLOADED": 1,
        "DETECTING_IN_PROGRESS": 1.5,
        "PROCESSING": 1.5,
        "DETECTING_COMPLETED": 2,
        "DETECTING_COMPLETED_NO_EVENTS": 2.1,
        "SUMMARIZING_IN_PROGRESS": 2.5,
        "SUMMARIZING_COMPLETED": 3,
        "COMPLETED": 3,
    }

    _BACKEND_SPLIT_SYMBOL = "-----------EVENT_DESCRIPTION-----------"

    _AGENT_DEFAULTS: Dict[AnalysisType, Dict[str, str]] = {
        AnalysisType.GENERAL_AGENT: {
            "edge_case_category": "agent_mode_placeholder",
            "agent_mode": "agent",
        },
        AnalysisType.LANE_CHANGE: {
            "edge_case_category": "Lane Change Detection",
            "agent_mode": "assistant",
        },
        AnalysisType.TURN: {
            "edge_case_category": "Vehicle Turns",
            "agent_mode": "assistant",
        },
        AnalysisType.RELATIVE_MOTION: {
            "edge_case_category": "Relative Motion Analysis",
            "agent_mode": "assistant",
        },
        AnalysisType.DRIVING_VIOLATIONS: {
            "edge_case_category": "Driving Violations",
            "agent_mode": "assistant",
        },
    }

    _ASSISTANT_EDGE_CASES: Dict[AnalysisType, List[Dict[str, Any]]] = {
        AnalysisType.LANE_CHANGE: [
            {
                "title": "lane change",
                "description": "Detect instances where the ego vehicle crosses lane markings to change lanes (left or right).",
                "importance": 80,
            },
        ],
        AnalysisType.TURN: [
            {
                "title": "vehicle turns",
                "description": "Detect left or right turns at intersections or driveways.",
                "importance": 80,
            },
        ],
        AnalysisType.RELATIVE_MOTION: [
            {
                "title": "relative motion",
                "description": "Detect significant relative motion patterns between ego and surrounding vehicles (approach, overtake, diverge).",
                "importance": 70,
            },
        ],
        AnalysisType.DRIVING_VIOLATIONS: [
            {
                "title": "speeding",
                "description": "Detect instances where the ego vehicle exceeds posted speed limits or drives at unsafe speeds.",
                "importance": 90,
            },
            {
                "title": "running red light",
                "description": "Detect when ego vehicle enters intersection after traffic signal turns red.",
                "importance": 95,
            },
            {
                "title": "failure to stop",
                "description": "Detect failures to come to complete stop at stop signs or before right turns on red.",
                "importance": 85,
            },
            {
                "title": "improper lane usage",
                "description": "Detect driving in wrong lane, crossing solid lines, or using emergency/HOV lanes improperly.",
                "importance": 80,
            },
            {
                "title": "following too closely",
                "description": "Detect unsafe following distances or tailgating behavior by ego vehicle.",
                "importance": 75,
            },
        ],
    }

    def _build_agent_request(
        self,
        agent_type: AnalysisType,
        *,
        model_id: str,
        concept_ids: Optional[Sequence[str]] = None,
        _config: str = "default",
    ) -> Dict[str, Any]:
        """Return the form payload matching the agent presets exposed in the product."""

        if agent_type not in self._AGENT_DEFAULTS:
            supported = ", ".join(sorted(t.name for t in self._AGENT_DEFAULTS))
            raise ValueError(f"Unsupported agent analysis type '{agent_type}'. Pick one of: {supported}")

        defaults = self._AGENT_DEFAULTS[agent_type]
        assistant_cases = self._ASSISTANT_EDGE_CASES.get(agent_type, [])

        return {
            "firebase_collection_name": self.client.collection_name,
            "model_id": model_id,
            "edge_case_category": defaults["edge_case_category"],
            "concepts_json": json.dumps(list(concept_ids or [])),
            "mode": defaults["agent_mode"],
            "assistant_edge_cases_json": json.dumps(assistant_cases),
            "config": _config,
        }
    
    def __init__(self, client: NomadicML):
        """
        Initialize the video client with a NomadicML client.
        
        Args:
            client: An initialized NomadicML client.
        """
        self.client = client
        self._user_info = None

    def _print_status_bar(
        self,
        item_id: str,
        *,
        status: str | None = None,
        percent: float | None = None,
        width: int = 30,
    ) -> None:
        """
        Log a tidy ASCII progress-bar.

        Parameters
        ----------
        item_id : str
            Identifier shown in the log line (video_id, sweep_id, …).
        status : str | None
            Human-readable stage label ("UPLOADED", "PROCESSING"…).  
            Ignored when an explicit `percent` is supplied.
        percent : float | None
            0 – 100 exact progress.  If omitted, the method falls back to the
            coarse-grained stage → rank mapping stored in ``self._status_ranks``.
        width : int
            Total bar characters (default 30).
        """
        # ── compute percentage ────────────────────────────────────────────────
        if percent is None:
            # coarse mode: derive % from status → rank table
            rank = self._status_ranks.get((status or "").upper(), 0)
            max_rank = max(self._status_ranks.values()) or 1
            percent = (rank / max_rank) * 100

        # clamp & build bar
        percent = max(0, min(percent, 100))
        filled  = int(percent / 100 * width)
        bar     = "[" + "=" * filled + " " * (width - filled) + "]"

        # choose label
        label = f"{percent:3.0f}%" if status is None else status.upper()

        logger.info(f"{item_id}: {bar} {label}")
            
    async def _get_auth_user(self) -> Optional[Dict[str, Any]]:
        """
        Get the authenticated user information.
        
        Returns:
            A dictionary with user information if available, None otherwise.
        """
        if self.user_info:
            return self.user_info
            
        try:
            response = self.client._make_request(
                method="POST",
                endpoint="/api/keys/verify",
            )
            
            self.user_info = response.json()
            return self.user_info
        except Exception as e:
            logger.warning(f"Failed to get authenticated user info: {e}")
            return None

    def _get_api_events(self, analysis_json: Dict[str, Any]):
        """Return the list of events from either the new or legacy payload."""
        # Check for new analysis document structure first
        if "analysis" in analysis_json and analysis_json["analysis"]:
            events = analysis_json["analysis"].get("events")
            if events is not None:
                return events
        
        # Fall back to legacy structure in metadata.visual_analysis
        events = (
            analysis_json.get("metadata", {})
                        .get("visual_analysis", {})
                        .get("events")
        )
        if events is not None:
            return events
        
        # Try another legacy format
        return (
            analysis_json
            .get("events", {})
            .get("visual_analysis", {})
            .get("status", {})
            .get("quick_summary", {})
            .get("events")
        )

    def _parse_api_events(self, analysis_json, analysis_type=AnalysisType.ASK):
            """
            Parse the API analysis JSON into a list of event dictionaries.
            Handles both legacy (visual_analysis in metadata) and new (analysis document) formats.
            
            Args:
                analysis_json: The raw JSON dict returned from the API.
                default_duration: Default duration (in seconds) to assume if an event only has a single time point.
                analysis_type: The type of analysis performed (e.g., 'rapid_review', 'edge_case', etc.)
                
            Returns:
                list: List of events dictionaries with label, start_time, and end_time
            """
            results = []
            
            # Debug: Print top-level keys to help understand structure
            logger.debug(f"Parsing API events. Top-level keys: {list(analysis_json.keys())}")
            
            # Try different possible paths for events
            events_list = self._get_api_events(analysis_json)

            if not events_list:
                logger.debug("events list empty in API response")
                return results
        
            is_agent_type = False
            if isinstance(analysis_type, AnalysisType):
                is_agent_type = analysis_type in self._AGENT_DEFAULTS
            else:
                try:
                    coerced = self._coerce_analysis_type(analysis_type)
                    is_agent_type = coerced in self._AGENT_DEFAULTS
                except ValueError:
                    is_agent_type = False

            if is_agent_type:
                logger.debug(
                    "Analysis type '%s' detected as agent-based (legacy edge_case), so filtering rejected events.",
                    analysis_type,
                )
                logger.debug(f"Events before filtering: {len(events_list)}")
                events_list = [event for event in events_list if event.get('edgeCaseValidated', 'false').lower() == 'true']
                logger.debug(f"Filtered events count: {len(events_list)}")

            # Process each event
            for event in events_list:
                if not isinstance(event, dict):
                    continue

                # Rapid review events (UI format) → convert to SDK format
                if (analysis_type == AnalysisType.ASK or str(analysis_type) == AnalysisType.ASK.value) and (
                    "type" in event and "time" in event
                ):
                    converted = self._convert_ui_event_to_rapid_review(event)
                    if converted:
                        results.append(converted)
                    continue

                # Already-normalised event (likely from SDK itself)
                if "t_start" in event and "t_end" in event:
                    results.append(event)
                    continue

                # We'll treat 'description' as the label.
                label = event.get("description", "Unknown")

                # Print event structure for debugging
                logger.debug(f"Processing event: {label}")

                # Try to extract start and end time information
                start_time = None
                end_time = None

                if "time" in event:
                    time_str = event.get("time", "")
                    match = re.search(r"t=(\d+(\.\d+)?)", time_str)
                    if match:
                        start_time = float(match.group(1))

                if "end_time" in event:
                    end_time_str = event.get("end_time", "")
                    match = re.search(r"t=(\d+(\.\d+)?)", end_time_str)
                    if match:
                        end_time = float(match.group(1))

                # Check for refined_events if present
                used_refined_events = False
                refined = event.get("refined_events", "")
                if refined:
                    try:
                        refined_data = json.loads(refined)  # Expecting a list of intervals like [start, end, text]
                        if isinstance(refined_data, list):
                            for item in refined_data:
                                if isinstance(item, list) and len(item) >= 2:
                                    st = float(item[0])
                                    en = float(item[1])
                                    results.append({
                                        "label": label,
                                        "start_time": st,
                                        "end_time": en
                                    })
                                    used_refined_events = True
                                    logger.debug(f"  Added refined event: {label} from {st}s to {en}s")
                    except json.JSONDecodeError:
                        logger.warning(f"  Failed to parse refined_events JSON: {refined[:50]}...")
                        pass

                # If no refined intervals and we found basic timing, use that
                if not used_refined_events and start_time is not None and end_time is not None:
                    results.append({
                        "label": label,
                        "start_time": start_time,
                        "end_time": end_time
                    })
                    logger.debug(f"  Added event: {label} from {start_time}s to {end_time}s")
            
            logger.info(f"Total events extracted: {len(results)}")
            return results
    
    def _parse_upload_response(self, video_id: str, payload: Dict[str, Any]) -> Dict[str, str]:
        """Return the compact {{video_id, status}} dict expected by callers."""
        status = (payload.get("status")
                or payload.get("visual_analysis", {})
                        .get("status", {})
                        .get("status", "unknown"))
        return {"video_id": video_id, "status": str(status).lower()}

    @staticmethod
    def _normalize_overlay_value(value: Any) -> Optional[Union[str, float, int]]:
        """Normalize overlay values so they are JSON-friendly and comparable."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return None
            try:
                return float(stripped)
            except ValueError:
                return stripped
        return value

    def _build_overlay_pairs(self, source: Dict[str, Any]) -> Dict[str, OverlayFieldPair]:
        """Extract *_start/*_end pairs from a dict into overlay field structures."""
        overlay_fields: Dict[str, OverlayFieldPair] = {}
        for key, value in source.items():
            if not isinstance(key, str) or key in {"overlay", "data"}:
                continue
            if key.endswith("_start") or key.endswith("_end"):
                base, suffix = key.rsplit("_", 1)
                if not base:
                    continue
                if not base.startswith("frame_"):
                    continue
                normalized = self._normalize_overlay_value(value)
                pair = overlay_fields.setdefault(base, {"start": None, "end": None})
                if suffix == "start":
                    pair["start"] = normalized
                else:
                    pair["end"] = normalized
        cleaned_fields: Dict[str, OverlayFieldPair] = {}
        for field_name, values in overlay_fields.items():
            if values["start"] is None and values["end"] is None:
                continue
            cleaned_fields[field_name] = values
        return cleaned_fields

    def _ensure_overlay_defaults(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Guarantee essential keys are present on returned events."""
        event.setdefault("approval", "pending")
        # frame_* fields may be present temporarily to construct the overlay map
        try:
            if "confidence" in event:
                event["confidence"] = float(event["confidence"])
        except (TypeError, ValueError):
            event["confidence"] = 0.0

        overlay_pairs = self._build_overlay_pairs(event)
        frame_overlay_keys = [
            key for key in list(event.keys())
            if isinstance(key, str)
            and key.startswith("frame_")
            and (key.endswith("_start") or key.endswith("_end"))
        ]
        if overlay_pairs:
            event["overlay"] = overlay_pairs
        for key in frame_overlay_keys:
            event.pop(key, None)

        return event

    def _convert_ui_event_to_rapid_review(self, ui_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a UI-formatted event from Firebase back to RapidReviewEvent format.
        
        The backend stores events in UI format using _ui_event() function,
        but the SDK should return them in the original RapidReviewEvent format.
        
        Args:
            ui_event: Event in UI format from Firebase
            
        Returns:
            Event in RapidReviewEvent format expected by SDK users
        """
        if not ui_event:
            return {}

        def seconds_to_timestamp(time_str: str) -> str:
            """Convert 't=X.XX' format to 'MM:SS' or 'HH:MM:SS' format."""
            if not time_str:
                return "00:00"

            candidate = time_str
            if candidate.startswith("t="):
                candidate = candidate[2:]

            try:
                seconds = float(candidate)
            except (TypeError, ValueError):
                return "00:00"

            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)

            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{secs:02d}"
            return f"{minutes:02d}:{secs:02d}"

        def to_float(value: Any) -> Optional[float]:
            if value in (None, "", "null"):
                return None
            try:
                return float(value)
            except (TypeError, ValueError):
                return None

        original_data = ui_event.get("data", {}) or {}

        frame_ts_start_raw = original_data.get("frame_timestamp_start") or ui_event.get("frame_timestamp_start")
        frame_ts_end_raw = original_data.get("frame_timestamp_end") or ui_event.get("frame_timestamp_end")

        def normalize_timestamp(value: Any) -> Optional[str]:
            if value in (None, "", "null"):
                return None
            return str(value)

        try:
            confidence_value = float(original_data.get("confidence", 0.85))
        except (TypeError, ValueError):
            confidence_value = 0.85

        # Overlay frame_* fields will be converted into event["overlay"] later.
        annotated_thumbnail = (
            original_data.get("annotated_thumbnail_url")
            or ui_event.get("annotated_thumbnail_url")
        )

        rapid_review_event = {
            "t_start": seconds_to_timestamp(ui_event.get("time", "")),
            "t_end": seconds_to_timestamp(ui_event.get("end_time", "")),
            "category": ui_event.get("type", original_data.get("category", "Unknown")),
            "label": ui_event.get("description", original_data.get("label", "")),
            "severity": str(ui_event.get("severity", original_data.get("severity", "medium"))),
            "aiAnalysis": ui_event.get("aiAnalysis", original_data.get("aiAnalysis", "")),
            "confidence": confidence_value,
            "approval": ui_event.get("approval", original_data.get("approval", "pending")),
        }

        if annotated_thumbnail:
            rapid_review_event["annotated_thumbnail_url"] = annotated_thumbnail

        # Only add frame_timestamp fields if they exist in the source data
        if frame_ts_start_raw is not None:
            rapid_review_event["frame_timestamp_start"] = normalize_timestamp(frame_ts_start_raw)
        if frame_ts_end_raw is not None:
            rapid_review_event["frame_timestamp_end"] = normalize_timestamp(frame_ts_end_raw)

        # Add all frame_* fields that exist in original_data (including GPS, speed, etc.)
        # This ensures we only return fields that were actually present in the data
        for key, value in original_data.items():
            if key.startswith("frame_") and (key.endswith("_start") or key.endswith("_end")):
                if key not in rapid_review_event:
                    # For GPS coordinates, convert to float if present
                    if "gps_lat" in key or "gps_lon" in key:
                        rapid_review_event[key] = to_float(value) if value is not None else value
                    else:
                        rapid_review_event[key] = value

        return self._ensure_overlay_defaults(rapid_review_event)

    
    def get_user_id(self) -> Optional[str]:
        """
        Get the authenticated user ID.
        
        Returns:
            The user ID if available, None otherwise.
        """
        # Try to get cached user info
        if self._user_info and "user_id" in self._user_info:
            return self._user_info["user_id"]
        
        # Make a synchronous request to get user info
        try:
            response = self.client._make_request(
                method="POST",
                endpoint="/api/keys/verify"
            )
            self._user_info = response.json()
            return self._user_info.get("user_id")
        except Exception as e:
            logger.warning(f"Failed to get user ID: {str(e)}")
            return None

    def _determine_structured_env(self) -> str:
        """Infer Firestore environment bucket used for reasoning traces."""
        override = os.getenv("DRIVEMONITOR_IS_PROD")
        if override == "true":
            return "pro"
        if override == "false":
            return "dev"

        base = (self.client.base_url or "").lower()
        dev_tokens = ("localhost", "127.0.0.1", "dev.", "-dev", "staging", "-stage", "test.", "preview")
        if any(token in base for token in dev_tokens):
            return "dev"
        return "pro"

    def _normalize_structured_columns(
        self,
        columns: Optional[Sequence[StructuredOddColumn]],
    ) -> List[StructuredOddColumn]:
        """Validate and normalise column definitions before submitting to backend."""
        if columns is None:
            source_columns: List[StructuredOddColumn] = [
                dict(col)  # shallow copy; we'll normalise below
                for col in DEFAULT_STRUCTURED_ODD_COLUMNS
            ]
        else:
            source_columns = list(columns)
            if not source_columns:
                raise ValidationError("At least one column definition is required for structured ODD export.")

        normalized: List[StructuredOddColumn] = []
        for idx, column in enumerate(source_columns):
            if column is None:
                raise ValidationError(f"Column at position {idx} cannot be None.")

            if isinstance(column, dict):
                # Shallow copy so downstream mutation doesn't leak
                col_dict: Dict[str, Any] = {k: v for k, v in column.items() if v is not None}
            else:
                # Support lightweight custom objects with attribute access
                try:
                    col_dict = {
                        "name": getattr(column, "name"),
                        "prompt": getattr(column, "prompt"),
                        "type": getattr(column, "type"),
                    }
                except AttributeError as exc:
                    raise ValidationError(
                        f"Column at position {idx} must supply name, prompt, and type."
                    ) from exc
                literals = getattr(column, "literals", None)
                if literals is not None:
                    col_dict["literals"] = list(literals)

            name = col_dict.get("name")
            prompt = col_dict.get("prompt")
            col_type = col_dict.get("type")

            if not name or not isinstance(name, str):
                raise ValidationError(f"Column at position {idx} is missing a valid 'name'.")
            if not prompt or not isinstance(prompt, str):
                raise ValidationError(f"Column '{name}' is missing a prompt/description.")
            if not col_type or not isinstance(col_type, str):
                raise ValidationError(f"Column '{name}' must define a string 'type'.")

            literals = col_dict.get("literals")
            if literals is not None:
                if not isinstance(literals, (list, tuple)):
                    raise ValidationError(f"Column '{name}' literals must be a list of strings.")
                literal_list = []
                for lit in literals:
                    if not isinstance(lit, str):
                        raise ValidationError(f"Column '{name}' literals must be strings.")
                    literal_list.append(lit)
                if literal_list:
                    col_dict["literals"] = literal_list
                else:
                    col_dict.pop("literals", None)

            entry: StructuredOddColumn = {
                "name": name,
                "prompt": prompt,
                "type": col_type,
            }
            if "literals" in col_dict:
                entry["literals"] = col_dict["literals"]

            normalized.append(entry)

        # Ensure deep copy semantics for consumers (literals lists in particular)
        return json.loads(json.dumps(normalized))

    def generate_structured_odd(
        self,
        video_id: str,
        *,
        columns: Optional[Sequence[StructuredOddColumn]] = None,
        reasoning_trace_path: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> StructuredOddResult:
        """
        Generate an ASAM OpenODD CSV describing the vehicle's operating domain.

        Args:
            video_id: Identifier of the analysed video.
            columns: Optional sequence of column definitions. Defaults to the SDK's
                ASAM-aligned schema if omitted.
            reasoning_trace_path: Optional Firestore document path to capture model
                reasoning. When omitted, the SDK derives the correct bucket.
            timeout: Optional request timeout override in seconds.

        Returns:
            A dictionary containing the CSV text, any share metadata, the final column
            configuration, and the backend response payload.

        Raises:
            ValidationError: If the request is misconfigured.
            NomadicMLError / APIError subclasses: For authentication or backend errors.
        """

        if not video_id or not isinstance(video_id, str):
            raise ValidationError("video_id must be a non-empty string.")

        column_definitions = self._normalize_structured_columns(columns)

        derived_reasoning_path = reasoning_trace_path
        if not derived_reasoning_path:
            user_id = self.get_user_id()
            if not user_id:
                raise NomadicMLError(
                    "Unable to determine user id for structured ODD export. "
                    "Verify that your API key has access to the DriveMonitor dashboard."
                )
            env = self._determine_structured_env()
            derived_reasoning_path = f"user-status/{env}/users/{user_id}/reasoning-traces/structured-output"

        payload = {
            "question": "odd_export",
            "prompt_type": "odd_export",
            "video_id": video_id,
            "reasoning_trace_path": derived_reasoning_path,
            "custom_columns": json.dumps(column_definitions),
        }

        response = self.client._make_request(
            "POST",
            "/api/ask-question",
            data=payload,
            timeout=timeout,
        )

        try:
            data = response.json()
        except ValueError as exc:
            raise NomadicMLError("Structured ODD response was not valid JSON.") from exc

        csv_content = data.get("answer")
        if not csv_content or not isinstance(csv_content, str):
            raise NomadicMLError("Structured ODD export did not return CSV content.")

        result: StructuredOddResult = {
            "csv": csv_content,
            "reasoning_trace_path": derived_reasoning_path,
            "columns": column_definitions,
            "raw": data,
        }

        share_id = data.get("share_id")
        if isinstance(share_id, str):
            result["share_id"] = share_id

        share_url = data.get("share_url")
        if isinstance(share_url, str):
            result["share_url"] = share_url

        processing_time = data.get("processing_time")
        if isinstance(processing_time, (int, float)):
            result["processing_time"] = float(processing_time)

        return result
    
    def _custom_event_detection(
        self,
        video_id: str,
        custom_category: CustomCategory | str,
        event_description: str,
        is_thumbnail: bool = False,
        use_enhanced_motion_analysis: bool = False,
        _config: str = "default",
        confidence: str = "low",
        custom_agent_id: str | None = None,
        overlay_mode: OverlayMode | str | None = None,
    ) -> Dict[str, Any]:
        """
        Ask the backend to derive structured events for ``video_id`` by asking a specific question.
        Uses the POST /ask endpoint for rapid_review.

        Args:
            video_id: The ID of the video.
            custom_category: The category enum or string value, used to form the prompt.
            event_description: The description of the event, used to form the prompt.

        Returns:
            A dictionary with the backend's response.

        Raises:
            NomadicMLError: If the request fails.
        """
        if not event_description and not custom_agent_id:
            raise ValueError("event_description cannot be empty for analysis type rapid_review.")
        if not isinstance(use_enhanced_motion_analysis, bool) and not custom_agent_id:
            raise ValueError("use_enhanced_motion_analysis must be a boolean value.")

        # Extract the string value whether it's an enum or string, default to 'driving' if None
        if custom_category is not None:
            category_value = custom_category.value if isinstance(custom_category, CustomCategory) else custom_category
        else:
            category_value = 'driving'  # Default category matching frontend behavior
        prompt = f"{category_value}{self._BACKEND_SPLIT_SYMBOL}{event_description}"

        payload = {
            "question": prompt,
            "video_id": video_id,
            "is_thumbnail": is_thumbnail,
            "use_enhanced_motion_analysis": use_enhanced_motion_analysis,
            "config": _config,
            "confidence": confidence,
            "custom_agent_id": custom_agent_id,
        }

        # Process overlay_mode
        if overlay_mode:
            # Extract string value whether it's an enum or string
            mode_value = overlay_mode.value if isinstance(overlay_mode, OverlayMode) else overlay_mode.lower()

            if mode_value == "timestamps":
                payload["extract_frame_timestamps"] = True
            elif mode_value == "gps":
                payload["extract_frame_timestamps"] = True
                payload["extract_frame_gps"] = True
            elif mode_value == "custom":
                payload["overlay_mode"] = True

        resp = self.client._make_request("POST", "/api/ask", data=payload)
        
        if resp.status_code == 202:
            # Chunked processing - poll until complete
            result = resp.json()
            analysis_id = result.get("analysis_id")
            if not analysis_id:
                raise NomadicMLError("Backend returned 202 but no analysis_id")
            logger.info(f"Rapid review started. Analysis ID: {analysis_id}")
            # Wait for completion and return final merged result
            return self._wait_for_rapid_review(video_id, analysis_id, is_thumbnail=is_thumbnail)
        elif 200 <= resp.status_code < 300:
            # Immediate response - return as before
            return resp.json()
        else:
            error_msg = resp.json() if resp.content else "Unknown error"
            raise NomadicMLError(f"Failed to generate events via /ask: {format_error_message(error_msg)}")

    # ── batch helpers ───────────────────────────────────────────────────
    def _build_batch_viewer_links(self, batch_id: str) -> Dict[str, str]:
        """Return relative and absolute links for Batch Results Viewer."""
        path = f"/use-cases/rapid-review/batch-view/{batch_id}"

        base_url = os.getenv("NOMADICML_DASHBOARD_BASE_URL")
        if not base_url:
            collection = (self.client.collection_name or "").lower()
            if collection == "videos":
                base_url = "https://app.nomadicml.com"
            else:
                base_url = "https://main.app.nomadicml.com"

        base = base_url.rstrip("/")
        return {"path": path, "url": f"{base}{path}"}

    def _serialize_bool(self, value: bool | None) -> Optional[str]:
        """Serialize booleans for form submissions."""
        if value is None:
            return None
        return "true" if value else "false"

    def _prepare_metadata_upload(self, metadata_file: MetadataInput) -> tuple[str, bytes, str]:
        """Return (filename, content, mimetype) tuple for metadata uploads."""
        if metadata_file is None:
            raise ValidationError("metadata_file cannot be None when preparing upload payload")

        if isinstance(metadata_file, bytes):
            return ("metadata.json", metadata_file, "application/json")

        if isinstance(metadata_file, Path):
            path = metadata_file
        elif isinstance(metadata_file, str):
            candidate = Path(metadata_file)
            if candidate.exists():
                path = candidate
            else:
                # Treat as JSON string
                return ("metadata.json", metadata_file.encode("utf-8"), "application/json")
        else:
            raise ValidationError(f"Unsupported metadata_file type: {type(metadata_file).__name__}. Expected JSON file path, JSON string, or bytes.")

        if not path.exists():
            raise ValidationError(f"metadata_file path does not exist: {path}")

        with open(path, "rb") as fh:
            content = fh.read()

        filename = path.name or "metadata.json"
        return (filename, content, "application/json")

    def _prepare_batch_form(
        self,
        video_ids: List[str],
        *,
        analysis_type: AnalysisType,
        custom_event: Optional[str],
        custom_category: Optional[CustomCategory | str],
        concept_ids: Optional[List[str]],
        model_id: str,
        is_thumbnail: bool,
        use_enhanced_motion_analysis: bool,
        haystack_search: bool = False,
        _config: str = "default",
        confidence: str = "low",
        custom_agent_id: Optional[str] = None,
        overlay_mode: OverlayMode | str | None = None,
    ) -> tuple[str, List[tuple[str, str]]]:
        """Return mode label and list of (key, value) tuples for create-batch."""

        if not video_ids:
            raise ValidationError("No video_ids provided for batch analysis")

        entries: List[tuple[str, str]] = []
        for vid in video_ids:
            entries.append(("video_ids", vid))

        concepts_json = json.dumps(concept_ids or [])

        if analysis_type == AnalysisType.ASK:
            if not custom_event:
                raise ValueError("custom_event must be provided for asking agent batch analyses")
            # Use default category 'driving' if not provided, matching frontend behavior
            if custom_category is not None:
                category_value = custom_category.value if isinstance(custom_category, CustomCategory) else custom_category
            else:
                category_value = 'driving'

            entries.extend([
                ("analysis_kind", "rapid_review"),
                ("prompt", custom_event),
                ("category", category_value),
                ("concepts_json", concepts_json),
                ("config", _config),
                ("confidence", confidence)
            ])

            is_thumb = self._serialize_bool(is_thumbnail)
            if is_thumb is not None:
                entries.append(("is_thumbnail", is_thumb))

            enhanced_motion = self._serialize_bool(use_enhanced_motion_analysis)
            if enhanced_motion is not None:
                entries.append(("use_enhanced_motion_analysis", enhanced_motion))

            haystack = self._serialize_bool(haystack_search)
            if haystack is not None:
                entries.append(("use_embedding_search", haystack))
            
            # Process overlay_mode
            if overlay_mode:
                # Extract string value whether it's an enum or string
                mode_value = overlay_mode.value if isinstance(overlay_mode, OverlayMode) else overlay_mode.lower()

                if mode_value == "timestamps":
                    entries.append(("extract_frame_timestamps", "true"))
                elif mode_value == "gps":
                    entries.append(("extract_frame_timestamps", "true"))
                    entries.append(("extract_frame_gps", "true"))
                elif mode_value == "custom":
                    entries.append(("overlay_mode", "true"))

            mode_label = "rapid_review"
        elif analysis_type == AnalysisType.CUSTOM_AGENT:
            if not custom_agent_id:
                raise ValueError("custom_agent_id must be provided for custom_agent batch analyses")

            entries.extend([
                ("analysis_kind", "rapid_review"),
                ("concepts_json", concepts_json),
                ("model_id", model_id),
                ("config", _config),
                ("custom_agent_id", custom_agent_id),
            ])

            # Process overlay_mode
            if overlay_mode:
                # Extract string value whether it's an enum or string
                mode_value = overlay_mode.value if isinstance(overlay_mode, OverlayMode) else overlay_mode.lower()

                if mode_value == "timestamps":
                    entries.append(("extract_frame_timestamps", "true"))
                elif mode_value == "gps":
                    entries.append(("extract_frame_timestamps", "true"))
                    entries.append(("extract_frame_gps", "true"))
                elif mode_value == "custom":
                    entries.append(("overlay_mode", "true"))

            mode_label = "rapid_review"
        else:
            if analysis_type not in self._AGENT_DEFAULTS:
                supported = ", ".join(sorted(t.name for t in self._AGENT_DEFAULTS))
                raise ValueError(
                    f"Batch agent analyses support only {supported}. Received {analysis_type!r}."
                )

            defaults = self._AGENT_DEFAULTS[analysis_type]
            assistant_edge_cases = self._ASSISTANT_EDGE_CASES.get(analysis_type, [])

            entries.extend([
                ("analysis_kind", "edge_agent"),
                ("concepts_json", concepts_json),
                ("model_id", model_id),
                ("config", _config),
            ])
            entries.append(("edge_case_category", defaults["edge_case_category"]))
            entries.append(("agent_mode", defaults["agent_mode"]))
            entries.append(("assistant_edge_cases_json", json.dumps(assistant_edge_cases)))

            # Return the renamed public-facing mode so batch + single analyses match
            mode_label = "agent"

        entries.append(("start", "true"))
        entries.append(("client_batch_id", uuid.uuid4().hex))

        return mode_label, entries

    def _submit_batch(
        self,
        entries: List[tuple[str, str]],
    ) -> Dict[str, Any]:
        """Call /create-batch and validate response."""
        response = self.client._make_request(
            method="POST",
            endpoint="/api/create-batch",
            data=entries,
        )
        payload = response.json()
        batch_id = payload.get("batch_id")
        if not batch_id:
            raise NomadicMLError("Backend create-batch response was missing batch_id")
        return payload

    def _poll_batch_status(
        self,
        batch_id: str,
        *,
        timeout: int,
        poll_interval: int = 5,
    ) -> Dict[str, Any]:
        """Poll backend batch status endpoint until completion or timeout."""
        deadline = time.time() + timeout
        last_completed = -1

        while True:
            response = self.client._make_request(
                method="GET",
                endpoint=f"/api/batch/{batch_id}/status",
            )
            status_payload = response.json()
            agg = status_payload.get("aggregated_progress") or {}
            total = int(agg.get("total", 0) or 0)
            completed = int(agg.get("completed", 0) or 0)
            status = (status_payload.get("status") or "").lower()

            if completed > last_completed:
                last_completed = completed
                logger.info(
                    "Batch %s progress %s/%s status=%s",
                    batch_id,
                    completed,
                    total,
                    status or "unknown",
                )

            if total > 0 and completed >= total:
                return status_payload
            if status in {"completed", "failed", "cancelled"}:
                return status_payload
            if time.time() > deadline:
                raise TimeoutError(
                    f"Batch {batch_id} did not complete within {timeout} seconds"
                )
            time.sleep(poll_interval)

    def _extract_analysis_id(self, payload: Dict[str, Any]) -> Optional[str]:
        """Best-effort extraction of analysis_id from API payload."""
        if not isinstance(payload, dict):
            return None
        if payload.get("analysis_id"):
            return payload.get("analysis_id")
        analysis = payload.get("analysis")
        if isinstance(analysis, dict) and analysis.get("analysis_id"):
            return analysis.get("analysis_id")
        metadata = payload.get("metadata")
        if isinstance(metadata, dict):
            # Rapid review metadata stores analysis id under visual_analysis
            candidate = metadata.get("analysis_id")
            if candidate:
                return candidate
            visual = metadata.get("visual_analysis", {})
            if isinstance(visual, dict):
                candidate = visual.get("analysis_id") or visual.get("analysisId")
                if candidate:
                    return candidate
        return None

    def _extract_summary(self, payload: Dict[str, Any]) -> str:
        """Fetch summary/answer text from payload where available."""
        if not isinstance(payload, dict):
            return ""
        analysis = payload.get("analysis")
        if isinstance(analysis, dict):
            answer = analysis.get("answer") or analysis.get("summary")
            if isinstance(answer, str):
                return answer
            if isinstance(answer, list):
                return "\n".join(str(item) for item in answer)
        metadata = payload.get("metadata", {})
        if isinstance(metadata, dict):
            visual = metadata.get("visual_analysis", {})
            if isinstance(visual, dict):
                status_block = visual.get("status", {})
                if isinstance(status_block, dict):
                    quick_summary = status_block.get("quick_summary")
                    if isinstance(quick_summary, dict):
                        answer = quick_summary.get("answer")
                        if isinstance(answer, str):
                            return answer
        return ""

    ###### UPLOAD#######################################################################
    @overload
    def upload(self, videos: VideoInput | None = None, /, *,
                folder: str | None = None,
                metadata_file: MetadataInput | None = None,
                scope: FolderScopeLiteral = "user",
                upload_timeout: int = 1_200,
                wait_for_uploaded: bool = True,
                gcs_integration_id: str | None = None,
                integration_id: str | None = None
                ) -> Dict[str, Any]: ...

    @overload
    def upload(self, videos: VideoWithMetadata | None = None, /, *,
                folder: str | None = None,
                scope: FolderScopeLiteral = "user",
                upload_timeout: int = 1_200,
                wait_for_uploaded: bool = True,
                gcs_integration_id: str | None = None,
                integration_id: str | None = None
                ) -> Dict[str, Any]: ...

    @overload
    def upload(self, videos: Sequence[Union[VideoInput, VideoWithMetadata]] | None = None, /, *,
                folder: str | None = None,
                scope: FolderScopeLiteral = "user",
                upload_timeout: int = 1_200,
                wait_for_uploaded: bool = True,
                gcs_integration_id: str | None = None,
                integration_id: str | None = None
                ) -> List[Dict[str, Any]]: ...

    def upload(self, videos: VideoInputs | None = None, /, *,
                folder: str | None = None,
                metadata_file: MetadataInput | None = None,
                scope: FolderScopeLiteral = "user",
                upload_timeout: int = 1_200,
                wait_for_uploaded: bool = True,
                gcs_integration_id: str | None = None,
                integration_id: str | None = None,
                **_):  # swallow unknown kwargs for forward compat
# noqa: E701 – keep signature readable
        """Upload one or many videos from local paths or URLs.

        Parameters
        ----------
        videos            : a single video path/URL, a (video, metadata) tuple,
                           or a sequence of videos/tuples
        folder            : optional folder to organize videos
        metadata_file     : optional Nomadic overlay metadata for single video uploads
                           (ignored when videos is a tuple or contains tuples)
        scope             : "user" (default) or "org" scope hint for folder resolution
        upload_timeout    : seconds to wait in `_wait_for_uploaded`
        wait_for_uploaded : block until backend reports "UPLOADED"
        integration_id    : Optional identifier for use when uploading from saved
                            cloud integrations (GCS or S3). When omitted, the SDK
                            attempts to locate a saved integration whose bucket
                            matches the provided URIs.
        gcs_integration_id: Deprecated alias kept for backwards compatibility with
                            earlier versions of the SDK. Prefer `integration_id`.

        Examples
        --------
        # Single video
        client.upload("video.mp4")

        # Single video with metadata
        client.upload(("video.mp4", "metadata.json"))

        # Multiple videos with mixed metadata
        client.upload([
            ("video1.mp4", "metadata1.json"),
            "video2.mp4",  # No metadata
            ("video3.mp4", "metadata3.json")
        ])
        """
        if videos is None:
            raise ValidationError("Provide at least one video path or URI.")

        resolved_folder_id: Optional[str] = None

        if folder:
            folder_payload = self.create_or_get_folder(folder, scope=scope)
            resolved_folder_id = folder_payload.get("id")

        if integration_id and gcs_integration_id and integration_id != gcs_integration_id:
            raise ValidationError(
                "Specify either integration_id or gcs_integration_id (deprecated), but not both with different values."
            )

        integration_hint = integration_id or gcs_integration_id

        view_set_keys = {"front", "rear", "back", "left", "right", "top", "bottom"}

        def _is_view_set_mapping(value: Any) -> bool:
            return isinstance(value, Mapping) and any(k in value for k in view_set_keys)

        def _looks_like_view_list(value: Any) -> bool:
            if isinstance(value, (str, bytes, Path)):
                return False
            if not isinstance(value, Sequence):
                return False
            seq = list(value)
            if not seq:
                return True
            for item in seq:
                if item is None:
                    continue
                if not isinstance(item, Mapping):
                    return False
                if not any(k in item for k in ("view", "camera", "key", "name", "label")):
                    return False
            return True

        def _is_sequence_of_view_sets(value: Any) -> bool:
            if isinstance(value, (str, bytes, Path)):
                return False
            if not isinstance(value, Sequence):
                return False
            seq = list(value)
            if not seq:
                return False
            return all(_is_view_set_mapping(item) for item in seq)

        if _is_sequence_of_view_sets(videos):
            if metadata_file is not None:
                raise ValidationError("metadata_file cannot be combined with multi-view uploads.")
            results: List[Dict[str, Any]] = []
            for view_set in videos:  # type: ignore[arg-type]
                results.append(
                    self._upload_multi_view(
                        views=view_set,
                        folder_id=resolved_folder_id,
                        scope=scope,
                        wait_for_uploaded=wait_for_uploaded,
                        upload_timeout=upload_timeout,
                        integration_hint=integration_hint,
                    )
                )
            return results

        if isinstance(videos, Mapping) or _looks_like_view_list(videos):
            if metadata_file is not None:
                raise ValidationError("metadata_file cannot be combined with multi-view uploads.")
            return self._upload_multi_view(
                views=videos,
                folder_id=resolved_folder_id,
                scope=scope,
                wait_for_uploaded=wait_for_uploaded,
                upload_timeout=upload_timeout,
                integration_hint=integration_hint,
            )

        cloud_provider: CloudProviderLiteral | None = None
        cloud_targets: List[str] = []
        local_inputs: VideoInputs | None = videos

        def _register_cloud_target(value: Any, provider: CloudProviderLiteral) -> None:
            nonlocal cloud_provider, local_inputs
            if metadata_file is not None:
                raise ValidationError("metadata_file cannot be combined with cloud imports.")
            if cloud_provider and cloud_provider != provider:
                raise ValidationError("Cannot mix GCS and S3 URIs in a single call.")
            cloud_provider = provider
            cloud_targets.append(str(value))
            local_inputs = None

        # Detect cloud imports supplied directly in the videos argument
        if isinstance(videos, tuple):
            first = videos[0]
            provider = _detect_cloud_provider(first)
            if provider:
                raise ValidationError("Cloud imports do not support metadata sidecars.")
        elif isinstance(videos, (str, Path)):
            candidate = str(videos)
            provider = _detect_cloud_provider(candidate)
            if provider:
                _register_cloud_target(candidate, provider)
        elif _is_iterable(videos):
            items = list(videos)
            local_candidates: List[Any] = []
            for item in items:
                if isinstance(item, tuple):
                    provider = _detect_cloud_provider(item[0])
                    if provider:
                        raise ValidationError("Cloud imports do not support metadata sidecars.")
                    local_candidates.append(item)
                    continue
                if not isinstance(item, (str, Path)):
                    raise ValidationError("Expected video paths or URIs.")
                provider = _detect_cloud_provider(item)
                if provider:
                    _register_cloud_target(item, provider)
                else:
                    local_candidates.append(item)

            if cloud_targets:
                if local_candidates:
                    raise ValidationError("Cannot mix cloud URIs with local uploads in a single call.")
                local_inputs = None

        if cloud_targets:
            assert cloud_provider is not None
            bucket, object_names = self._normalize_cloud_uris(cloud_provider, cloud_targets)
            integration_ids, auto_resolved = self._resolve_cloud_integration_ids(
                provider=cloud_provider,
                bucket=bucket,
                explicit_id=integration_hint,
            )
            logger.info(
                "Uploading %d %s object(s) from bucket '%s'",
                len(object_names),
                cloud_provider.upper(),
                bucket,
            )
            if cloud_provider == "gcs":
                video_ids = self._upload_from_gcs(
                    object_names=object_names,
                    integration_ids=integration_ids,
                    folder_id=resolved_folder_id,
                    scope=scope,
                    bucket=bucket,
                    auto_resolved=auto_resolved,
                )
            else:
                video_ids = self._upload_from_s3(
                    object_names=object_names,
                    integration_ids=integration_ids,
                    folder_id=resolved_folder_id,
                    scope=scope,
                    bucket=bucket,
                    auto_resolved=auto_resolved,
                )
            return self._finalize_cloud_upload(video_ids, wait_for_uploaded, upload_timeout)

        if local_inputs is None:
            raise ValidationError("No video inputs provided.")

        # Check if videos is a tuple (single video with metadata)
        if isinstance(local_inputs, tuple):
            if len(local_inputs) != 2:
                raise ValidationError(f"Video/metadata tuple must have exactly 2 elements, got {len(videos)}")
            video_path, video_metadata = local_inputs
            return self._upload_single(
                video_path,
                upload_timeout,
                wait_for_uploaded,
                resolved_folder_id,
                scope,
                metadata_file=video_metadata,
            )

        # Check if it's an iterable (list/sequence)
        if _is_iterable(local_inputs):
            paths = list(local_inputs)
            if not paths:
                raise ValueError("No paths provided")
            return self._upload_many(
                paths,
                upload_timeout,
                wait_for_uploaded,
                resolved_folder_id,
                scope,
            )

        # Single video path without tuple
        return self._upload_single(
            local_inputs,
            upload_timeout,
            wait_for_uploaded,
            resolved_folder_id,
            scope,
            metadata_file=metadata_file,
        )

    def create_or_get_folder(
        self,
        name: str,
        *,
        scope: FolderScopeLiteral = "user",
        org_id: str | None = None,
    ) -> Dict[str, Any]:
        """Guarantee a folder exists and return its metadata."""
        if not name or not name.strip():
            raise ValidationError("Folder name cannot be empty")

        scope_value = scope.lower()
        if scope_value not in {"user", "org"}:
            raise ValidationError(f"Unsupported scope '{scope}'")

        payload: Dict[str, Any] = {
            "name": name.strip(),
            "scope": scope_value,
        }
        if org_id:
            payload["org_id"] = org_id

        response = self.client._make_request(
            method="POST",
            endpoint="/api/folders/create-or-get",
            json_data=payload,
        )

        if not (200 <= response.status_code < 300):
            raise NomadicMLError(
                f"Failed to ensure folder: {format_error_message(response.json())}"
            )

        return response.json()

    #  ── helpers ──────────────────────────────────────────────────────
    def _upload_single(
        self,
        video: VideoInput,
        timeout: int,
        wait: bool,
        folder_id: str | None = None,
        scope: FolderScopeLiteral = "user",
        metadata_file: MetadataInput | None = None,
    ) -> Dict[str, Any]:
        """Delegate to low‑level helper plus optional wait."""
        res = self._upload_video(
            file_path=str(video),
            folder_id=folder_id,
            scope=scope,
            metadata_file=metadata_file,
        )

        vid = res["video_id"]

        if wait:
            self._wait_for_uploaded(vid, timeout=timeout)
            res = self.get_video_status(vid)   # refreshed payload

        return self._parse_upload_response(vid, res)
    

    def _upload_many(self, videos: List[Union[VideoInput, VideoWithMetadata]],
                    timeout: int,
                    wait: bool,
                    folder_id: str | None = None,
                    scope: FolderScopeLiteral = "user") -> List[Dict[str, Any]]:
        """Parallel uploader supporting both plain videos and (video, metadata) tuples.

        Accepts a list where each item can be:
        - A video path/URL (str or Path)
        - A tuple of (video, metadata) where metadata is a JSON file path/string/bytes

        Raises **TypeError** if any item is malformed.
        """
        # Prepare upload tasks with their metadata
        upload_tasks = []
        for i, item in enumerate(videos):
            if isinstance(item, tuple):
                # Validate tuple format
                if len(item) != 2:
                    raise ValidationError(
                        f"Item {i+1}: Video/metadata tuple must have exactly 2 elements, got {len(item)}"
                    )
                video_path, video_metadata = item
                # Validate video path
                if not isinstance(video_path, (str, Path)):
                    raise TypeError(
                        f"Item {i+1}: Video path in tuple must be str or Path, got {type(video_path).__name__}"
                    )
                upload_tasks.append((video_path, video_metadata))
            elif isinstance(item, (str, Path)):
                # Plain video without metadata
                upload_tasks.append((item, None))
            else:
                raise TypeError(
                    f"Item {i+1}: Expected video path or (video, metadata) tuple, got {type(item).__name__}"
                )

        # CONCURRENCY LIMIT: Only 4 uploads will run simultaneously
        # ThreadPoolExecutor internally maintains a queue of pending tasks.
        # Example: When uploading 50 videos:
        #   - ThreadPoolExecutor creates 4 worker threads (max_workers=4)
        #   - All 50 upload tasks are immediately submitted via exe.submit()
        #   - Each submit() returns a Future object and queues the task internally
        #   - First 4 tasks start executing immediately on the 4 threads
        #   - Remaining 46 tasks wait in ThreadPoolExecutor's internal queue
        #   - As each upload completes, that thread automatically picks the next task from queue
        #   - This continues until all 50 uploads are processed
        #
        # This prevents overwhelming backend servers, proxies, and load balancers
        # with too many concurrent connections (which can cause timeouts/failures).
        # Using min(4, len(videos)) ensures we don't create unnecessary threads
        # when uploading fewer than 4 videos.

        with ThreadPoolExecutor(max_workers=min(4, len(upload_tasks))) as exe:
            futs = [
                exe.submit(
                    self._upload_single,
                    video_path,
                    timeout,
                    wait,
                    folder_id,
                    scope,
                    metadata_file=metadata,
                )
                for video_path, metadata in upload_tasks
            ]

            # Collect results, handling individual failures gracefully
            results = []
            for i, f in enumerate(futs):
                try:
                    result = f.result()
                    results.append(result)
                except Exception as e:
                    # Log the failure but continue with other uploads
                    video_info = upload_tasks[i][0]
                    logger.error(f"Upload failed for video {i+1}/{len(upload_tasks)} ({video_info}): {e}")
                    results.append({
                        "video_id": None,
                        "status": "failed",
                        "error": str(e),
                        "file_path": str(video_info)
                    })
            return results  # preserves input order, includes both successes and failures

    ####################################### #ANALYZE #################


    #Single Video decorato
    @overload
    def analyze(
        self,
        ids: VideoID,
        /,
        *,
        analysis_type: AnalysisType,
        model_id: str = "Nomadic-VL-XLarge",
        timeout: int = 2_400,
        wait_for_completion: bool = True,
        folder: str | None = None,
        search_query: str | None = None,
        custom_event: str | None = None,
        custom_category: CustomCategory | str | None = None,
        concept_ids: List[str] | None = None,
        mode: str = "assistant",
        return_subset: bool = False,
        is_thumbnail: bool = False,
        use_enhanced_motion_analysis: bool = False,
        haystack_search: bool = False,
        confidence: str = "low",
        custom_agent_id: str | None = None,
        overlay_mode: OverlayMode | str | None = None,
    ) -> Dict[str, Any]: ...
    
    #Batch Analyze decorator
    @overload
    def analyze(
        self,
        ids: VideoIDList,
        /,
        *,
        analysis_type: AnalysisType,
        model_id: str = "Nomadic-VL-XLarge",
        timeout: int = 2_400,
        wait_for_completion: bool = True,
        folder: str | None = None,
        search_query: str | None = None,
        custom_event: str | None = None,
        custom_category: CustomCategory | str | None = None,
        concept_ids: List[str] | None = None,
        mode: str = "assistant",
        return_subset: bool = False,
        is_thumbnail: bool = False,
        use_enhanced_motion_analysis: bool = False,
        haystack_search: bool = False,
        confidence: str = "low",
        custom_agent_id: str | None = None,
        overlay_mode: OverlayMode | str | None = None,
    ) -> Dict[str, Any]: ...

    def analyze(
        self,
        ids: Union[VideoID, VideoIDList, None] = None,
        /,
        *,
        analysis_type: AnalysisType,
        model_id: str = "Nomadic-VL-XLarge",
        timeout: int = 2_400,
        wait_for_completion: bool = True,
        folder: str | None = None,
        search_query: str | None = None,
        custom_event: str | None = None,
        custom_category: CustomCategory | str | None = None,
        concept_ids: List[str] | None = None,
        mode: str = "assistant",
        return_subset: bool = False,
        is_thumbnail: bool = False,
        use_enhanced_motion_analysis: bool = False,
        haystack_search: bool = False,
        confidence: str = "low",
        custom_agent_id: str | None = None,
        overlay_mode: OverlayMode | str | None = None,
        **legacy_kwargs,
    ):
        """Trigger analysis for one or many video IDs with explicit type.

        Returns a per-video dict for single analyses. When multiple IDs are
        supplied, the return value is a dictionary with ``results`` and
        ``batch_metadata`` keys (see :meth:`_analyze_many`).
        """
        if ids is None and folder is None:
            raise ValueError("Must provide either ids or folder")

        if folder and ids is not None:
            raise ValueError("Provide either ids or folder, not both")

        if confidence not in {"low", "high"}:
            raise ValueError("confidence must be 'low' or 'high'")

        unsupported_kwargs = {key for key in legacy_kwargs if key in {"agent_category", "edge_case_category"}}
        if unsupported_kwargs:
            raise ValueError(
                "Agent categories are now selected via `analysis_type`. "
                "Choose one of the predefined agent types in AnalysisType instead of passing "
                f"{', '.join(sorted(unsupported_kwargs))}."
            )

        analysis_type_enum = self._coerce_analysis_type(analysis_type)
        self._validate_kwargs(
            analysis_type_enum,
            search_query=search_query,
            custom_event=custom_event,
            custom_category=custom_category,
            custom_agent_id=custom_agent_id
        )

        if folder:
            vids_info = self.my_videos(folder_id=folder)
            ids = [v["video_id"] for v in vids_info]
            if not ids:
                raise ValueError(f"No videos found in folder '{folder}'")

        # vector dispatch
        if _is_iterable(ids):
            vids = list(ids)
            if not vids:
                raise ValueError("No video_ids provided")
            return self._analyze_many(
                vids,
                analysis_type_enum,
                model_id,
                timeout,
                wait_for_completion,
                search_query,
                custom_event,
                custom_category,
                concept_ids,
                return_subset,
                is_thumbnail,
                use_enhanced_motion_analysis,
                haystack_search,
                confidence=confidence,
                custom_agent_id=custom_agent_id,
                overlay_mode=overlay_mode,
            )

        return self._analyze_single(
            ids,
            analysis_type_enum,
            model_id,
            timeout,
            wait_for_completion,
            search_query,
            custom_event,
            custom_category,
            concept_ids,
            mode,
            return_subset,
            is_thumbnail,
            use_enhanced_motion_analysis,
            confidence=confidence,
            custom_agent_id=custom_agent_id,
            overlay_mode=overlay_mode,
        )

    def analyze_multiview(
        self,
        view_dict: Dict[str, List[str]],
        *,
        analysis_type: AnalysisType,
        model_id: str = "Nomadic-VL-XLarge",
        timeout: int = 2_400,
        wait_for_completion: bool = True,
        custom_event: str | None = None,
        custom_category: CustomCategory | str | None = None,
        concept_ids: List[str] | None = None,
        mode: str = "assistant",
        return_subset: bool = False,
        is_thumbnail: bool = False,
        use_enhanced_motion_analysis: bool = False,
        haystack_search: bool = False,
        confidence: str = "low",
        custom_agent_id: str | None = None,
        overlay_mode: OverlayMode | str | None = None,
        filter_results: bool = False,
        top_k: int | None = None,
        **legacy_kwargs,
    ) -> Dict[str, Any]:
        """Analyze multiple views of videos and optionally fuse results.

        Args:
            view_dict: Dictionary mapping view identifiers to lists of video IDs.
                      Example: {"FRONT": ["id1", "id2"], "REAR": ["id3", "id4"]}
            analysis_type: Type of analysis to perform
            model_id: Model to use for analysis
            timeout: Maximum time to wait for each view's analysis
            wait_for_completion: Whether to wait for all analyses to complete
            custom_event: Custom event description for ASK analysis
            custom_category: Category for ASK analysis
            concept_ids: Concept IDs for concept-based analysis
            mode: Analysis mode
            return_subset: Whether to return subset of results
            is_thumbnail: Whether analyzing thumbnails
            use_enhanced_motion_analysis: Use enhanced motion analysis
            haystack_search: Enable haystack search
            confidence: Confidence level ("low" or "high")
            custom_agent_id: Custom agent ID for CUSTOM_AGENT analysis
            overlay_mode: Overlay mode for visualization
            filter_results: Whether to sort and filter results by uniqueness before fusion
            top_k: Number of top results to keep per batch when filtering (optional)

        Returns:
            If source URIs are available and fusion succeeds:
                {
                    "view_types": List[str],
                    "fusion_method": "source_uri_matching",
                    "results": List[Dict],  # Fused results per video
                    "unmatched_results": List[Dict]  # Videos that couldn't be matched
                }
            Otherwise:
                List of batch results per view:
                [
                    {"view_key": str, "batch_metadata": Dict, "results": List[Dict]},
                    ...
                ]
        """
        if not view_dict:
            raise ValueError("view_dict must contain at least one view")

        if not wait_for_completion:
            raise ValueError("analyze_multiview requires wait_for_completion=True")

        # Run analyze in series for each view
        batch_results = []
        batch_ids = []
        view_keys = []

        logger.info(f"Starting multi-view analysis for {len(view_dict)} views")

        for view_key, video_ids in view_dict.items():
            if not video_ids:
                logger.warning(f"Skipping view '{view_key}' with no video IDs")
                continue

            logger.info(f"Analyzing view '{view_key}' with {len(video_ids)} videos")

            # Call analyze for this view
            result = self.analyze(
                video_ids,
                analysis_type=analysis_type,
                model_id=model_id,
                timeout=timeout,
                wait_for_completion=True,
                custom_event=custom_event,
                custom_category=custom_category,
                concept_ids=concept_ids,
                mode=mode,
                return_subset=return_subset,
                is_thumbnail=is_thumbnail,
                use_enhanced_motion_analysis=use_enhanced_motion_analysis,
                haystack_search=haystack_search,
                confidence=confidence,
                custom_agent_id=custom_agent_id,
                overlay_mode=overlay_mode,
                **legacy_kwargs,
            )

            batch_results.append({
                "view_key": view_key,
                "batch_metadata": result.get("batch_metadata", {}),
                "results": result.get("results", [])
            })

            if "batch_metadata" in result:
                batch_ids.append(result["batch_metadata"]["batch_id"])
                view_keys.append(view_key)

        if not batch_ids:
            raise ValueError("No valid batches were created")

        # Create batch_ids mapping
        batch_ids_by_view = dict(zip(view_keys, batch_ids))

        # Filter results by uniqueness if requested
        if filter_results:
            logger.info(f"Filtering results for {len(batch_ids)} batches (top_k={top_k})")
            for i, batch_id in enumerate(batch_ids):
                try:
                    sorted_result = self._sort_batch_edge_cases(batch_id, top_k=top_k)
                    # Update batch_results with filtered results
                    if "results" in sorted_result:
                        batch_results[i]["results"] = sorted_result["results"]
                        logger.info(f"Filtered batch {batch_id} to {len(sorted_result['results'])} results")
                except Exception as e:
                    logger.warning(f"Failed to filter batch {batch_id}: {e}")
                    # Continue with unfiltered results

        # Try to fuse results via backend
        try:
            logger.info(f"Attempting to fuse {len(batch_ids)} batch results")
            fused_result = self._fuse_multiview_batches(batch_ids, view_keys)
            logger.info("Multi-view fusion successful")
            # Add batch_ids_by_view to fused result
            fused_result["batch_ids_by_view"] = batch_ids_by_view
            return fused_result
        except Exception as e:
            logger.warning(f"Multi-view fusion failed or not available: {e}")
            logger.info("Returning unfused batch results")
            # Return with batch_ids_by_view for fallback case
            return {
                "batch_ids_by_view": batch_ids_by_view,
                "batch_results": batch_results
            }

    def _fuse_multiview_batches(
        self,
        batch_ids: List[str],
        view_keys: List[str]
    ) -> Dict[str, Any]:
        """Call backend fusion endpoint to merge multi-view results.

        Args:
            batch_ids: List of batch IDs to fuse
            view_keys: List of view identifiers corresponding to batch_ids

        Returns:
            Fused results from backend
        """
        payload = {
            "batch_ids": batch_ids,
            "view_keys": view_keys
        }

        response = self.client._make_request(
            method="POST",
            endpoint="/api/fuse_multiview_results",
            json_data=payload
        )

        return response.json()

    def _sort_batch_edge_cases(
        self,
        batch_id: str,
        top_k: int | None = None
    ) -> Dict[str, Any]:
        """Sort batch results by uniqueness and rarity.

        Args:
            batch_id: ID of the batch to sort
            top_k: Optional number of top results to return after sorting

        Returns:
            Sorted batch results with uniqueness ratings (optionally filtered to top_k)
        """
        endpoint = f"/api/batch/{batch_id}/sort_edge_cases"

        response = self.client._make_request(
            method="POST",
            endpoint=endpoint
        )

        result = response.json()

        # Apply top_k filtering if specified
        if top_k is not None and "results" in result:
            result["results"] = result["results"][:top_k]

        # Parse and convert UI events to SDK format
        return self._parse_sort_response(result, analysis_type=AnalysisType.ASK)

    def _parse_sort_response(
        self,
        sort_response: Dict[str, Any],
        analysis_type: AnalysisType = AnalysisType.ASK
    ) -> Dict[str, Any]:
        """Parse sort_edge_cases response and convert UI events to SDK format.

        The backend returns events in UI format with uniqueness fields. This method:
        1. Extracts the batch metadata
        2. Converts each video's UI events to RapidReviewEvent format
        3. Preserves uniqueness_rating and uniqueness_reasoning fields

        Args:
            sort_response: Raw response from /api/batch/{batch_id}/sort_edge_cases
            analysis_type: Type of analysis (default: AnalysisType.ASK)

        Returns:
            Dict with batch_metadata and results (with converted events)
        """
        batch_metadata = sort_response.get("batch_metadata", {})
        results = []

        for result_item in sort_response.get("results", []):
            video_id = result_item.get("video_id")
            analysis_id = result_item.get("analysis_id")
            analysis = result_item.get("analysis", {})

            # Extract UI events from analysis
            ui_events = analysis.get("events", [])

            # Convert each UI event to RapidReviewEvent format
            converted_events = []
            for ui_event in ui_events:
                if isinstance(ui_event, dict) and "type" in ui_event and "time" in ui_event:
                    # Convert UI format → SDK format (preserves uniqueness fields)
                    converted_event = self._convert_ui_event_to_rapid_review(ui_event)
                    if converted_event:
                        converted_events.append(self._ensure_overlay_defaults(converted_event))
                else:
                    # Already in SDK format or malformed - pass through
                    if isinstance(ui_event, dict):
                        converted_events.append(self._ensure_overlay_defaults(dict(ui_event)))

            # Build result entry
            result_entry = {
                "video_id": video_id,
                "analysis_id": analysis_id,
                "mode": "rapid_review",  # Batch sorting typically used with rapid review
                "status": analysis.get("status", "completed"),
                "events": converted_events,
            }

            results.append(result_entry)

        return {
            "batch_metadata": batch_metadata,
            "results": results,
        }

    #  ── analyze helpers ──────────────────────────────────────────────
    def _validate_kwargs(
        self,
        analysis_type: AnalysisType,
        *,
        search_query: str | None,
        custom_event: str | None,
        custom_category: CustomCategory | str | None,
        custom_agent_id: str | None = None
    ) -> None:
        """Ensure required kwargs are provided for each analysis type."""

        if search_query:
            import warnings
            warnings.warn(
                "analysis_type='search' and search_query parameter are deprecated and have been removed. "
                "Use analysis_type='rapid_review' with custom_event parameter instead "
                "for searching in videos of any length.",
                DeprecationWarning,
                stacklevel=3,
            )
            raise ValueError(
                "analysis_type='search' and search_query parameter have been removed. "
                "Use analysis_type='rapid_review' with custom_event=<your_search_query> instead."
            )

        if analysis_type == AnalysisType.ASK:
            if not custom_event:
                raise ValueError("custom_event is required when analysis_type='ask'")
            # custom_category is now optional, defaults to 'driving' if not provided
            if custom_category is not None:
                if isinstance(custom_category, str) and custom_category not in [cat.value for cat in CustomCategory]:
                    valid_values = ", ".join([f"'{cat.value}'" for cat in CustomCategory])
                    raise ValueError(f"custom_category must be one of {valid_values}")
            return

        if analysis_type == AnalysisType.CUSTOM_AGENT:
            if not custom_agent_id:
                raise ValueError("custom_agent_id is required when analysis_type='custom_agent'")
            return

        if analysis_type in self._AGENT_DEFAULTS:
            if custom_event is not None:
                raise ValueError("custom_event is only valid for AnalysisType.ASK")
            if custom_category is not None:
                raise ValueError("custom_category is only valid for AnalysisType.ASK")
            return

        supported = ", ".join(sorted({AnalysisType.ASK.name, *[agent.name for agent in self._AGENT_DEFAULTS]}))
        raise ValueError(f"Unsupported analysis type '{analysis_type}'. Supported types: {supported}")

    def _coerce_analysis_type(self, analysis_type: AnalysisType | str) -> AnalysisType:
        """Return the canonical :class:`AnalysisType` for user-provided input."""

        if isinstance(analysis_type, AnalysisType):
            return analysis_type

        alias_map = {
            "ask": AnalysisType.ASK,
            "general": AnalysisType.GENERAL_AGENT,
            "general_agent": AnalysisType.GENERAL_AGENT,
            "general-edge-case": AnalysisType.GENERAL_AGENT,
            "edge_case_agent": AnalysisType.GENERAL_AGENT,
            "lane_change": AnalysisType.LANE_CHANGE,
            "lane-change": AnalysisType.LANE_CHANGE,
            "lane_change_agent": AnalysisType.LANE_CHANGE,
            "turn": AnalysisType.TURN,
            "turn_agent": AnalysisType.TURN,
            "relative_motion": AnalysisType.RELATIVE_MOTION,
            "relative-motion": AnalysisType.RELATIVE_MOTION,
            "relative_motion_agent": AnalysisType.RELATIVE_MOTION,
            "driving_violations": AnalysisType.DRIVING_VIOLATIONS,
            "driving-violations": AnalysisType.DRIVING_VIOLATIONS,
            "violation_agent": AnalysisType.DRIVING_VIOLATIONS,
        }

        lookup = str(analysis_type or "").lower()
        if lookup in alias_map:
            return alias_map[lookup]

        for member in AnalysisType:
            if member.value == lookup or member.name.lower() == lookup:
                return member

        valid_values = sorted({member.name for member in AnalysisType} | set(alias_map.keys()))
        raise ValueError(f"analysis_type must be one of {', '.join(valid_values)}")

    def _analyze_single(
        self,
        video_id: str,
        analysis_type: AnalysisType,
        model_id: str,
        timeout: int,
        wait_for_completion: bool,
        search_query: str | None = None,
        custom_event: str | None = None,
        custom_category: CustomCategory | str | None = None,
        concept_ids: list[str] | None = None,
        mode: str = "assistant",
        return_subset: bool = True,
        is_thumbnail: bool = False,
        use_enhanced_motion_analysis: bool = False,
        _config: str = "default",
        confidence: str = "low",
        custom_agent_id: str | None = None,
        overlay_mode: OverlayMode | str | None = None,
    ) -> dict:
        """Run ONE analysis job and hand back a compact dict."""

        # 1) sanity-check combo of flags
        self._validate_kwargs(
            analysis_type,
            search_query=search_query,
            custom_event=custom_event,
            custom_category=custom_category,
            custom_agent_id=custom_agent_id
        )

        analysis_type_enum = analysis_type

        # 2) dispatch by AnalysisType

        if analysis_type_enum == AnalysisType.ASK or analysis_type_enum == AnalysisType.CUSTOM_AGENT:

            if analysis_type_enum == AnalysisType.ASK:
                response = self._custom_event_detection(
                    video_id=video_id,
                    custom_category=custom_category,
                    event_description=custom_event,
                    is_thumbnail=is_thumbnail,
                    use_enhanced_motion_analysis=use_enhanced_motion_analysis,
                    _config=_config,
                    confidence=confidence,
                    overlay_mode=overlay_mode,
                )
            else:
                response = self._custom_event_detection(
                    event_description='',
                    custom_category='',
                    video_id=video_id,
                    _config=_config,
                    custom_agent_id=custom_agent_id,
                    overlay_mode=overlay_mode,
                )

            
            # For is_thumbnail=True, try to fetch thumbnail URLs
            events = response.get("suggested_events", [])
            normalized_events = []
            for ev in events or []:
                if isinstance(ev, dict):
                    normalized_events.append(self._ensure_overlay_defaults(dict(ev)))
                elif ev is not None:
                    normalized_events.append(ev)
            events = normalized_events
            response["suggested_events"] = events
            analysis_id = response.get("analysis_id")
            
            if is_thumbnail and analysis_id and events:
                try:
                    # Get thumbnails for all events
                    thumbnail_urls = self.get_visuals(video_id, analysis_id)
                    # Add thumbnail URLs to events if we got them
                    if thumbnail_urls and len(thumbnail_urls) == len(events):
                        for i, event in enumerate(events):
                            if isinstance(event, dict) and i < len(thumbnail_urls):
                                event["annotated_thumbnail_url"] = thumbnail_urls[i]
                except Exception as e:
                    logger.warning(f"Failed to fetch thumbnails: {e}")
            
            return {
                "video_id": video_id,
                "analysis_id": analysis_id,
                "mode":     "rapid_review",
                "status":   "completed",
                "summary":  response.get("answer", ""),
                "events":   events,
            }

        if analysis_type_enum in self._AGENT_DEFAULTS:
            mode_label = "agent"
            result = self.analyze_video_edge(
                video_id=video_id,
                agent_type=analysis_type_enum,
                model_id=model_id,
                concept_ids=concept_ids,
                _config=_config,
            )
            analysis_id = result.get("analysis_id")

            if not wait_for_completion:
                return {
                    "video_id": video_id,
                    "mode": mode_label,
                    "status": "started",
                    "analysis_id": analysis_id,
                }

            self.wait_for_analysis(video_id, timeout=timeout, analysis_id=analysis_id)
            payload = self.get_video_analysis(video_id, analysis_id=analysis_id)
            events = self._parse_api_events(payload, analysis_type=analysis_type_enum)

            return {
                "video_id": video_id,
                "mode": mode_label,
                "status": "completed",
                "events": events,
                "analysis_id": analysis_id,
            }

        raise ValueError(f"Unsupported analysis type '{analysis_type_enum}'")


# ───────────────────────── analyze (many) ───────────────────────────
    def _analyze_many(
        self,
        video_ids: list[str],
        analysis_type: AnalysisType,
        model_id: str,
        timeout: int,
        wait_for_completion: bool,
        search_query: str | None,
        custom_event: str | None,
        custom_category: CustomCategory | str | None,
        concept_ids: list[str] | None,
        return_subset: bool,
        is_thumbnail: bool = False,
        use_enhanced_motion_analysis: bool = False,
        haystack_search: bool = False,
        _config: str = "default",
        confidence: str = "low",
        custom_agent_id: str | None = None,
        overlay_mode: OverlayMode | str | None = None,
    ) -> Dict[str, Any]:
        """Route multi-video analyses through backend batch orchestration.

        Returns a dictionary with two keys:

        * ``batch_metadata`` – batch identifier plus viewer links.
        * ``results`` – list of per-video analysis dictionaries in the same
          format as :meth:`_analyze_single`.
        """

        if search_query:
            raise ValueError(
                "Batch analyses do not support the deprecated search_query parameter. "
                "Use custom_event with analysis_type='rapid_review' instead."
            )

        mode_label, form_entries = self._prepare_batch_form(
            video_ids,
            analysis_type=analysis_type,
            custom_event=custom_event,
            custom_category=custom_category,
            concept_ids=concept_ids,
            model_id=model_id,
            is_thumbnail=is_thumbnail,
            use_enhanced_motion_analysis=use_enhanced_motion_analysis,
            haystack_search=haystack_search,
            _config=_config,
            confidence=confidence,
            custom_agent_id=custom_agent_id,
            overlay_mode=overlay_mode,
        )

        batch_response = self._submit_batch(form_entries)
        batch_id = batch_response["batch_id"]
        links = self._build_batch_viewer_links(batch_id)
        logger.info(
            "Started batch %s (%s videos) for analysis_type=%s", batch_id,
            len(video_ids), getattr(analysis_type, "value", analysis_type)
        )

        batch_type = "ask" if mode_label == "rapid_review" else "agent"
        batch_metadata = {
            "batch_id": batch_id,
            "batch_viewer_url": links["url"],
            "batch_type": batch_type,
        }

        # Fast acknowledgement path
        if not wait_for_completion:
            ack = []
            for vid in video_ids:
                ack.append({
                    "video_id": vid,
                    "analysis_id": None,
                    "mode": mode_label,
                    "status": "started",
                })
            return {
                "batch_metadata": batch_metadata,
                "results": ack,
            }

        multiplier = max(1, len(video_ids))
        poll_budget = timeout * multiplier if timeout and timeout > 0 else 2400
        # Poll batch status until orchestrator finishes fan-out and harvest per-video pointers.
        batch_status_payload = self._poll_batch_status(batch_id, timeout=int(poll_budget))

        pointer_map: Dict[str, Dict[str, Any]] = {}
        for entry in batch_status_payload.get("videos", []) or []:
            video_id_value = entry.get("video_id")
            if video_id_value:
                pointer_map[str(video_id_value)] = entry

        missing_pointer_error = "Batch orchestrator did not provide analysis pointer for video"
        results: list[dict] = []
        for vid in video_ids:
            pointer = pointer_map.get(vid)
            if not pointer:
                results.append({
                    "video_id": vid,
                    "mode": mode_label,
                    "status": "failed",
                    "events": [],
                    "analysis_id": None,
                    "error": missing_pointer_error,
                })
                continue

            pointer_status_raw = pointer.get("status")
            pointer_status = str(pointer_status_raw).lower() if pointer_status_raw else None
            analysis_id = pointer.get("analysis_id")
            pointer_error = pointer.get("last_error")

            if not analysis_id:
                failure_status = pointer_status if pointer_status == "failed" else "failed"
                results.append({
                    "video_id": vid,
                    "mode": mode_label,
                    "status": failure_status,
                    "events": [],
                    "analysis_id": None,
                    "error": pointer_error or missing_pointer_error,
                })
                continue

            detailed_payload: Dict[str, Any]
            try:
                detailed_payload = self.get_video_analysis(vid, analysis_id=analysis_id)
            except Exception as exc:  # noqa: BLE001 - surface unexpected issues to caller
                results.append({
                    "video_id": vid,
                    "mode": mode_label,
                    "status": pointer_status or "failed",
                    "events": [],
                    "analysis_id": analysis_id,
                    "error": pointer_error or str(exc),
                })
                continue

            events = self._parse_api_events(detailed_payload, analysis_type=analysis_type)
            status_value = self._status_from_metadata(detailed_payload.get("metadata", {}))
            if not status_value and isinstance(detailed_payload.get("analysis"), dict):
                status_value = detailed_payload.get("analysis", {}).get("status")
            status_value = (status_value or pointer_status or "completed").lower()
            if status_value not in {"completed", "failed"}:
                status_value = "completed"

            result_entry: Dict[str, Any] = {
                "video_id": vid,
                "analysis_id": analysis_id or self._extract_analysis_id(detailed_payload),
                "mode": mode_label,
                "status": status_value,
            }

            # Include import_source_uri if present (for S3/GCS uploaded videos)
            metadata = detailed_payload.get("metadata") or {}
            import_source_uri = metadata.get("import_source_uri")
            if import_source_uri:
                result_entry["import_source_uri"] = import_source_uri

            if mode_label == "rapid_review":
                summary_text = self._extract_summary(detailed_payload) or ""
                result_entry["summary"] = summary_text

            result_entry["events"] = events

            if status_value == "failed":
                result_entry.setdefault("error", pointer_error or "Analysis failed")

            results.append(result_entry)

        return {
            "batch_metadata": batch_metadata,
            "results": results,
        }
    #########################


    def _normalize_cloud_uris(
        self,
        provider: CloudProviderLiteral,
        uris: str | Sequence[str],
    ) -> tuple[str, List[str]]:
        """Validate and split cloud URIs into bucket and object names."""
        provider_label = provider.upper()
        if isinstance(uris, str):
            values = [uris]
        elif _is_iterable(uris):
            values = [str(item) for item in uris]
        else:
            raise ValidationError(f"{provider_label} URIs must be a string or a sequence of strings")

        if not values:
            raise ValidationError(f"No {provider_label} URIs provided.")

        bucket_name: Optional[str] = None
        object_names: List[str] = []
        expected_scheme = "gs" if provider == "gcs" else "s3"

        for raw in values:
            candidate = raw.strip()
            if not candidate:
                raise ValidationError(f"Encountered empty {provider_label} URI.")

            parsed = urlparse(candidate)
            if parsed.scheme != expected_scheme:
                raise ValidationError(
                    f"{provider_label} URI must start with '{expected_scheme}://', got '{candidate}'"
                )

            bucket = parsed.netloc
            if not bucket:
                raise ValidationError(f"{provider_label} URI '{candidate}' is missing a bucket name.")

            object_name = parsed.path.lstrip("/")
            if not object_name:
                raise ValidationError(f"{provider_label} URI '{candidate}' is missing an object path.")

            _, ext = os.path.splitext(object_name)
            if ext.lower() not in CLOUD_ALLOWED_EXTENSIONS:
                allowed = ", ".join(sorted(CLOUD_ALLOWED_EXTENSIONS))
                raise ValidationError(
                    f"Unsupported {provider_label} file extension '{ext}' for '{candidate}'. "
                    f"Supported extensions: {allowed}"
                )

            if bucket_name is None:
                bucket_name = bucket
            elif bucket != bucket_name:
                raise ValidationError(
                    "All cloud URIs in a single upload must reference the same bucket. "
                    f"Expected '{bucket_name}', got '{bucket}' for '{candidate}'."
                )

            object_names.append(object_name)

        unique_objects = list(dict.fromkeys(object_names))

        if bucket_name is None:
            raise ValidationError(f"Unable to determine bucket name from {provider_label} URIs.")

        return bucket_name, unique_objects

    def _resolve_cloud_integration_ids(
        self,
        *,
        provider: CloudProviderLiteral,
        bucket: str,
        explicit_id: str | None,
    ) -> tuple[List[str], bool]:
        """Return candidate integration ids plus a flag indicating auto-resolution."""
        if explicit_id:
            return [explicit_id], False

        helper = getattr(self.client, "cloud_integrations", None)
        if helper is None:
            raise ValidationError(
                "No cloud integration id provided and the client is missing the cloud integrations helper. "
                "Call client.cloud_integrations.add()/list() or provide integration_id explicitly."
            )

        try:
            integrations = helper.list(type=provider)
        except Exception as exc:  # pragma: no cover - defensive
            raise NomadicMLError(f"Failed to list cloud integrations: {exc}") from exc

        matches = [item for item in integrations if item.get("bucket") == bucket]
        if not matches:
            raise ValidationError(
                f"No saved {provider.upper()} integration found for bucket '{bucket}'. "
                "Save an integration or supply integration_id explicitly."
            )
        candidate_ids: List[str] = []
        for match in matches:
            integration_id = match.get("id")
            if integration_id:
                candidate_ids.append(str(integration_id))
        if not candidate_ids:
            raise NomadicMLError(
                f"Saved {provider.upper()} integration for bucket '{bucket}' is missing an id."
            )
        return candidate_ids, True

    def _upload_from_gcs(
        self,
        *,
        object_names: Sequence[str],
        integration_ids: Sequence[str],
        folder_id: str | None,
        scope: FolderScopeLiteral,
        bucket: str,
        auto_resolved: bool,
    ) -> List[str]:
        """Kick off backend uploads for objects already stored in GCS."""
        last_error: Exception | None = None
        for integration_id in integration_ids:
            payload: Dict[str, Any] = {
                "integration_id": integration_id,
                "files": list(object_names),
                "collection": self.client.collection_name,
                "folder_id": folder_id,
                "scope": scope,
            }

            try:
                response = self.client._make_request(
                    method="POST",
                    endpoint="/api/gcs/upload",
                    json_data=payload,
                )
            except APIError as exc:
                last_error = exc
                logger.debug(
                    "GCS upload failed with integration_id=%s (status=%s)",
                    integration_id,
                    exc.status_code,
                )
                continue

            data = response.json()
            video_ids = data.get("uploaded_video_ids")
            if not isinstance(video_ids, list):
                raise NomadicMLError("Unexpected response from /api/gcs/upload; missing 'uploaded_video_ids'.")
            if not video_ids:
                raise NomadicMLError("GCS upload returned no video ids.")
            return [str(vid) for vid in video_ids]

        if last_error is not None:
            if auto_resolved:
                raise ValidationError(
                    f"No saved GCS integration succeeded for bucket '{bucket}'. "
                    "Add or update the integration and try again."
                ) from last_error
            raise last_error

        raise ValidationError(
            "No cloud integration id provided. Pass integration_id or save a cloud integration."
        )

    def _upload_from_s3(
        self,
        *,
        object_names: Sequence[str],
        integration_ids: Sequence[str],
        folder_id: str | None,
        scope: FolderScopeLiteral,
        bucket: str,
        auto_resolved: bool,
    ) -> List[str]:
        """Kick off backend uploads for objects already stored in S3."""
        last_error: Exception | None = None
        for integration_id in integration_ids:
            payload: Dict[str, Any] = {
                "integration_id": integration_id,
                "keys": list(object_names),
                "collection": self.client.collection_name,
                "folder_id": folder_id,
                "scope": scope,
                "bucket": bucket,
            }

            try:
                response = self.client._make_request(
                    method="POST",
                    endpoint="/api/s3/upload",
                    json_data=payload,
                )
            except APIError as exc:
                last_error = exc
                logger.debug(
                    "S3 upload failed with integration_id=%s (status=%s)",
                    integration_id,
                    exc.status_code,
                )
                continue

            data = response.json()
            video_ids = data.get("uploaded_video_ids")
            if not isinstance(video_ids, list):
                raise NomadicMLError("Unexpected response from /api/s3/upload; missing 'uploaded_video_ids'.")
            if not video_ids:
                raise NomadicMLError("S3 upload returned no video ids.")
            return [str(vid) for vid in video_ids]

        if last_error is not None:
            if auto_resolved:
                raise ValidationError(
                    f"No saved S3 integration succeeded for bucket '{bucket}'. "
                    "Add or update the integration and try again."
                ) from last_error
            raise last_error

        raise ValidationError(
            "No cloud integration id provided. Pass integration_id or save a cloud integration."
        )

    def _normalize_multi_view_payload(self, views: Any) -> Dict[str, str]:
        """Normalize multi-view input (mapping or list) into {view: uri} form."""
        normalized: Dict[str, str] = {}

        def _push(key: Any, value: Any) -> None:
            if not isinstance(key, str):
                raise ValidationError("View names must be strings.")
            uri = "" if value is None else str(value).strip()
            view_key = key.strip().lower()
            if not view_key or not uri:
                return
            if view_key in normalized:
                raise ValidationError(f"Duplicate view '{view_key}' in views payload.")
            normalized[view_key] = uri

        if views is None:
            return normalized

        if isinstance(views, Mapping):
            for raw_key, raw_uri in views.items():
                if raw_uri is None:
                    continue
                _push(raw_key, raw_uri)
            return normalized

        if _is_iterable(views) and not isinstance(views, (str, bytes, Path)):
            for item in views:
                if item is None:
                    continue

                view_key: Any = None
                uri: Any = None

                if isinstance(item, Mapping):
                    view_key = (
                        item.get("view")
                        or item.get("camera")
                        or item.get("key")
                        or item.get("name")
                        or item.get("label")
                    )
                    uri = (
                        item.get("uri")
                        or item.get("url")
                        or item.get("video")
                        or item.get("path")
                        or item.get("value")
                        or item.get("video_id")
                        or item.get("videoId")
                    )
                elif isinstance(item, (list, tuple)) and len(item) >= 2:
                    view_key, uri = item[0], item[1]
                else:
                    raise ValidationError("Multi-view list entries must be dictionaries with 'view' and 'uri'.")

                if view_key is None:
                    raise ValidationError("Multi-view list entries must include a view name.")
                _push(view_key, uri)
            return normalized

        raise ValidationError("Multi-view uploads must be a mapping or list of view entries.")

    def _upload_multi_view(
        self,
        *,
        views: Any,
        folder_id: str | None,
        scope: FolderScopeLiteral,
        wait_for_uploaded: bool,
        upload_timeout: int,
        integration_hint: str | None,
    ) -> Dict[str, Any]:
        """Upload a set of synchronized camera views, then stitch them server-side."""
        normalized = self._normalize_multi_view_payload(views)
        if not normalized:
            raise ValidationError("Multi-view upload requires at least one view.")

        if "front" not in normalized:
            raise ValidationError("A 'front' view is required for multi-view uploads.")

        id_map: Dict[str, str] = {}

        def _require_video_id(res: Dict[str, Any], view_key: str) -> str:
            vid = res.get("video_id")
            if not vid:
                err_msg = res.get("error") or res.get("status") or "unknown error"
                raise NomadicMLError(f"Multi-view upload failed for view '{view_key}': {err_msg}")
            return str(vid)

        # Decide upload strategy: all cloud (same provider/bucket) or all non-cloud.
        providers = []
        for value in normalized.values():
            providers.append(_detect_cloud_provider(value))
        cloud_providers = {p for p in providers if p is not None}
        has_cloud = bool(cloud_providers)
        has_local = any(p is None for p in providers)

        if has_cloud and has_local:
            raise ValidationError("Multi-view uploads must be all cloud URIs or all local/HTTP URLs, not mixed.")

        if has_cloud:
            if len(cloud_providers) > 1:
                raise ValidationError("All cloud views must use the same provider.")
            provider = cloud_providers.pop()
            bucket, object_names = self._normalize_cloud_uris(provider, list(normalized.values()))

            # Build view->object map preserving input order
            view_objects: list[tuple[str, str]] = []
            for view_key, uri in normalized.items():
                parsed = urlparse(uri)
                obj = parsed.path.lstrip("/")
                view_objects.append((view_key, obj))

            integration_ids, auto_resolved = self._resolve_cloud_integration_ids(
                provider=provider,
                bucket=bucket,
                explicit_id=integration_hint,
            )

            if provider == "gcs":
                video_ids = self._upload_from_gcs(
                    object_names=object_names,
                    integration_ids=integration_ids,
                    folder_id=folder_id,
                    scope=scope,
                    bucket=bucket,
                    auto_resolved=auto_resolved,
                )
            else:
                video_ids = self._upload_from_s3(
                    object_names=object_names,
                    integration_ids=integration_ids,
                    folder_id=folder_id,
                    scope=scope,
                    bucket=bucket,
                    auto_resolved=auto_resolved,
                )

            upload_result = self._finalize_cloud_upload(
                video_ids,
                wait_for_uploaded,
                upload_timeout,
            )

            # Normalize to list
            results_list: list[Dict[str, Any]]
            if isinstance(upload_result, dict):
                results_list = [upload_result]
            else:
                results_list = upload_result

            if len(results_list) != len(view_objects):
                raise NomadicMLError("Unexpected cloud upload response; count mismatch for multi-view upload.")

            for (view_key, _obj), res in zip(view_objects, results_list):
                id_map[view_key] = _require_video_id(res, view_key)
        else:
            # Local paths or HTTP URLs; reuse parallel uploader
            view_items = list(normalized.items())
            payloads = [val for _, val in view_items]
            results = self._upload_many(
                payloads,
                upload_timeout,
                wait_for_uploaded,
                folder_id=folder_id,
                scope=scope,
            )
            if len(results) != len(view_items):
                raise NomadicMLError("Unexpected upload response; count mismatch for multi-view upload.")
            for (view_key, _), res in zip(view_items, results):
                id_map[view_key] = _require_video_id(res, view_key)

        primary_video_id = id_map.get("front")
        if not primary_video_id:
            raise NomadicMLError("Front view upload did not return a video_id.")

        # Stitch on the backend
        try:
            response = self.client._make_request(
                method="POST",
                endpoint="/api/multi-view/stitch",
                json_data={
                    "primary_view_id": primary_video_id,
                    "views": id_map,
                },
            )
            data = response.json()
            stitched_views = data.get("views") if isinstance(data.get("views"), dict) else id_map
        except APIError as exc:
            logger.debug("Multi-view stitch failed: %s", exc)
            stitched_views = id_map  # fall back to local map so caller still has ids

        # Mirror regular upload return shape; front ID only to avoid confusion
        status_payload: Dict[str, Any] = {"status": "processing"}
        if wait_for_uploaded:
            status_payload = self.get_video_status(primary_video_id)
        return self._parse_upload_response(primary_video_id, status_payload)

    def _finalize_cloud_upload(
        self,
        video_ids: Sequence[str],
        wait_for_uploaded: bool,
        timeout: int,
    ) -> Union[Dict[str, str], List[Dict[str, str]]]:
        """Normalize cloud-upload responses so they match the local upload contract."""
        results: List[Dict[str, str]] = []
        for vid in video_ids:
            payload: Dict[str, Any]
            if wait_for_uploaded:
                self._wait_for_uploaded(vid, timeout=timeout)
                payload = self.get_video_status(vid)
            else:
                payload = {"status": "processing"}
            results.append(self._parse_upload_response(vid, payload))

        if len(results) == 1:
            return results[0]
        return results

    def _upload_video(
        self,
        file_path: str,
        *,
        folder_id: Optional[str] = None,
        scope: FolderScopeLiteral = "user",
        metadata_file: MetadataInput | None = None,
        # ¦ deprecated ------------------------------------------------------
        source: Union[str, VideoSource, None] = None,
     ) -> Dict[str, Any]:
        """
        Upload a video for analysis.
        
        Args:
            file_path: Local path or remote URL of the video.
            folder_id: Optional id of the folder to organize the video.
            metadata_file: Optional Nomadic overlay metadata dictionary/file/JSON string.
            source: Deprecated. Ignored by the SDK.
        
        Returns:
            A dictionary with the upload status and video_id.
        
        Raises:
            ValidationError: If the input parameters are invalid.
            VideoUploadError: If the upload fails.
            APIError: If the API returns an error.
            NomadicMLError: For any other errors.
        """
        if source is not None:
            logger.warning("'source' parameter is deprecated and ignored; the SDK infers the source automatically.")
        
        if not file_path:
            raise ValidationError("Must provide file_path")

        # ── determine source type -----------------------------------------
        inferred_source = infer_source(file_path)
        
        # Only support FILE and VIDEO_URL, not SAVED
        if inferred_source == VideoSource.SAVED:
            raise ValidationError("Cannot upload from saved video ID. Use analyze() to analyze existing videos.")

        # Prepare request data ----------------------------------------------
        endpoint = "/api/upload-video"

        form_data: Dict[str, Any] = {
            "source": inferred_source.value,
            "firebase_collection_name": self.client.collection_name,
            "scope": scope,
        }
        if folder_id:
            form_data["folder_id"] = folder_id
        files = None

        if inferred_source == VideoSource.FILE:
            filename = get_filename_from_path(file_path)
            mime_type = get_file_mime_type(file_path)
            with open(file_path, "rb") as f:
                file_content = f.read()
            files = {"file": (filename, file_content, mime_type)}
            logger.info(f"Uploading local file: {filename}")
        elif inferred_source == VideoSource.VIDEO_URL:
            form_data["video_url"] = file_path
            logger.info(f"Uploading by URL: {file_path}")

        if metadata_file is not None:
            metadata_payload = self._prepare_metadata_upload(metadata_file)
            files = files or {}
            files["metadata_file"] = metadata_payload

        # Make the request ---------------------------------------------------
        response = self.client._make_request(
            method="POST",
            endpoint=endpoint,
            data=form_data,
            files=files,
            timeout=self.client.timeout * 20,
        )

        if not (200 <= response.status_code < 300):
            raise VideoUploadError(f"Failed to upload video: {format_error_message(response.json())}")

        logger.info(f"Upload (source={inferred_source.value}) response: {response.json()}")

        return response.json()

    def analyze_video(self, video_id: str, model_id: Optional[str] = "Nomadic-VL-XLarge") -> Dict[str, Any]:
        """
        Start analysis for an uploaded video.
        
        Args:
            video_id: The ID of the video to analyze.
            
        Returns:
            A dictionary with the analysis status.
            
        Raises:
            AnalysisError: If the analysis fails to start.
            APIError: If the API returns an error.
            NomadicMLError: For any other errors.
        """
        endpoint = f"/api/analyze-video/{video_id}"
        
        # Prepare form data with the collection name
        data = {
            "firebase_collection_name": self.client.collection_name,
            "model_id": model_id,
        }
        
        # Make the request
        response = self.client._make_request(
            method="POST",
            endpoint=endpoint,
            data=data,
        )
        
        # Return the parsed JSON response
        return response.json()

    def analyze_video_edge(
        self,
        video_id: str,
        agent_type: AnalysisType,
        *,
        model_id: str = "Nomadic-VL-XLarge",
        concept_ids: Optional[Sequence[str]] = None,
        _config: str = "default",
    ) -> Dict[str, Any]:
        """Start an agent (edge-case) analysis for an uploaded video."""

        if agent_type not in self._AGENT_DEFAULTS:
            supported = ", ".join(sorted(agent.name for agent in self._AGENT_DEFAULTS))
            raise ValueError(f"Unsupported agent type '{agent_type}'. Supported options: {supported}")

        endpoint = f"/api/analyze-video-edge/{video_id}"
        data = self._build_agent_request(
            agent_type,
            model_id=model_id,
            concept_ids=concept_ids,
            _config=_config,
        )

        response = self.client._make_request(
            method="POST",
            endpoint=endpoint,
            data=data,
        )
        return response.json()
    
    def get_video_status(self, video_id: str) -> Dict[str, Any]:
        """
        Get the status of a video analysis.
        
        Args:
            video_id: The ID of the video.
            
        Returns:
            A dictionary with the video status.
            
        Raises:
            APIError: If the API returns an error.
            NomadicMLError: For any other errors.
        """
        endpoint = f"/api/video/{video_id}/status"
        
        # Add the required collection_name parameter
        params = {"firebase_collection_name": self.client.collection_name}
        
        # Make the request
        response = self.client._make_request("GET", endpoint, params=params)
        
        # Return the parsed JSON response
        return response.json()
        
    def wait_for_analysis(
        self,
        video_id: str,
        timeout: int = 2_400, # Default 40 minutes
        poll_interval: int = 5,
        analysis_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Block until the video analysis completes or times out.
        
        Args:
            video_id: The ID of the video to wait for.
            timeout: Maximum time to wait in seconds before raising TimeoutError.
            poll_interval: Time between status checks in seconds.
            analysis_id: Optional analysis ID for new EC analyses stored in separate docs.
            
        Returns:
            A dictionary with the final video status payload.
            
        Raises:
            TimeoutError: If the analysis doesn't complete within the timeout period.
        """
        start_time = time.time()
        
        # For new edge case analyses with analysis_id, we need to poll differently
        if analysis_id:
            while True:
                # Get the full analysis document which includes status
                payload = self.get_video_analysis(video_id, analysis_id=analysis_id)
                # Check if analysis document exists and has status
                if "analysis" in payload and "status" in payload["analysis"]:
                    status = str(payload["analysis"]["status"]).upper()
                else:
                    # Fallback to metadata status for compatibility
                    status = self._status_from_metadata(payload.get("metadata", {})) or "PROCESSING"
                    status = status.upper()
                
                self._print_status_bar(f"{video_id}:{analysis_id}", status=status)
                logger.debug(f"Analysis {analysis_id} for video {video_id} - Status: '{status}'")
                
                if status in {"COMPLETED", "FAILED"}:
                    logger.info(f"Analysis {analysis_id} reached terminal status: {status}.")
                    return payload
                    
                if time.time() - start_time > timeout:
                    msg = f"Analysis {analysis_id} for {video_id} did not complete in {timeout}s. Last status: {status}"
                    logger.error(msg)
                    raise TimeoutError(msg)
                    
                time.sleep(poll_interval)
        else:
            # Legacy behavior for analyses without analysis_id
            while True:
                payload = self.get_video_status(video_id)
                status = str(payload.get("status", "")).upper()
                self._print_status_bar(video_id, status=status)
                logger.debug(f"Video {video_id} - Status: '{status}', payload: '{payload}'")
                
                if status in {"COMPLETED", "FAILED"}:
                    logger.info(f"Video {video_id} reached terminal status: {status}.")
                    return payload
                    
                if time.time() - start_time > timeout:
                    msg = f"Analysis for {video_id} did not complete in {timeout}s. Last status: {status}"
                    logger.error(msg)
                    raise TimeoutError(msg)
                    
                time.sleep(poll_interval)

    def wait_for_analyses(
        self,
        video_ids,
        timeout: int = 4800,
        poll_interval: int = 5
    ) -> dict:
        """
        Wait for multiple video analyses in parallel, with pretty status bars.
        """
        ids = list(video_ids)
        results = {}
        with ThreadPoolExecutor(max_workers=len(ids)) as executor:
            futures = {executor.submit(self.wait_for_analysis, vid, timeout, poll_interval): vid for vid in ids}
            for fut in as_completed(futures):
                vid = futures[fut]
                try:
                    results[vid] = fut.result()
                except Exception as e:
                    results[vid] = e
        return results
    
    def get_video_analysis(self, video_id: str, analysis_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the complete analysis of a video.
        
        Args:
            video_id: The ID of the video.
            analysis_id: Optional analysis ID for new EC analyses stored in separate docs.
            
        Returns:
            The complete video analysis. For new analyses with analysis_id, includes
            both metadata and the analysis document.
            
        Raises:
            APIError: If the API returns an error.
            NomadicMLError: For any other errors.
        """
        if analysis_id:
            # Use the new endpoint for fetching analysis documents
            endpoint = f"/api/videos/{video_id}/analyses/{analysis_id}"
            params = {"firebase_collection_name": self.client.collection_name}
            
            response = self.client._make_request(
                method="GET",
                endpoint=endpoint,
                params=params,
            )
            
            return response.json()
        else:
            # Use the original endpoint for legacy analyses
            endpoint = f"/api/video/{video_id}/analysis"
            params = {"firebase_collection_name": self.client.collection_name}
                    
            response = self.client._make_request(
                method="GET",
                endpoint=endpoint,
                params=params,
            )
            
            return response.json()
    
    def get_video_analyses(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get analyses for multiple videos.
        
        Args:
            video_ids: List of video IDs.
            
        Returns:
            A list of analyses for each video.
            
        Raises:
            APIError: If the API returns an error.
            NomadicMLError: For any other errors.
        """
        analyses = []
        for vid in video_ids:
            analysis = self.get_video_analysis(vid)
            analyses.append(analysis)
        return analyses
    
    def get_detected_events(self, video_id: str) -> List[Dict[str, Any]]:
        """
        Get detected events for a video.

        Args:
            video_id: The ID of the video.

        Returns:
            A list of detected events.

        Raises:
            APIError: If the API returns an error.
            NomadicMLError: For any other errors.
        """
        return self._parse_api_events(self.get_video_analysis(video_id))

    def get_batch_analysis(
        self,
        batch_id: str,
        filter: Optional[Union[str, List[str]]] = None
    ) -> Dict[str, Any]:
        """
        Get the analysis results for a completed batch by batch_id.

        Args:
            batch_id: The ID of the batch to retrieve.
            filter: Filter events by approval status. Can be a single string or list of strings.
                   Valid values: 'approved', 'rejected', 'pending', 'invalid'.
                   Defaults to all statuses if not specified.

        Returns:
            A dictionary with 'batch_metadata' and 'results' keys.
            - batch_metadata: Contains batch_id, batch_viewer_url, batch_type, analysis_type,
                            and configuration details (prompt, category, etc for Ask batches)
            - results: List of per-video analysis dictionaries with filtered events

        Raises:
            NomadicMLError: If batch is not completed or other errors occur.
            ValidationError: If filter contains invalid values.
        """
        # Validate and normalize filter parameter
        if filter is None:
            filter_list = None  # Backend will use default
        elif isinstance(filter, str):
            filter_list = [filter]
        else:
            filter_list = list(filter)

        # Basic validation before sending to backend
        if filter_list is not None:
            valid_filters = {'approved', 'rejected', 'pending', 'invalid'}
            invalid_filters = set(filter_list) - valid_filters
            if invalid_filters:
                raise ValidationError(
                    f"Invalid filter value(s): {', '.join(invalid_filters)}. "
                    f"Must be one of: approved, rejected, pending, invalid"
                )

        # Call the new backend endpoint that handles all the filtering logic
        payload = {"filter": filter_list}

        response = self.client._make_request(
            method="POST",
            endpoint=f"/api/batch/{batch_id}/filter_batch",
            json_data=payload,
        )

        return response.json()

    def add_batch_metadata(
        self,
        batch_id: str,
        metadata: Dict[str, Union[str, int]]
    ) -> Dict[str, Any]:
        """
        Add or update metadata for a batch analysis.
        New metadata keys will be merged with existing metadata, overwriting keys with the same name.

        Args:
            batch_id: The ID of the batch to update.
            metadata: Dictionary with string keys and string/int values (non-nested).

        Returns:
            Dictionary with success status and updated metadata.

        Raises:
            ValidationError: If metadata format is invalid.
            NomadicMLError: If the API request fails.

        Example:
            >>> client.video.add_batch_metadata(
            ...     "batch_123",
            ...     {
            ...         "experiment_id": "exp-001",
            ...         "version": 2,
            ...         "notes": "Test run with new model"
            ...     }
            ... )
        """
        # Validate metadata structure
        if not isinstance(metadata, dict):
            raise ValidationError("metadata must be a dictionary")

        for key, value in metadata.items():
            if not isinstance(key, str):
                raise ValidationError("All keys must be strings")
            if not isinstance(value, (str, int)):
                raise ValidationError("All values must be strings or integers (non-nested)")

        # Convert to JSON string
        metadata_str = json.dumps(metadata)

        # Call backend endpoint
        response = self.client._make_request(
            method="POST",
            endpoint=f"/api/batch/{batch_id}/metadata",
            json_data={"metadata": metadata_str}
        )

        return response.json()

    # ------------------------------------------------------------------
    # Semantic search across multiple videos
    # ------------------------------------------------------------------

    def search(
        self,
        *,
        query: str,
        folder_name: str,
        scope: FolderScopeLiteral = "user",
    ) -> Dict[str, Any]:
        """Search across videos in a folder for a natural language query.

        Args:
            query: Natural language search query.
            folder_name: Human-friendly folder name that the videos belong to.
            scope: Folder scope hint ("user", "org", or "sample").

        Returns:
            Dict containing summary, chain-of-thought entries, matches, and session metadata.

        Raises:
            NomadicMLError: For API errors or failed searches.
        """

        if not query or not query.strip():
            raise NomadicMLError("Search query cannot be empty")
        if not folder_name or not folder_name.strip():
            raise NomadicMLError("Folder name is required for search")

        scope_map = {
            "user": "my",
            "org": "org",
            "sample": "sample",
        }

        session_scope = scope_map.get(scope, "my")

        # 1) Initialize a search session so we can collect reasoning + results from Firestore
        start_payload = {
            "query": query,
            "folder_name": folder_name,
            "scope": session_scope,
        }

        start_resp = self.client._make_request(
            "POST",
            "/api/search-sessions/start",
            json_data=start_payload,
        )
        session_info = start_resp.json()
        session_id = session_info.get("session_id")
        owner_uid = session_info.get("owner_uid")
        session_doc_path = session_info.get("session_doc_path")
        reasoning_trace_path = session_info.get("reasoning_trace_path", session_doc_path)

        if not (session_id and owner_uid and session_doc_path):
            raise NomadicMLError("Failed to initialize search session")

        # 2) Trigger the backend search (writes results into the session document)
        form_data = {
            "query": query,
            "folder": folder_name,
            "session_id": session_id,
            "session_doc_path": session_doc_path,
            "reasoning_trace_path": reasoning_trace_path,
        }
        if session_scope == "sample":
            form_data["is_sample_videos"] = "true"

        # Remove empty values to avoid confusing FastAPI's Form parsing
        form_data = {k: v for k, v in form_data.items() if v}

        self.client._make_request(
            "POST",
            "/api/search",
            params={"folder_collection": session_scope},
            data=form_data,
        )

        # 3) Poll the session document until the search completes
        poll_endpoint = f"/api/search-sessions/{owner_uid}/{session_id}"
        started_at = time.time()
        delay = 1.0
        max_delay = 10.0

        while True:
            session_resp = self.client._make_request("GET", poll_endpoint)
            payload = session_resp.json()
            data = payload.get("data", {})
            status = (data.get("status") or "").lower()

            if status == "completed":
                raw_matches = data.get("matches") or []
                summary = data.get("summary") or ""
                thoughts = data.get("thoughts") or []

                normalized_matches: List[Dict[str, Any]] = []
                for entry in raw_matches:
                    if not isinstance(entry, dict):
                        continue
                    normalized_matches.append({
                        "video_id": entry.get("video_id"),
                        "analysis_id": entry.get("analysis_id"),
                        "event_index": entry.get("event_index"),
                        "similarity": entry.get("similarity"),
                        "reason": entry.get("reason", ""),
                    })

                return {
                    "summary": summary,
                    "thoughts": thoughts,
                    "matches": normalized_matches,
                    "session_id": session_id,
                }

            if status == "failed":
                error_message = data.get("error") or data.get("error_message") or "Search failed"
                raise NomadicMLError(error_message)

            elapsed = time.time() - started_at
            if elapsed > self.client.timeout:
                raise TimeoutError("Timed out waiting for search results")

            time.sleep(delay)
            delay = min(delay * 1.5, max_delay)

    ###############
    # ──────────────── Deprecated Methods ────────────────────────────────────────
    ###############

    def apply_search(self, parent_id: str, query: str,
                    model_id: str = "Nomadic-VL-XLarge") -> Dict[str, Any]:
        """
        DEPRECATED: This method has been removed.
        Use analyze() with analysis_type='rapid_review' instead.
        """
        raise NomadicMLError(
            "apply_search has been deprecated. Use analyze() with analysis_type='rapid_review' instead, "
            "which now supports all video lengths including long videos."
        )


    def _get_analysis_status(self, video_id: str, analysis_id: str) -> Dict[str, Any]:
        """Get the current status of a rapid review analysis."""
        params = {"collection": self.client.collection_name}
        r = self.client._make_request(
            "GET", f"/api/videos/{video_id}/analyses/{analysis_id}/status", params=params
        )
        if r.status_code >= 400:
            raise NomadicMLError(format_error_message(r.json()))
        return r.json()


    def _wait_for_rapid_review(self, video_id: str, analysis_id: str,
                              timeout: int = 3_600, poll_interval: int = 5,
                              is_thumbnail: bool = False) -> Dict[str, Any]:
        """Wait for a rapid review analysis to complete and return the final result."""
        start = time.time()
        while True:
            p = self._get_analysis_status(video_id, analysis_id)
            status = (p.get("status") or "").upper()
            
            # Calculate progress from either chunks ratio or progress field
            if p.get("chunks_completed") and p.get("chunks_total"):
                progress = (p.get("chunks_completed") / p.get("chunks_total")) * 100
            else:
                progress = float(p.get("progress", 0))
            
            self._print_status_bar(f"RapidReview:{analysis_id}",
                        percent=progress)
            
            if status == "COMPLETED":
                # Convert UI events back to RapidReviewEvent format
                ui_events = p.get("events", [])
                converted_events = []
                
                # Handle events that might be in UI format from Firebase
                for event in ui_events:
                    # Check if event is already in UI format (has 'type' and 'time' fields)
                    if isinstance(event, dict) and "type" in event and "time" in event:
                        # Convert from UI format to RapidReviewEvent format
                        converted_event = self._convert_ui_event_to_rapid_review(event)
                        if converted_event:
                            converted_events.append(self._ensure_overlay_defaults(converted_event))
                    else:
                        # Event might already be in correct format or different format
                        if isinstance(event, dict):
                            converted_events.append(self._ensure_overlay_defaults(dict(event)))
                        elif event is not None:
                            converted_events.append(event)
                
                # Handle answer field - could be string or array
                answer = p.get("answer", "")
                if isinstance(answer, list):
                    # Join array elements into a single string
                    answer = "\n".join(answer)
                
                # Fetch thumbnails if requested and events exist
                if is_thumbnail and converted_events:
                    try:
                        # Get thumbnails for all events
                        thumbnail_urls = self.get_visuals(video_id, analysis_id)
                        # Add thumbnail URLs to events if we got them
                        if thumbnail_urls and len(thumbnail_urls) == len(converted_events):
                            for i, event in enumerate(converted_events):
                                if isinstance(event, dict) and i < len(thumbnail_urls):
                                    event["annotated_thumbnail_url"] = thumbnail_urls[i]
                    except Exception as e:
                        logger.warning(f"Failed to fetch thumbnails: {e}")
                
                # Return the final result in the expected format
                return {
                    "answer": answer,
                    "suggested_events": converted_events,
                    "video_id": video_id,
                    "analysis_id": analysis_id,
                    "status": "completed"
                }
            if status == "FAILED":
                raise NomadicMLError(f"Rapid review analysis failed for {analysis_id}")
            if time.time() - start > timeout:
                raise TimeoutError(f"Rapid review {analysis_id} timed-out after {timeout}s")
            time.sleep(poll_interval)


    def my_videos(self, folder_id: str | None = None) -> List[Dict[str, Any]]:
        params = {
            "firebase_collection_name": self.client.collection_name,
            "folder_collection": self.client.folder_collection_name
        }
        if folder_id:
            params["folder"] = folder_id
        resp = self.client._make_request("GET", "/api/my-videos", params=params)
        return resp.json().get("videos", [])

    def delete_video(self, video_id: str) -> Dict[str, Any]:
        params = {"firebase_collection_name": self.client.collection_name}
        resp = self.client._make_request("DELETE", f"/api/video/{video_id}", params=params)
        return resp.json()
    

    # ─────────────────────── wait until status == UPLOADED ───────────── CHANGED
    def _wait_for_uploaded(self,
                           video_id: str,
                           timeout: int = 1200,
                           initial_delay: int = 15,
                           max_delay: int = 30,
                           multiplier: int = 2) -> None:
        """Block until video upload is finished.

        Handles both single videos and chunked uploads. When ``chunks_total`` is
        present in metadata, this waits until all chunks are reported as
        uploaded; otherwise it waits for ``visual_analysis.status.status`` to become
        ``UPLOADED``.
        """
        delay = initial_delay
        deadline = time.time() + timeout

        while True:
            payload = self.get_video_status(video_id)
            meta = payload.get("metadata", {})

            state = (self._status_from_metadata(meta) or "").upper()
            total = meta.get("chunks_total")
            uploaded = meta.get("chunks_uploaded", 0)

            if isinstance(total, int) and total > 0:
                if uploaded >= total:
                    logger.info(f"Upload completed for video {video_id}")
                    return
            elif state == "UPLOADED":
                logger.info(f"Upload completed for video {video_id}: status={state}")
                return

            if state in ("UPLOADING_FAILED", "FAILED"):
                raise VideoUploadError(f"Upload failed (backend status={state})")
            if time.time() > deadline:
                raise TimeoutError(f"Backend never reached UPLOADED in {timeout}s")

            sleep_for = max(0, delay + random.uniform(-1, 1))
            time.sleep(sleep_for)

            delay = min(delay * multiplier, max_delay)
            
    def upload_and_analyze(self,*args, **kwargs):
        raise NotImplementedError(
            "Deprecated: Use separate upload() and analyze() calls instead. "
            "See documentation for examples: https://docs.nomadicml.com/api-reference/sdk-examples"
        )

    def _status_from_metadata(self, meta: dict) -> Optional[str]:
        """
        Return the processing state stored in the scalar Firestore field
        `visual_analysis.status.status`.
        """
        return meta.get("visual_analysis", {}).get("status", {}).get("status")
    
    def get_visuals(self, video_id: str, analysis_id: str) -> List[str]:
        """
        Get all visual thumbnail URLs from an analysis.
        Automatically generates them if they don't exist.
        
        Args:
            video_id: The ID of the video
            analysis_id: The ID of the analysis
            
        Returns:
            List of thumbnail URLs for all events
        """
        # Call the generate-thumbnails endpoint which will:
        # 1. Check if thumbnails already exist
        # 2. Generate them if they don't
        # 3. Return all events with thumbnail URLs
        logger.info(f"Getting visuals for video {video_id}, analysis {analysis_id}")
        endpoint = f"/api/videos/{video_id}/analyses/{analysis_id}/generate-thumbnails"
        data = {"firebase_collection_name": self.client.collection_name}
        
        response = self.client._make_request(
            method="POST",
            endpoint=endpoint,
            data=data
        )
        
        result = response.json()
        events = result.get("events", [])
        
        if not events:
            logger.warning("No events found in analysis")
            return []
        
        thumbnail_urls = [event.get("annotated_thumbnail_url", "") for event in events]
        # Filter out any empty URLs
        thumbnail_urls = [url for url in thumbnail_urls if url]
        
        logger.info(f"Retrieved {len(thumbnail_urls)} thumbnail URLs")
        return thumbnail_urls
    
    def get_visual(self, video_id: str, analysis_id: str, event_idx: int) -> str:
        """
        Get a single visual thumbnail URL for a specific event.
        Automatically generates thumbnails if needed.

        Args:
            video_id: The ID of the video
            analysis_id: The ID of the analysis
            event_idx: The index of the event (0-based)

        Returns:
            Single thumbnail URL for the specified event

        Raises:
            ValueError: If the event index is out of range
        """
        visuals = self.get_visuals(video_id, analysis_id)

        if not visuals:
            raise ValueError(f"No visuals found for video {video_id}, analysis {analysis_id}")

        if event_idx < 0 or event_idx >= len(visuals):
            raise ValueError(
                f"Event index {event_idx} out of range. "
                f"Valid range: 0-{len(visuals)-1}"
            )

        return visuals[event_idx]

    def create_agent(
        self,
        name: str,
        batch_ids: List[str] = [],
        analysis_ids: List[str] = [],
        wait_for_completion: bool = False,
    ) -> Dict[str, Any]:
        """
        Create a fine-tuned agent using batch analysis data.

        Args:
            batch_ids: List of batch IDs to use as training data
            name: Name for the agent being created
            wait_for_completion: Whether to wait for the optimization job to complete (default: False)

        Raises:
            NomadicMLError: If the API request fails
            AuthenticationError: If user is not an admin
            ValidationError: If any batch has insufficient approved or rejected events

        Example:
            >>> client = NomadicML(api_key="your_api_key")
            >>> result = client.video.create_agent(
            ...     batch_ids=["batch_123", "batch_456"],
            ...     name="My Lane Change Agent",
            ...     wait_for_completion=False
            ... )
            >>> print(f"Agent training job started: {result['job_id']}")
        """
        if not batch_ids and not analysis_ids:
            raise ValueError("At least one batch_id or analysis_id must be provided")

        if not name or not name.strip():
            raise ValueError("Agent name must be provided and cannot be empty")

        # Generate idempotency key for this request (same pattern as client._make_request)
        # This ensures retries of the same request will use the same agent_id
        idempotency_key = str(uuid.uuid4())

        payload = {
            "batch_ids": batch_ids,
            "analysis_ids": analysis_ids,
            "name": name,
            "wait_for_completion": wait_for_completion,
            "client_agent_id": idempotency_key,  # Pass idempotency key as agent ID
        }

        logger.info(f"Creating agent from {len(batch_ids)} batch(es) and {len(analysis_ids)} analysis(es) with client_agent_id={idempotency_key}")

        response = self.client._make_request(
            method="POST",
            endpoint="/api/create-agent",
            json_data=payload,
            timeout=10_800,  # 3 hours
        )

        if not (200 <= response.status_code < 300):
            raise NomadicMLError(
                f"Failed to create agent: {format_error_message(response.json())}"
            )

        result = response.json()
        logger.info(f"Agent training job submitted: {result.get('job_id')}")

        return result

    def update_agent(
        self,
        agent_id: str,
        batch_ids: List[str] = [],
        analysis_ids: List[str] = [],
        wait_for_completion: bool = False,
    ) -> Dict[str, Any]:
        """
        Update an existing agent with additional training data.

        Args:
            agent_id: ID of the agent to update
            batch_ids: List of batch IDs to add as training data
            analysis_ids: List of analysis IDs (format: "video_id:analysis_id") to add as training data

        Returns:
            Dictionary containing:
                - agent_id: ID of the updated agent
                - update_type: "prompt_optimization" or "finetuning"
                - total_approved: Total count of approved events
                - total_rejected: Total count of rejected events
                - Other job-specific information

        Raises:
            NomadicMLError: If the API request fails
            AuthenticationError: If user is not an admin
            ValidationError: If agent not found or duplicate IDs provided

        Example:
            >>> client = NomadicML(api_key="your_api_key")
            >>> result = client.video.update_agent(
            ...     agent_id="agent_abc123",
            ...     batch_ids=["batch_789"],
            ... )
            >>> print(f"Agent updated with {result['update_type']}")
        """
        if not agent_id or not agent_id.strip():
            raise ValueError("Agent ID must be provided and cannot be empty")

        if not batch_ids and not analysis_ids:
            raise ValueError("At least one batch_id or analysis_id must be provided")

        # Generate idempotency key for this update operation
        # This ensures retries of the same request will not spawn duplicate jobs
        client_update_id = str(uuid.uuid4())

        payload = {
            "agent_id": agent_id,
            "batch_ids": batch_ids,
            "analysis_ids": analysis_ids,
            "wait_for_completion": wait_for_completion,
            "client_update_id": client_update_id,
        }

        logger.info(f"Updating agent {agent_id} with {len(batch_ids)} batch(es) and {len(analysis_ids)} analysis(es) with client_update_id={client_update_id}")

        response = self.client._make_request(
            method="POST",
            endpoint="/api/update-agent",
            json_data=payload,
            timeout=10_800,  # 3 hours
        )

        if not (200 <= response.status_code < 300):
            raise NomadicMLError(
                f"Failed to update agent: {format_error_message(response.json())}"
            )

        result = response.json()
        logger.info(f"Agent update job submitted: update_type={result.get('update_type')}")

        return result

    def list_agents(
        self,
        scope: str = "user",
    ) -> List[Dict[str, Any]]:
        """
        List all agents for the authenticated user or organization.

        Args:
            scope: Scope for listing agents - either "user" or "org"
                  - "user": List agents created by the authenticated user
                  - "org": List agents created by any user in the same organization

        Returns:
            List of agent dictionaries, each containing:
                - agent_id: The unique ID of the agent
                - name: The name of the agent
                - status: The current status of the agent

        Raises:
            NomadicMLError: If the API request fails
            AuthenticationError: If user is not an admin
            ValidationError: If scope is invalid

        Example:
            >>> client = NomadicML(api_key="your_api_key")
            >>> # List user's own agents
            >>> my_agents = client.video.list_agents(scope="user")
            >>> print(f"Found {len(my_agents)} agents")
            >>>
            >>> # List all agents in the organization
            >>> org_agents = client.video.list_agents(scope="org")
            >>> for agent in org_agents:
            ...     print(f"{agent['name']}: {agent['status']}")
        """
        if scope not in ["user", "org"]:
            raise ValueError("scope must be either 'user' or 'org'")

        payload = {"scope": scope}

        logger.info(f"Listing agents with scope={scope}")

        response = self.client._make_request(
            method="POST",
            endpoint="/api/list-agents",
            json_data=payload,
        )

        if not (200 <= response.status_code < 300):
            raise NomadicMLError(
                f"Failed to list agents: {format_error_message(response.json())}"
            )

        result = response.json()
        agents = result.get("agents", [])
        logger.info(f"Listed {len(agents)} agents for scope={scope}")

        return agents
DEFAULT_STRUCTURED_ODD_COLUMNS: List[StructuredOddColumn] = [
    {
        "name": "timestamp",
        "prompt": (
            'Log the timestamp in full ISO 8601 format. Since the video does not contain an absolute date, '
            'you MUST use the placeholder date "2024-01-01". Append the time from the video (e.g., "HH:MM:SS"). '
            'The final format must be, for example: "2024-01-01T14:32:15Z".'
        ),
        "type": "YYYY-MM-DDTHH:MM:SSZ",
        "literals": [],
    },
    {
        "name": "comment",
        "prompt": (
            'Brief summary of the significant change (e.g., "Car merges into ego lane"). Format: Use only letters, '
            "numbers, spaces, and hyphens. No punctuation, commas, quotes, or line breaks. Rephrase comments containing "
            "prohibited characters."
        ),
        "type": "string",
        "literals": [],
    },
    {
        "name": "scenery.road.type",
        "prompt": "The type of road the vehicle is on.",
        "type": "categorical",
        "literals": ["motorway", "rural", "urban_street", "parking_lot", "unpaved", "unknown"],
    },
    {
        "name": "scenery.road.number_of_lanes",
        "prompt": "The total number of lanes in the direction of travel.",
        "type": "integer",
        "literals": [],
    },
    {
        "name": "scenery.road.lane_marking_type",
        "prompt": "The condition and type of lane markings visible for the ego-lane.",
        "type": "categorical",
        "literals": ["clear", "blurred", "temporary_yellow", "none", "unknown"],
    },
    {
        "name": "scenery.road.surface_condition",
        "prompt": "The condition of the road surface.",
        "type": "categorical",
        "literals": ["dry", "wet", "icy", "snow_covered", "leaves_debris", "potholes", "uneven", "unknown"],
    },
    {
        "name": "scenery.road.grade_category",
        "prompt": "The estimated slope of the road.",
        "type": "categorical",
        "literals": ["level", "slight_incline", "steep_incline", "slight_decline", "steep_decline", "unknown"],
    },
    {
        "name": "scenery.road.speed_limit",
        "prompt": "The posted speed limit visible on signs. Log as an integer. Leave blank if no sign is visible.",
        "type": "km/h",
        "literals": [],
    },
    {
        "name": "scenery.road.is_construction_zone",
        "prompt": '"true" if there are visible signs of a construction zone (e.g., cones, barriers, specific signs), otherwise "false".',
        "type": "boolean",
        "literals": [],
    },
    {
        "name": "scenery.junction.type",
        "prompt": "The type of intersection ahead or currently in.",
        "type": "categorical",
        "literals": ["none", "t_junction", "four_way", "roundabout", "merge_lane", "exit_lane", "unknown"],
    },
    {
        "name": "scenery.junction.traffic_control",
        "prompt": "The primary traffic control method at the junction.",
        "type": "categorical",
        "literals": ["none", "traffic_light", "stop_sign", "yield_sign", "uncontrolled", "unknown"],
    },
    {
        "name": "scenery.junction.is_signalized",
        "prompt": (
            '"true" if the junction is controlled by traffic lights, "false" otherwise. This is a specific subset of '
            '"traffic_control". Note: If scenery.junction.traffic_control is "traffic_light", then scenery.junction.is_signalized '
            'MUST be "true". If traffic_control is any other value, is_signalized MUST be "false".'
        ),
        "type": "boolean",
        "literals": [],
    },
    {
        "name": "scenery.participants.pedestrian.count",
        "prompt": "The total count of pedestrians visible in or near the drivable area.",
        "type": "integer",
        "literals": [],
    },
    {
        "name": "scenery.participants.cyclist.count",
        "prompt": "The total count of cyclists (bicycles, e-scooters) visible in or near the drivable area.",
        "type": "integer",
        "literals": [],
    },
    {
        "name": "scenery.participants.car.count",
        "prompt": "The total count of passenger cars visible.",
        "type": "integer",
        "literals": [],
    },
    {
        "name": "scenery.participants.truck.count",
        "prompt": "The total count of trucks, buses, or large commercial vehicles visible.",
        "type": "integer",
        "literals": [],
    },
    {
        "name": "scenery.participants.emergency_vehicle.is_present",
        "prompt": '"true" if an emergency vehicle (police, ambulance, fire truck) with or without active sirens/lights is visible, "false" otherwise.',
        "type": "boolean",
        "literals": [],
    },
    {
        "name": "environment.weather.precipitation_type",
        "prompt": "The type of precipitation.",
        "type": "categorical",
        "literals": ["none", "rain", "snow", "hail", "sleet"],
    },
    {
        "name": "environment.weather.precipitation_intensity",
        "prompt": "The intensity of the precipitation.",
        "type": "categorical",
        "literals": ["none", "light", "moderate", "heavy", "violent"],
    },
    {
        "name": "environment.weather.fog_density",
        "prompt": "The density of fog or mist affecting visibility.",
        "type": "categorical",
        "literals": ["none", "light", "moderate", "dense"],
    },
    {
        "name": "environment.weather.is_sun_glare",
        "prompt": '"true" if direct sun glare is visible and potentially impacting sensors, otherwise "false".',
        "type": "boolean",
        "literals": [],
    },
    {
        "name": "environment.weather.lighting_condition",
        "prompt": "The overall lighting of the scene.",
        "type": "categorical",
        "literals": ["daylight", "dusk_dawn", "night_well_lit", "night_unlit", "tunnel"],
    },
]
