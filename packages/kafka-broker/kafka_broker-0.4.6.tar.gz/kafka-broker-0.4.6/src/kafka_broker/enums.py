import enum


class EventStatus(str, enum.Enum):
    ERROR = "error"
    SUCCESS = "success"
    ONGOING = "ongoing"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

