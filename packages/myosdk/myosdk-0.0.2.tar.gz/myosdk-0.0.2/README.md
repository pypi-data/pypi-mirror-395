# MyoSapiens Python SDK (MyoSDK)

A lightweight Python client for the MyoSapiens API.

## Installation

```bash
pip install myosdk
```

## Quick Start

### Prerequisites
Before installing the SDK, ensure you have:

- **Python 3.10+**
- **A MyoSapiens API key**, available at  [dev.myolab.ai](dev.myolab.ai)

### Basic Usage
``` python
from myosdk import Client

client = Client(api_key="ak_live_xxx")

# Upload a C3D motion capture file
c3d_asset = client.assets.upload_file(<c3d_path>)

# Upload markerset XML file
markerset_asset = client.assets.upload_file(<markerset_path>)

# Run tracking
job = client.jobs.start_retarget(
    c3d_asset_id=c3d_asset["asset_id"],
    markerset_asset_id=markerset_asset["asset_id"],
)

# Wait for completion
result = client.jobs.wait(job["job_id"])

# Download the resulting joint angles and joint names(.npz)
joint_angle_asset_id = result["output"]["retarget_output_asset_id"]
client.assets.download(joint_angle_asset_id, <output_npy_path>)
```

## Examples and Tutorials
See examples and tutorials at [https://github.com/myolab/myosdk_tutorials](https://github.com/myolab/myosdk_tutorials)

## SDK Documentation
Full SDK and API documentation is available at [docs.myolab.ai](docs.myolab.ai).