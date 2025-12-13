"""
Model definitions for ComfyUI model downloading.

These dataclasses define model sources (HuggingFace, CivitAI, Google Drive)
and are serialized to JSON when sent to the ComfyUI server for downloading.

Note: Actual downloading happens server-side. This module only defines
the data structures for client-server communication.
"""

from dataclasses import dataclass
from enum import Enum, auto


class ControlNetType(Enum):
    STANDARD = auto()
    XS = auto()


@dataclass
class ModelDef:
    """
    Represents paths for a specific model type with fallback options.

    Used to specify where a model can be downloaded from. The server
    will try sources in order: local -> civitai -> huggingface -> gdrive
    """

    huggingface: str | None = None
    local: str | None = None
    civitai: str | None = None
    gdrive: str | None = None
    fp16: bool = True
    ckpt_type: str = "checkpoints"

    def to_dict(self) -> dict:
        """Convert ModelDef to a dictionary for JSON serialization"""
        return {
            "huggingface": self.huggingface,
            "local": self.local,
            "civitai": self.civitai,
            "gdrive": self.gdrive,
            "fp16": self.fp16,
            "ckpt_type": self.ckpt_type,
        }

    @property
    def huggingface_id(self) -> str | None:
        """Extract organization/model repo ID from HuggingFace URL or direct ID"""
        if not self.huggingface:
            return None

        repo_id = self.huggingface
        if repo_id.startswith("https://huggingface.co/"):
            parts = repo_id[len("https://huggingface.co/") :].split("/")
            if len(parts) >= 2:
                repo_id = "/".join(parts[:2])
        return repo_id

    @property
    def huggingface_filename(self) -> str | None:
        """Extract filename from HuggingFace URL if it's a direct file link"""
        if not self.huggingface:
            return None

        if any(self.huggingface.endswith(ext) for ext in [".safetensors", ".bin", ".ckpt"]):
            return self.huggingface.split("/")[-1]
        return None


@dataclass
class ControlNetDef(ModelDef):
    """Represents a ControlNet configuration with path and type information"""

    cn_type: ControlNetType = ControlNetType.STANDARD

    def __init__(
        self,
        huggingface: str | None = None,
        local: str | None = None,
        civitai: str | None = None,
        gdrive: str | None = None,
        fp16: bool = True,
        cn_type: ControlNetType = ControlNetType.STANDARD,
    ):
        super().__init__(huggingface, local, civitai, gdrive, fp16)
        self.ckpt_type = "controlnet"
        self.cn_type = cn_type

    def is_xs(self) -> bool:
        return self.cn_type == ControlNetType.XS


@dataclass
class VaeDef(ModelDef):
    """Represents a VAE model definition"""

    def __init__(
        self,
        huggingface: str | None = None,
        local: str | None = None,
        civitai: str | None = None,
        gdrive: str | None = None,
        fp16: bool = True,
    ):
        super().__init__(huggingface, local, civitai, gdrive, fp16)
        self.ckpt_type = "vae"


@dataclass
class LoraDef(ModelDef):
    """Represents a LoRA configuration with path and strength information"""

    unet_strength: float = 1.0
    text_encoder_strength: float | None = None
    fuse: bool = False

    def __init__(
        self,
        huggingface: str | None = None,
        local: str | None = None,
        civitai: str | None = None,
        gdrive: str | None = None,
        weights: float | tuple[float, float] = 1.0,
        fuse: bool = True,
    ):
        super().__init__(huggingface, local, civitai, gdrive)
        self.unet_strength = weights[0] if isinstance(weights, tuple) else weights
        self.text_encoder_strength = weights[1] if isinstance(weights, tuple) else weights
        self.fuse = fuse
        self.ckpt_type = "loras"
