from enum import Enum
from dataclasses import dataclass

class VirtueAIModel(Enum):
    VIRTUE_GUARD_TEXT_LITE = "Virtue-AI/VirtueGuard-Text-Lite"


class VirtueAIResponseStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    UNSAFE = "unsafe"

@dataclass
class VirtueAIResponse():
    status: VirtueAIResponseStatus
    message: str | None = None
    validated_output: str | None = None