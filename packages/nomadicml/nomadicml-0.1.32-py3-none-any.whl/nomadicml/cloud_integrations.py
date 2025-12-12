"""
Cloud integration helpers for the NomadicML SDK.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Literal, Mapping, Optional, Sequence, TypedDict, Union, TYPE_CHECKING

from .exceptions import NomadicMLError, ValidationError

if TYPE_CHECKING:
    from .client import NomadicML


class CloudIntegration(TypedDict, total=False):
    """Shape returned by the cloud integrations API."""

    id: str
    name: str
    type: Literal["gcs", "s3"]
    bucket: str
    prefix: str | None
    region: str | None
    created_at: str
    last_used: str | None
    created_by: str
    created_by_display_name: str | None
    is_owner: bool


CredentialsInput = Union[Mapping[str, Any], str, Path, bytes]


class CloudIntegrationsClient:
    """Thin wrapper around the backend's cloud integration endpoints."""

    def __init__(self, client: "NomadicML"):
        self._client = client

    # ──────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────
    def list(
        self,
        *,
        type: Literal["gcs", "s3", None] = None,
    ) -> List[CloudIntegration]:
        """
        Return all integrations visible to the caller.

        When ``type`` is provided, results are filtered client-side.
        """
        response = self._client._make_request("GET", "/api/cloud-integrations")
        payload = response.json()

        if not isinstance(payload, list):
            raise NomadicMLError("Unexpected response from /api/cloud-integrations.")

        integrations: List[CloudIntegration] = []
        for item in payload:
            if isinstance(item, dict):
                integrations.append(item)  # type: ignore[list-item]

        if type:
            integrations = [item for item in integrations if item.get("type") == type]

        return integrations

    def add(
        self,
        *,
        type: Literal["gcs", "s3"],
        name: str,
        bucket: str,
        credentials: CredentialsInput,
        prefix: str | None = None,
        region: str | None = None,
    ) -> CloudIntegration:
        """
        Persist a new cloud integration and return its metadata.

        Args:
            type: ``"gcs"`` or ``"s3"``.
            name: Human-friendly label for the integration.
            bucket: Bucket name to associate with the integration.
            credentials: Credential payload (mapping, JSON string, bytes, or path).
            prefix: Optional prefix to scope the integration.
            region: Required when ``type="s3"``.
        """
        integration_type = type.lower()
        if integration_type not in {"gcs", "s3"}:
            raise ValidationError("type must be either 'gcs' or 's3'.")

        if not name or not name.strip():
            raise ValidationError("Integration name cannot be empty.")
        if not bucket or not bucket.strip():
            raise ValidationError("Bucket name cannot be empty.")

        if integration_type == "gcs":
            endpoint = "/api/cloud-integrations/gcs"
            service_account = self._coerce_credentials(credentials)
            payload: Dict[str, Any] = {
                "name": name.strip(),
                "type": "gcs",
                "service_account": service_account,
                "bucket": bucket.strip(),
                "prefix": prefix,
            }
        else:
            if not region or not region.strip():
                raise ValidationError("region is required for S3 integrations.")

            creds_mapping = self._coerce_credentials(credentials)
            normalized = {self._normalize_credential_key(k): v for k, v in creds_mapping.items()}

            access_key = normalized.get("access_key_id") or normalized.get("accesskeyid")
            secret_key = normalized.get("secret_access_key") or normalized.get("secretaccesskey")

            if access_key is None:
                raise ValidationError(
                    "Missing required S3 credential field: access_key_id/accessKeyId."
                )
            if secret_key is None:
                raise ValidationError(
                    "Missing required S3 credential field: secret_access_key/secretAccessKey."
                )

            session_token = (
                normalized.get("session_token")
                or normalized.get("sessiontoken")
            )

            endpoint = "/api/cloud-integrations/s3"
            payload = {
                "name": name.strip(),
                "type": "s3",
                "access_key_id": access_key,
                "secret_access_key": secret_key,
                "session_token": session_token,
                "region": region.strip(),
                "bucket": bucket.strip(),
                "prefix": prefix,
            }

        response = self._client._make_request("POST", endpoint, json_data=payload)
        data = response.json()
        if not isinstance(data, dict):
            raise NomadicMLError("Unexpected response when creating cloud integration.")

        return data  # type: ignore[return-value]

    # ──────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────
    def _coerce_credentials(self, credentials: CredentialsInput) -> Dict[str, Any]:
        """Normalize credentials input into a JSON-friendly mapping."""
        if isinstance(credentials, Mapping):
            # Convert keys to strings for consistency
            return {str(k): v for k, v in credentials.items()}

        if isinstance(credentials, bytes):
            try:
                return json.loads(credentials.decode("utf-8"))
            except json.JSONDecodeError as exc:
                raise ValidationError("Unable to decode credential bytes as JSON.") from exc

        if isinstance(credentials, (str, Path)):
            path = credentials.expanduser() if isinstance(credentials, Path) else Path(credentials).expanduser()
            text: Optional[str] = None
            if isinstance(credentials, Path) or path.exists():
                try:
                    text = path.read_text()
                except OSError as exc:
                    raise ValidationError(f"Failed to read credential file: {exc}") from exc
            else:
                text = str(credentials)

            try:
                return json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValidationError("Credential string could not be parsed as JSON.") from exc

        raise ValidationError(
            "credentials must be a mapping, JSON string/path, or bytes payload."
        )

    @staticmethod
    def _normalize_credential_key(key: Any) -> str:
        """Best-effort normalization for credential dict keys."""
        key_str = str(key)
        key_str = key_str.replace("-", "_").replace(" ", "_")
        return key_str.lower()
