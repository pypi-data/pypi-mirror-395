from enum import Enum, auto


class NotificationType(Enum):
    """Types of notifications."""
    SUCCESS = auto()
    ERROR = auto()
    WARNING = auto()