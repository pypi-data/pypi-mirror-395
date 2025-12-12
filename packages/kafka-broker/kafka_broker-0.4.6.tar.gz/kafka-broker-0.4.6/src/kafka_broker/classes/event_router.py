import logging
from typing import Self
from pydantic import ValidationError

from kafka_broker.exceptions.base import CustomException
from kafka_broker.schemas.log import LogSchema

from ..enums import EventStatus
from ..exceptions.cache import KeyNotFoundException
from ..broker_manager import broker_manager
from .event_object import EventObject

logging_module = "LoggingModule"
log_event = "log.create"

class EventRouter:
    """A simple router.
    Bind events to expose them to the router.
    Bind routers to expand the router.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.binds = {}

    def check_bind(self, name):
        if self.binds.get(name) is not None:            
            raise KeyError(f"Bind name '{name}' is already in use.")

    def bind_event(self, name):
        self.check_bind(name)
        def inner(func):
            self.binds[name] = func
            return func
        return inner
    
    def include_binder(self, binder: Self):
        self.check_bind(binder.name)
        self.binds[binder.name] = binder

    def execute_event(self, event_object: EventObject, events: list[str] = None):
        try:
            if not events:
                events = event_object.event.split(".")

            for key, func in self.binds.items():
                if key == events[0]:
                    if isinstance(func, EventRouter):
                        return func.execute_event(event_object, events[1:])
                    
                    return func(event_object=event_object)
            else:
                logging.warning(f"Event '{event_object.event}' not found in '{self.name}'")

        except CustomException as exc:
            self.exception_handler(exc, exc.level, exc.message, event_object)

        except ValidationError as exc:
            self.exception_handler(exc, 40, exc.title, event_object)

        except Exception as exc:
            self.exception_handler(exc, 50, f"internal server error: {str(exc)}", event_object)

    def exception_handler(self, exc: Exception, level: int, msg: str, event_object: EventObject):
        logging.exception(exc)
        event_object.as_reply()
        event_object.status = EventStatus.ERROR
        
        try:
            broker_manager.cache.update(event_object)
        except KeyNotFoundException:
            broker_manager.cache.add(event_object)

        if broker_manager.config.get("general").get("current_location") != logging_module:
            
            job_id = event_object.data["payload"].get("job_id")
            sequence = event_object.data["payload"].get("sequence")
            if not sequence:
                sequence = []
            store = event_object.data["payload"].get("store")
            if not store:
                store = {}

            log = LogSchema(
                correlation_id=event_object.correlation_id,
                level=level,
                message=msg,
                module=logging_module,
                status=EventStatus.ERROR,
                job_id=job_id,
                sequence=sequence,
                store=store
            )
            event_object.event = log_event
            event_object.data = log
            broker_manager.produce(logging_module, event_object)
