# comfy-uiapi

Python client for [ComfyUI-uiapi](https://github.com/oxysoft/ComfyUI-uiapi) - programmatic control of ComfyUI workflows.

## Installation

```bash
pip install comfy-uiapi
```

Or for development:

```bash
pip install -e /path/to/comfy-uiapi-client
```

## Quick Start

```python
from comfy_uiapi import ComfyClient

# Connect to ComfyUI with uiapi extension
client = ComfyClient("127.0.0.1:8188")
client.ensure_connection()

# Set workflow fields
client.set("prompt.text", "a beautiful landscape, photorealistic")
client.set("ksampler.seed", 42)
client.set("ksampler.steps", 20)

# Execute and get result
result = client.execute()  # Returns numpy array (RGB)
```

## Two Execution Modes

### 1. WebUI Mode (default)

Manipulates the workflow graph in the browser via uiapi:

```python
client = ComfyClient("127.0.0.1:8188")
client.require_webui = True  # default

client.set("prompt.text", "hello world")
result = client.execute()
```

Requires: Browser with ComfyUI WebUI open and connected.

### 2. Workflow API Mode

Posts JSON workflow directly to `/prompt` endpoint - no browser needed:

```python
import json

# Load workflow JSON (exported from ComfyUI)
with open("workflow_api.json") as f:
    workflow = json.load(f)

client = ComfyClient("127.0.0.1:8188")
client.require_webui = False

# Execute with field overrides
result = client.execute_workflow(
    workflow,
    fields=[
        ("prompt.text", "a cat in space"),
        ("ksampler.seed", 123),
    ]
)
```

## Model Downloads

```python
from comfy_uiapi import ComfyClient, ModelDef

client = ComfyClient("127.0.0.1:8188")

models = {
    "sd_xl_base_1.0.safetensors": ModelDef(
        huggingface="stabilityai/stable-diffusion-xl-base-1.0"
    ),
    "my_lora.safetensors": ModelDef(
        civitai="https://civitai.com/api/download/models/12345"
    ),
}

client.download_models(models)
```

## Async API

All methods have async variants:

```python
import asyncio
from comfy_uiapi import ComfyClient

async def main():
    client = ComfyClient("127.0.0.1:8188")
    await client.ensure_connection_async()
    await client.set_async("prompt.text", "async generation")
    result = await client.execute_async()

asyncio.run(main())
```

## License

MIT
