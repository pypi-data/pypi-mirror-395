"""
ComfyUI-uiapi client for programmatic workflow control.

This client communicates with ComfyUI via the uiapi extension, enabling:
- Field get/set operations on the WebUI graph
- Workflow execution with result retrieval
- Model downloading orchestration
- Direct workflow API execution (without WebUI)

Two execution modes:
1. WebUI mode (require_webui=True): Manipulates the browser's graph via uiapi
2. Workflow API mode: Posts JSON workflow directly to /prompt endpoint
"""

from __future__ import annotations

import asyncio
import base64
import io
import json
import logging
import math
import threading
import time
import urllib.parse
import uuid
from collections.abc import Mapping
from typing import Any, BinaryIO, TypedDict, cast

import aiofiles
import cv2
import httpx
import numpy as np
from PIL import Image
from websockets.asyncio.client import connect

from .model_defs import ModelDef

log = logging.getLogger(__name__)

PNG_MAGIC_BYTES = b"\x89PNG\r\n\x1a\n"


# Type definitions
# ----------------------------------------
class ImageInfo(TypedDict):
    filename: str
    subfolder: str
    type: str


class UploadResponse(TypedDict):
    name: str
    subfolder: str
    type: str


class WorkflowResponse(TypedDict):
    prompt_id: str


class HistoryOutput(TypedDict):
    images: list[ImageInfo]


class HistoryData(TypedDict):
    outputs: dict[str, HistoryOutput]


class ExecutionResult(TypedDict):
    prompt_id: str
    outputs: dict[str, list[np.ndarray]]
    history: HistoryData


class ComfyConnectionError(ConnectionError):
    """Raised when the ComfyUI server cannot be reached."""

    pass


# Utilities
# ----------------------------------------
def is_image(value: Any) -> bool:
    """Check if a value is an image type we can handle"""
    if isinstance(value, (np.ndarray, Image.Image)):
        return True
    try:
        import torch

        if isinstance(value, torch.Tensor):
            return True
    except ImportError:
        pass
    return False


def clamp01(v: float) -> float:
    """Clamp value to [0, 1] range"""
    return min(max(v, 0), 1)


def encode_image_to_base64(image: Image.Image | np.ndarray) -> str:
    """Convert various image types to base64 string"""
    if isinstance(image, Image.Image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    elif isinstance(image, np.ndarray):
        if image.dtype in [np.float32, np.float64]:
            image = (image * 255).astype(np.uint8)
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        success, buffer = cv2.imencode(".png", image)
        if not success:
            raise ValueError("Failed to encode image")
        return base64.b64encode(buffer.tobytes()).decode()
    else:
        raise ValueError(f"Unsupported image type: {type(image)}")


class ComfyClient:
    """
    Client for ComfyUI-uiapi extension.

    Provides both sync and async APIs for workflow control.

    Args:
        server_address: ComfyUI server address (default: "127.0.0.1:8188")

    Example:
        client = ComfyClient("127.0.0.1:8188")
        client.ensure_connection()
        client.set("prompt.text", "a beautiful landscape")
        result = client.execute()
    """

    def __init__(self, server_address: str = "127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self._webui_ready = False
        self._connection_lock: asyncio.Lock | None = None  # Lazy-init in async context
        self._reconnect_backoff = 1.0
        self._sync_lock = threading.Lock()
        self.require_webui = True
        self.workflow: dict | None = None
        self.workflow_fields: dict[str, Any] = {}

        log.info(f"ComfyClient initialized @ {server_address} (id={self.client_id[:8]})")

    # Connection Management
    # ----------------------------------------
    def _get_connection_lock(self) -> asyncio.Lock:
        """Lazy-init connection lock (must be created in async context)"""
        if self._connection_lock is None:
            self._connection_lock = asyncio.Lock()
        return self._connection_lock

    def ensure_connection(self, require_webui: bool | None = None, loop: bool = True) -> bool:
        """Ensure both HTTP and WebSocket connections are alive (sync)"""
        return self.run_sync(self.ensure_connection_async(require_webui=require_webui, loop=loop))

    async def connect_ws(self, timeout: float = 10):
        """Establish WebSocket connection"""
        ws_url = f"ws://{self.server_address}/ws?clientId={self.client_id}"
        return connect(ws_url, open_timeout=timeout)

    async def ensure_connection_async(self, require_webui: bool | None = None, loop: bool = True) -> bool:
        """Ensure both HTTP and WebSocket connections are alive (async)"""
        require_webui = require_webui if require_webui is not None else self.require_webui

        async with self._get_connection_lock():
            while True:
                try:
                    if not self._webui_ready:
                        log.info(f"Checking ComfyUI connection at {self.server_address}...")

                    if require_webui:
                        resp = await self._make_request_once("GET", "/uiapi/connection_status")
                        assert isinstance(resp, dict)
                        if resp.get("active_clients", 0) == 0:
                            raise ConnectionError("WebUI not connected")

                    # Test WebSocket connection (close immediately)
                    ws = await self.connect_ws()
                    await ws.close()
                    self._webui_ready = True
                    return True

                except Exception as e:
                    self._webui_ready = False
                    wait_time = min(self._reconnect_backoff * 2, 30)
                    log.warning(f"Connection failed: {e!s} (retrying in {wait_time:.1f}s...)")
                    await asyncio.sleep(wait_time)
                    self._reconnect_backoff = wait_time
                    if not loop:
                        return False

    # HTTP Request Layer
    # ----------------------------------------
    async def _make_request_once(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        files: Mapping[str, BinaryIO | tuple[str | None, BinaryIO, str]] | None = None,
        verbose: bool = False,
    ) -> dict[str, Any] | np.ndarray:
        """Single HTTP request without retry logic"""
        address = f"{self.server_address}{url}"
        if not address.startswith("http"):
            address = f"http://{address}"

        if verbose:
            log.debug(f"Request: {method} {address} data={data} files={files.keys() if files else None}")

        try:
            async with httpx.AsyncClient() as client:
                if files:
                    response = await client.post(address, data=data, files=files)
                    response.raise_for_status()
                    return cast(dict[str, Any], response.json())
                else:
                    json_data = data if data is not None else None
                    response = await client.request(
                        method,
                        address,
                        json=json_data,
                        headers={"Content-Type": "application/json"} if json_data else None,
                    )
                    response.raise_for_status()
                    ret = response.content

                    if isinstance(ret, bytes):
                        if ret.startswith(PNG_MAGIC_BYTES):
                            img = cv2.imdecode(np.frombuffer(ret, np.uint8), cv2.IMREAD_COLOR)
                            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        else:
                            return cast(dict[str, Any], json.loads(ret.decode("utf-8")))
                    else:
                        raise ValueError(f"Unexpected response type: {type(ret)}")

        except (httpx.ConnectError, ConnectionRefusedError) as e:
            raise ComfyConnectionError(f"ComfyUI not reachable at {address}") from e

    async def _make_request(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        files: Mapping[str, BinaryIO | tuple[str | None, BinaryIO, str]] | None = None,
        verbose: bool = False,
        retry: bool = False,
    ) -> dict[str, Any] | np.ndarray:
        """Make request with optional automatic reconnection"""
        while True:
            try:
                return await self._make_request_once(method, url, data, files, verbose)
            except Exception as e:
                if not retry:
                    raise
                log.error(f"Request failed: {method} {url} - {e!s}, retrying...")
                self._webui_ready = False
                await self.ensure_connection_async()

    # Sync/Async Bridge
    # ----------------------------------------
    def run_sync(self, coroutine):
        """
        Run a coroutine synchronously.

        CRITICAL: Cannot be called from async context (will deadlock).
        Creates isolated event loop for thread safety.
        """
        # Prevent deadlock: cannot call from async context
        try:
            asyncio.get_running_loop()
            raise RuntimeError(
                "run_sync() called from async context - use await instead. "
                "This would deadlock. Call the async version directly."
            )
        except RuntimeError:
            pass  # No running loop, safe to proceed

        with self._sync_lock:
            # Always create new loop for isolation (prevents state leakage)
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(coroutine)
            finally:
                # Clean up the loop to prevent resource leak
                loop.close()

    # JSON API Helpers
    # ----------------------------------------
    def json_post(self, url: str, input_data: dict | None = None, verbose: bool = False, retry: bool = False) -> dict:
        """Sync POST with JSON body"""
        return self.run_sync(self.json_post_async(url, input_data, verbose, retry))

    async def json_get_async(self, url: str, verbose: bool = False, retry: bool = False) -> Any:
        """Async GET request"""
        return await self._make_request("GET", url, None, verbose=verbose, retry=retry)

    async def json_post_async(
        self, url: str, input_data: dict | None = None, verbose: bool = False, retry: bool = False
    ) -> Any:
        """Async POST with JSON body"""
        data = input_data or {}
        if isinstance(data, str):
            data = json.loads(data)
        data["verbose"] = verbose
        data["client_id"] = self.client_id
        return await self._make_request("POST", url, data, verbose=verbose, retry=retry)

    # Field Operations (uiapi)
    # ----------------------------------------
    def gets(self, verbose: bool = False):
        """Query all available fields (sync)"""
        return self.run_sync(self.gets_async(verbose))

    def get(self, path_or_paths: str | list[str], verbose: bool = False):
        """Get field value(s) (sync)"""
        return self.run_sync(self.get_async(path_or_paths, verbose))

    def set(self, path_or_fields: str | list, value: Any = None, verbose: bool = False, clamp: bool = False):
        """Set field value(s) (sync)"""
        return self.run_sync(self.set_async(path_or_fields, value, verbose, clamp))

    def connect(self, path1: str, path2: str, verbose: bool = False):
        """Connect two nodes (sync)"""
        return self.run_sync(self.connect_async(path1, path2, verbose))

    async def gets_async(self, verbose: bool = False):
        """Query all available fields (async)"""
        response = await self.json_post_async("/uiapi/query_fields", verbose=verbose)
        if isinstance(response, dict):
            return response.get("result") or response.get("response")
        raise ValueError("Unexpected response format from server")

    async def get_async(self, path_or_paths: str | list[str], verbose: bool = False):
        """Get field value(s) (async)"""
        is_single = isinstance(path_or_paths, str)
        paths = [path_or_paths] if is_single else path_or_paths

        response = await self.json_post_async("/uiapi/get_fields", {"fields": paths}, verbose=verbose)

        if isinstance(response, dict):
            result = response.get("result") or response.get("response")
            if result:
                return result[path_or_paths] if is_single else result

        raise ValueError(f"Unexpected response format: {response}")

    async def set_async(
        self, path_or_fields: str | list, value: Any = None, verbose: bool = False, clamp: bool = False
    ):
        """Set field value(s) (async)"""
        # If using workflow mode, buffer fields locally
        if self.workflow is not None:
            if isinstance(path_or_fields, str):
                self.workflow_fields[path_or_fields] = value
            else:
                for path, val in path_or_fields:
                    self.workflow_fields[path] = val
            return

        # WebUI mode - send to server
        fields = [(path_or_fields, value)] if isinstance(path_or_fields, str) else path_or_fields
        processed_fields = []

        for path, val in fields:
            if not self.is_valid_value(val):
                log.warning(f"Skipping invalid value for {path}: {val}")
                continue

            if is_image(val):
                try:
                    base64_img = encode_image_to_base64(val)
                    processed_fields.append([path, {"type": "image_base64", "data": base64_img}])
                except Exception as e:
                    log.error(f"Failed to encode image for {path}: {e}")
                    continue
            else:
                if clamp:
                    val = clamp01(val)
                processed_fields.append([path, val])

        if not processed_fields:
            log.warning("No valid fields to set")
            return None

        return await self.json_post_async("/uiapi/set_fields", {"fields": processed_fields}, verbose=verbose)

    async def connect_async(self, path1: str, path2: str, verbose: bool = False):
        """Connect two nodes (async)"""
        return await self.json_post_async("/uiapi/set_connection", {"field": [path1, path2]}, verbose=verbose)

    def is_valid_value(self, value: Any) -> bool:
        """Check if a value is valid to send (no NaN, Infinity, None)"""
        if isinstance(value, (int, float)):
            return not (math.isinf(value) or math.isnan(value))
        elif isinstance(value, (str, bool)):
            return True
        elif value is None:
            return False
        elif isinstance(value, (list, tuple)):
            return all(self.is_valid_value(v) for v in value)
        return True

    # Execution
    # ----------------------------------------
    def execute(self, wait: bool = True) -> np.ndarray | None:
        """Execute workflow and return result image (sync)"""
        return self.run_sync(self.execute_async(wait))

    async def execute_async(self, wait: bool = True) -> np.ndarray | None:
        """Execute workflow via uiapi and return result image (async)"""
        try:
            await self.on_before_execute()

            log.info("Executing prompt...")
            ret = await self.json_post_async("/uiapi/execute")

            if not wait:
                return ret

            if not isinstance(ret, dict):
                raise ValueError(f"Unexpected response format: {ret}")

            # Validate response structure immediately - no retry on malformed response
            # (retrying would send ANOTHER execution, not re-query the same one)
            if "response" not in ret or "prompt_id" not in ret.get("response", {}):
                raise ValueError(
                    f"Malformed execution response (missing prompt_id). "
                    f"Response: {ret}. "
                    f"This indicates a server-side issue, not a transient network error."
                )

            exec_id = ret["response"]["prompt_id"]

            # Prevent race condition where queue appears empty before execution posts
            await asyncio.sleep(3)
            await self.await_execution()

            log.info("Execution completed, fetching results...")

            workflow_json = await self.get_workflow()
            if not isinstance(workflow_json, dict) or "response" not in workflow_json:
                raise ValueError(f"Invalid workflow response: {workflow_json}")

            output_node_id = self.find_output_node(workflow_json["response"])
            if not output_node_id:
                raise ValueError("No output node found in workflow")

            history = await self.get_history_async(exec_id)
            history_data = history[exec_id]

            filenames = history_data["outputs"][output_node_id]["images"]
            if not filenames:
                log.warning("No images found in execution output")
                return None

            info = filenames[0]
            result = await self.get_image_async(info["filename"], info["subfolder"], info["type"])

            await self.on_after_execute(result)
            return result

        except Exception as e:
            log.error(f"Execution failed: {e!s}")
            raise

    async def on_before_execute(self):
        """Hook called before workflow execution. Override in subclasses."""
        pass

    async def on_after_execute(self, result: np.ndarray | None = None):
        """Hook called after workflow execution. Override in subclasses."""
        pass

    async def await_execution(self):
        """
        Wait for execution completion via WebSocket.

        CRITICAL: Properly closes WebSocket on error to prevent resource leak.
        Uses async iteration for message receiving.
        """
        start_time = time.time()
        max_timeout = 90
        last_status_time = 0
        got_execution_status = False
        ws = await self.connect_ws(max_timeout)

        try:
            # Use async for to iterate over messages
            async for message in ws:
                current_time = time.time()
                elapsed = current_time - start_time

                if current_time - last_status_time >= 5:
                    log.info(f"Execution status: Running for {elapsed:.1f}s")
                    last_status_time = current_time

                if isinstance(message, str):
                    msg = json.loads(message)
                    msg_type = msg["type"]

                    if msg_type == "status":
                        queue_size = msg["data"]["status"]["exec_info"]["queue_remaining"]
                        if queue_size > 0:
                            got_execution_status = True
                        elif got_execution_status:
                            log.info(f"Execution completed in {elapsed:.1f}s")
                            break

                    elif msg_type == "execution_start":
                        log.info(f"Started prompt: {msg['data']['prompt_id']}")

                    elif msg_type == "execution_cached":
                        log.info(f"Cached nodes: {len(msg['data']['nodes'])}")

                    elif msg_type == "executing":
                        node = msg["data"]["node"]
                        if node:
                            log.debug(f"Executing node: {node}")

                    elif msg_type == "progress":
                        value, max_val = msg["data"]["value"], msg["data"]["max"]
                        log.debug(f"Progress: {value}/{max_val}")

                    elif msg_type == "execution_success":
                        break

        except Exception as e:
            log.error(f"Execution monitoring failed: {e!s}")
            raise
        finally:
            # CRITICAL: Always close WebSocket to prevent resource leak
            await ws.close()

    # Workflow API (direct, no WebUI)
    # ----------------------------------------
    def execute_workflow(
        self, workflow: dict, fields: list[tuple[str, Any]] | None = None, wait: bool = True
    ) -> np.ndarray | None:
        """Execute workflow directly via /prompt endpoint (sync)"""
        return self.run_sync(self.execute_workflow_async(workflow, fields=fields, wait=wait))

    async def execute_workflow_async(
        self, workflow: dict, fields: list[tuple[str, Any]] | None = None, wait: bool = True
    ) -> np.ndarray | None:
        """Execute workflow directly via /prompt endpoint (async)"""
        try:
            if fields is None:
                fields = []

            if self.workflow is not None:
                fields.extend(self.workflow_fields.items())

            await self.on_before_execute()

            # Convert None values to empty strings
            def convert_nones(obj):
                if isinstance(obj, dict):
                    return {k: convert_nones(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_nones(x) for x in obj]
                elif obj is None:
                    return ""
                return obj

            workflow = cast(dict, convert_nones(workflow))
            workflow = json.loads(json.dumps(workflow))  # Deep copy

            # Apply field overrides
            if fields:
                for path, value in fields:
                    parts = path.split(".")
                    if not parts:
                        continue

                    node_result = self._find_node_by_title_or_id(workflow, parts[0])
                    if not node_result:
                        log.warning(f"Node not found: {parts[0]}")
                        continue

                    node_id, node = node_result
                    node_title = node.get("_meta", {}).get("title", "").strip() or f"node_{node_id}"

                    if "inputs" not in node:
                        node["inputs"] = {}

                    # Handle image uploads
                    image_extensions = [".png", ".jpg", ".jpeg", ".webp"]
                    is_image_path = isinstance(value, str) and any(
                        value.lower().endswith(ext) for ext in image_extensions
                    )
                    if is_image(value) or is_image_path:
                        try:
                            response = await self.upload_image(
                                value,
                                folder_type="input",
                                overwrite=True,
                                filename=f"INPUT_{node_title}",
                            )
                            value = response["name"]
                        except Exception as e:
                            log.error(f"Failed to upload image for {path}: {e}")
                            continue

                    # Apply value based on path format
                    if len(parts) == 1 or (len(parts) == 2 and parts[1] == "value"):
                        field_name = self._get_default_input_name(node)
                        if field_name:
                            node["inputs"][field_name] = value
                    elif len(parts) == 2:
                        node["inputs"][parts[1]] = value
                    elif len(parts) == 3 and parts[1] == "inputs":
                        node["inputs"][parts[2]] = value

            # Queue the prompt
            log.info("Executing workflow via API...")
            ret = await self._make_request("POST", "/prompt", {"prompt": workflow, "client_id": self.client_id})

            if not wait:
                return cast(WorkflowResponse, ret)

            if not isinstance(ret, dict) or "prompt_id" not in ret:
                raise ValueError(f"Invalid response format: {ret}")

            prompt_id = ret["prompt_id"]

            await asyncio.sleep(1)
            await self.await_execution()

            # Fetch results
            history = await self.get_history_async(prompt_id)
            if not isinstance(history, dict) or prompt_id not in history:
                raise ValueError(f"Invalid history response: {history}")

            history_data = cast(HistoryData, history[prompt_id])

            # Find and return first SaveImage output
            result = None
            for node_id, node_output in history_data.get("outputs", {}).items():
                if "images" in node_output:
                    for image_info in node_output["images"]:
                        image_data = await self.get_image_async(
                            image_info["filename"], image_info["subfolder"], image_info["type"]
                        )
                        if isinstance(image_data, np.ndarray):
                            if "save" in workflow[node_id]["class_type"].lower():
                                result = image_data
                                break

            await self.on_after_execute(result)
            return result

        except Exception as e:
            log.error(f"Workflow execution failed: {e!s}")
            raise

    # Model Downloads
    # ----------------------------------------
    def download_models(
        self, models: dict[str, ModelDef], timeout: int = 300, workflow: dict[str, Any] | None = None
    ) -> dict[str, dict[str, Any]]:
        """Download models (sync)"""
        return self.run_sync(self.download_models_async(models, timeout, workflow))

    async def download_models_async(
        self, models: dict[str, ModelDef], timeout: int = 300, workflow: dict[str, Any] | None = None
    ) -> dict[str, dict[str, Any]]:
        """Download models via uiapi (async)"""
        download_table = {filename: model_def.to_dict() for filename, model_def in models.items()}

        log.info(f"Starting download of {len(models)} models (timeout={timeout}s)")

        start_time = time.time()
        try:
            resp = await self._make_request(
                "POST",
                "/uiapi/download_models",
                {"download_table": download_table, "workflow": workflow},
            )
            assert isinstance(resp, dict)

            download_id = resp.get("download_id")
            if not download_id:
                raise ValueError("No download_id in response")

            last_status_time = 0
            while True:
                stat = await self._make_request("GET", f"/uiapi/download_status/{download_id}")
                assert isinstance(stat, dict)

                current_time = time.time()
                elapsed = current_time - start_time

                if current_time - last_status_time >= 5:
                    progress = stat.get("progress", {})
                    completed = sum(1 for info in progress.values() if info.get("status") == "success")
                    log.info(f"Download progress: {completed}/{len(models)} ({elapsed:.1f}s)")
                    last_status_time = current_time

                if stat.get("completed", False):
                    log.info(f"All downloads completed in {elapsed:.1f}s")
                    return stat.get("progress", {})

                for model, info in stat.get("progress", {}).items():
                    if info.get("status") == "error":
                        log.error(f"Error downloading {model}: {info.get('error')}")

                await asyncio.sleep(1)

                if elapsed > timeout:
                    raise TimeoutError(f"Download timeout after {timeout}s")

        except ComfyConnectionError:
            raise
        except Exception as e:
            log.error(f"Download process failed: {e!s}")
            raise

    # Utilities
    # ----------------------------------------
    async def get_workflow(self) -> dict:
        """Get current workflow state"""
        return await self.json_post_async("/uiapi/get_workflow")

    async def get_history_async(self, prompt_id: str) -> dict:
        """Get execution history"""
        return await self._make_request("GET", f"/history/{prompt_id}")

    async def get_image_async(self, filename: str, subfolder: str, folder_type: str) -> np.ndarray | None:
        """Fetch image from ComfyUI"""
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        ret = await self._make_request("GET", f"/view?{url_values}")
        assert isinstance(ret, np.ndarray)
        return ret

    async def upload_image(
        self,
        image_input: str | Image.Image | np.ndarray,
        subfolder: str | None = None,
        folder_type: str | None = None,
        overwrite: bool = False,
        filename: str | None = None,
    ) -> UploadResponse:
        """Upload an image to ComfyUI server"""
        url = "/upload/image"
        data = {"overwrite": str(overwrite).lower()}
        if subfolder:
            data["subfolder"] = subfolder
        if folder_type:
            data["type"] = folder_type

        if isinstance(image_input, str):
            async with aiofiles.open(image_input, "rb") as f:
                content = await f.read()
            files = {"image": (f"{filename}.png" if filename else None, content, "image/png")}
        elif isinstance(image_input, np.ndarray):
            img_array = image_input
            if img_array.dtype in [np.float32, np.float64]:
                img_array = (img_array * 255).astype(np.uint8)
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            success, buffer = cv2.imencode(".png", img_array)
            if not success:
                raise ValueError("Failed to encode image")
            img_byte_arr = io.BytesIO(buffer.tobytes())
            files = {"image": (f"{filename}.png" if filename else "image.png", img_byte_arr, "image/png")}
        else:
            img_byte_arr = io.BytesIO()
            image_input.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)
            files = {"image": (f"{filename}.png" if filename else "image.png", img_byte_arr, "image/png")}

        response = await self._make_request("POST", url, data=data, files=files)
        if not isinstance(response, dict):
            raise ValueError(f"Invalid upload response: {response}")
        return cast(UploadResponse, response)

    @staticmethod
    def _find_node_by_title_or_id(workflow: dict, node_ref: str) -> tuple[str, dict] | None:
        """Find a node by its title or ID"""
        if node_ref in workflow:
            return node_ref, workflow[node_ref]
        for node_id, node in workflow.items():
            if node.get("_meta", {}).get("title", "").lower() == node_ref.lower():
                return node_id, node
        return None

    @staticmethod
    def _get_default_input_name(node: dict) -> str | None:
        """Get the name of the first input field for a node"""
        if not node.get("inputs"):
            return None
        return next(iter(node["inputs"].keys()), None)

    @staticmethod
    def find_output_node(json_object: dict) -> str | None:
        """Find the SaveImage node in the workflow"""
        for key, value in json_object.items():
            if isinstance(value, dict):
                if value.get("class_type") in ["SaveImage", "Image Save"]:
                    return key
                result = ComfyClient.find_output_node(value)
                if result:
                    return result
        return None

    @property
    def is_webui_ready(self) -> bool:
        """Check if WebUI is ready without waiting"""
        return self._webui_ready

    def check_webui_connection_status(self) -> dict:
        """Check WebUI connection status"""
        try:
            return self.run_sync(self.json_get_async("/uiapi/connection_status"))
        except Exception as e:
            log.error(f"Error checking connection status: {e}")
            return {"status": "error", "error": str(e), "webui_connected": False}

    def free(self):
        """Mark client as freed (for cleanup)"""
        self.freed = True
