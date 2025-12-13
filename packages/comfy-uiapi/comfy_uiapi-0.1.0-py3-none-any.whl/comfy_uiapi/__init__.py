"""
comfy-uiapi: Python client for ComfyUI-uiapi

Provides programmatic control of ComfyUI workflows via the uiapi extension.

Usage:
    from comfy_uiapi import ComfyClient, ModelDef

    client = ComfyClient("127.0.0.1:8188")
    client.ensure_connection()
    client.set("prompt.text", "a beautiful landscape")
    result = client.execute()
"""

from .client import ComfyClient, ComfyConnectionError
from .model_defs import ModelDef, ControlNetDef, LoraDef, VaeDef

__all__ = [
    "ComfyClient",
    "ComfyConnectionError",
    "ModelDef",
    "ControlNetDef",
    "LoraDef",
    "VaeDef",
]

__version__ = "0.1.0"
