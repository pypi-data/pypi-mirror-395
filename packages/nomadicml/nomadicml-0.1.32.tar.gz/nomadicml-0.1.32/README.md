# NomadicML Python SDK

A Python client library for the NomadicML DriveMonitor API, allowing you to upload and analyze driving videos programmatically.

## Installation

### From PyPI (for users)

```bash
pip install nomadicml
```

### For Development (from source)

To install the package in development mode, where changes to the code will be immediately reflected without reinstallation:

```bash
# Clone the repository
git clone https://github.com/nomadic-ml/drivemonitor.git
cd sdk

# For development: Install in editable mode
pip install -e .
```

With this installation, any changes you make to the code will be immediately available when you import the package.

## Quick Start

```python
from nomadicml import NomadicML

# Initialize the client with your API key
client = NomadicML(api_key="your_api_key")

# Upload a video and analyze it in one step
result = client.video.upload_and_analyze("path/to/your/video.mp4")

# Print the detected events
for event in result["events"]:
    print(f"Event: {event['type']} at {event['time']}s - {event['description']}")
#For a batch upload

videos_list = [.....]#list of video paths
batch_results = client.video.upload_and_analyze_videos(videos_list, wait_for_completion=False)

    
video_ids = [
    res.get("video_id")
    for res in batch_results
    if res                                         # safety for None
    ]

    
full_results = client.video.wait_for_analyses(video_ids)

```

## Authentication

You need an API key to use the NomadicML API. You can get one by:

1. Log in to your DriveMonitor account
2. Go to Profile > API Key
3. Generate a new API key

Then use this key when initializing the client:

```python
client = NomadicML(api_key="your_api_key")
```

## Video Upload and Analysis

### Upload a video

```python
# Preferred: upload with the high-level helper
upload_result = client.video.upload(
    "path/to/video.mp4",
    metadata_file="path/to/overlay_schema.json",  # optional
    wait_for_uploaded=True,
)
video_id = upload_result["video_id"]

# Legacy helpers remain available if you need fine-grained control
result = client.video.upload_video(
    source="file",
    file_path="path/to/video.mp4"
)
```

The `metadata_file` argument is optional and accepts any of the following:

- Path to a JSON metadata file describing per-frame overlay fields
- A Python `dict` that can be serialised to the Nomadic overlay schema
- Raw JSON string or UTF-8 bytes containing the schema

When provided, the SDK sends the schema to `/api/upload-video` so the backend
can extract on-screen telemetry (timestamps, GPS, speed, etc.) during later
analyses. If you specify `metadata_file` while uploading multiple videos at
once, the SDK will raise a `ValidationError`—attach metadata on single uploads
only.

### Upload videos stored in Google Cloud Storage

You can import `.mp4` objects directly from GCS once you have saved their
credentials as a cloud integration:

```python
# Trigger imports without re-downloading files locally
upload_result = client.video.upload([
    "gs://drive-monitor/uploads/trip-042/video_front.mp4",
    "gs://drive-monitor/uploads/trip-042/video_rear.mp4",
],
    folder="Fleet Library",
    wait_for_uploaded=False,    # async import – poll later if you prefer
)

# Provide an explicit integration id when you have multiple saved credentials
upload_result = client.video.upload([
    "gs://drive-monitor/uploads/trip-042/video_front.mp4",
],
    integration_id="gcs_int_123",
)
```

Rules for the GCS path:

- Only `.mp4` objects are accepted today.
- All URIs within a single call must share the same bucket.
- Pass either a single string or a list of literal blob URIs—wildcards are not
  supported.
- If you omit `integration_id`, the SDK tries each saved integration whose
  bucket matches the URI until one succeeds. Provide the id explicitly when multiple
  integrations share the bucket.

To discover the ids you have already saved (for example, those created through
the DriveMonitor UI) call:

```python
for item in client.cloud_integrations.list(type="gcs"):
    print(item["name"], item["bucket"], item["id"])
```

### Analyze a video

```python
from nomadicml.video import AnalysisType, CustomCategory

analysis = client.video.analyze(
    video_id,
    analysis_type=AnalysisType.ASK,
    custom_event="Did the driver stop before the crosswalk?",
    custom_category=CustomCategory.DRIVING,
    overlay={"timestamps": True, "gps": True},  # optional OCR flags
)

events = analysis.get("events", [])
```

Overlay extraction is controlled via the optional `overlay` dictionary:

- `timestamps=True` enables OCR of on-screen frame timestamps.
- `gps=True` adds latitude/longitude extraction (timestamps are implied).
- `custom=True` activates Nomadic overlay mode, instructing the backend to use
  any supplied metadata schema for full telemetry capture. This also implies
  `timestamps=True`.

Each event returned by the SDK now includes an `overlay` dictionary. Overlay
entries are keyed by the field name (for example `frame_timestamp`,
`frame_speed`, etc.) and map to `{"start": ..., "end": ...}` pairs with the
values that were read from the video frames or metadata.

### Generate an ASAM OpenODD CSV

The client exposes a top-level helper, `client.generate_structured_odd(...)`,
that mirrors the DriveMonitor UI workflow and accepts the same column schema.
You can reuse the SDK’s built-in `DEFAULT_STRUCTURED_ODD_COLUMNS` constant or
pass your own list of definitions.

```python
from nomadicml import NomadicML, DEFAULT_STRUCTURED_ODD_COLUMNS

client = NomadicML(api_key="your_api_key")

# Optionally customise the column schema before calling the export.
columns = [
    {
        "name": "timestamp",
        "prompt": "Log the timestamp in ISO 8601 format (placeholder date 2024-01-01).",
        "type": "YYYY-MM-DDTHH:MM:SSZ",
    },
    {
        "name": "scenery.road.type",
        "prompt": "The type of road the vehicle is on.",
        "type": "categorical",
        "literals": ["motorway", "rural", "urban_street", "parking_lot", "unpaved", "unknown"],
    },
    # ...add or tweak additional columns...
]

odd = client.generate_structured_odd(
    video_id="VIDEO_ID_FROM_UPLOAD",
    columns=columns or DEFAULT_STRUCTURED_ODD_COLUMNS,
)

csv_text = odd["csv"]
share_url = odd.get("share_url")
print(csv_text.splitlines()[0])  # Header row
```

If you customise the schema in the DriveMonitor UI, use the **Copy SDK snippet**
button to paste a ready-made Python snippet that mirrors the on-screen column
configuration. The SDK automatically mirrors the Firestore reasoning trace path
and returns any generated share links together with the CSV data.

### Upload and analyze in one step

```python
# Upload and analyze a video, waiting for results
analysis = client.video.upload_and_analyze("path/to/video.mp4")

# Or just start the process without waiting
result = client.video.upload_and_analyze("path/to/video.mp4", wait_for_completion=False)
```

## Advanced Usage

### Filter events by severity or type

```python
# Get only high severity events
high_severity_events = client.video.get_video_events(
    video_id=video_id,
    severity="high"
)

# Get only traffic violation events
traffic_violations = client.video.get_video_events(
    video_id=video_id,
    event_type="Traffic Violation"
)
```

### Custom timeout and polling interval

```python
# Wait for analysis with a custom timeout and polling interval
client.video.wait_for_analysis(
    video_id=video_id,
    timeout=1200,  # 20 minutes
    poll_interval=10  # Check every 10 seconds
)
```

### Batch analyses across many videos

When you provide a list of video IDs to `client.video.analyze(...)`, the SDK now
creates a backend batch automatically (for both Asking Agent and Edge Agent
pipelines) and keeps polling the `/batch/{batch_id}/status` endpoint until the
orchestrator finishes. The return value is a dictionary with two keys:

* `batch_metadata` — contains the `batch_id`, a fully-qualified
  `batch_viewer_url` pointing at the Batch Results Viewer, and a
  `batch_type` flag (`"ask"` or `"agent"`).
* `results` — the list of per-video analysis dictionaries (exactly the same
  schema you would get from calling `analyze()` on a single video).

### Manage cloud integrations

The SDK exposes a dedicated helper to manage saved cloud credentials:

```python
# List every integration visible to your user/org
integrations = client.cloud_integrations.list()

# Filter by provider (either "gcs" or "s3")
gcs_only = client.cloud_integrations.list(type="gcs")

# Add a new S3 integration using AWS keys
client.cloud_integrations.add(
    type="s3",
    name="AWS archive",
    bucket="drive-archive",
    prefix="raw/",
    region="us-east-1",
    credentials={
        "accessKeyId": "...",
        "secretAccessKey": "...",
        "sessionToken": "...",  # optional
    },
)
```

Once an integration exists, you only need its `id` when pulling files directly
from the bucket. Call `client.upload("gs://bucket/path.mp4", integration_id="...")`
or `client.upload("s3://bucket/path.mp4", integration_id="...")` and the SDK
will hand the request to the correct backend importer. Credentials are never
embedded in the upload request body.

## BEFORE DEPLOYIN RUN THIS: Running SDK integration tests locally

The integration suite is tagged with `calls_api` and exercises the live backend
endpoints. Make sure you have a valid API key and a backend domain reachable
from your environment, then run:

```bash
cd sdk
export NOMADICML_API_KEY=YOUR_API_KEY
export VITE_BACKEND_DOMAIN=http://127.0.0.1:8099
python -u -m pytest -m calls_api -vvs -rPfE --durations=0 --capture=no tests/test_integration.py
```

The command disables pytest's output capture so you can follow streaming logs
while the long-running tests execute.

```python
from nomadicml.video import AnalysisType, CustomCategory

batch = client.video.analyze(
    ["video_1", "video_2", "video_3"],
    analysis_type=AnalysisType.ASK,
    custom_event="Did the driver stop before the crosswalk?",
    custom_category=CustomCategory.DRIVING,
)

print(batch["batch_metadata"])
for item in batch["results"]:
    print(item["video_id"], item["analysis_id"], len(item.get("events", [])))
```

### Custom API endpoint

If you're using a custom deployment of the DriveMonitor backend:

```python
# Connect to a local or custom deployment
client = NomadicML(
    api_key="your_api_key",
    base_url="http://localhost:8099"
)
```

### Search across videos

Run a semantic search on several of your videos at once:

```python
results = client.video.search(
    "red pickup truck overtaking",
    ["vid123", "vid456"]
)
for match in results["matches"]:
    print(match["videoId"], match["eventIndex"], match["similarity"])
```

## Error Handling

The SDK provides specific exceptions for different error types:

```python
from nomadicml import NomadicMLError, AuthenticationError, VideoUploadError

try:
    client.video.upload_and_analyze("path/to/video.mp4")
except AuthenticationError:
    print("API key is invalid or expired")
except VideoUploadError as e:
    print(f"Failed to upload video: {e}")
except NomadicMLError as e:
    print(f"An error occurred: {e}")
```

## Development

### Setup

Clone the repository and install development dependencies:

```bash
git clone https://github.com/nomadicml/nomadicml-python.git
cd nomadicml-python
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

## License

MIT License. See LICENSE file for details.
