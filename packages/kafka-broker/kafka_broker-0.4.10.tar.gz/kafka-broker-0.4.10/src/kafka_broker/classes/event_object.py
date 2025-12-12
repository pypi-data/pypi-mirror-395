import json
import datetime
import uuid
from pydantic import BaseModel


class EventObject:
    def __init__(
        self,
        *,
        correlation_id: uuid.UUID = None,
        event: str = None,
        data: dict[any] = None,
        status: str = None,
        audit_log: list[dict[str, int, int]] = None,
    ) -> None:
        """Initialize the EventObject:

        Parameters
        ----------
        correlation_id : uuid.UUID
            Event identifier

        event : str
            Event action

        data : any
            payload

        audit_log : list[dict[str, int, int]]
            Places this object has been
        """
        if not correlation_id:
            correlation_id = uuid.uuid4()
        self.correlation_id = correlation_id

        if not event:
            event = "base.event"
        self.event = event

        if not data:
            data = {}
        self.data = data

        if not status:
            status = "pending"
        self.status = status

        if not audit_log:
            audit_log = []
        self.audit_log = audit_log
        self.last_update = int(datetime.datetime.now().timestamp())

    def time_update(self) -> None:
        self.last_update = int(datetime.datetime.now().timestamp())

    def as_reply(self, message: str = "Internal Server Error", status_code: int = 500) -> None:
        self.data = {
            "message": message,
            "status_code": status_code,
            "payload": self.data
        }

    def encode(self):
        result = {
            "correlation_id": self.correlation_id,
            "status": self.status,
            "event": self.event,
            "data": self.data,
            "audit_log": self.audit_log,
        }

        def default(o):
            if isinstance(o, (datetime.date, datetime.datetime)):
                return o.isoformat()
            
            if isinstance(o, uuid.UUID):
                return str(o)
            
            if isinstance(o, BaseModel):
                return o.model_dump()

        
        result = json.dumps(result, default=default)
        return result

    def decode(value):
        data = json.loads(value)

        self = EventObject()

        self.correlation_id = data.get("correlation_id")
        self.status = data.get("status")
        self.event = data.get("event")
        self.data = data.get("data")
        self.audit_log = data.get("audit_log")

        return self

    def add_audit_log(self, location):
        self.audit_log.append(
            {
                "data": self.data.copy(),
                "event": self.event,
                "location": location,
                "time_sent": int(datetime.datetime.now().timestamp()),
                "time_received": None,
            }
        )

    def update_audit_log(self):
        cur_location = self.audit_log[-1]
        cur_location["time_received"] = int(datetime.datetime.now().timestamp())
