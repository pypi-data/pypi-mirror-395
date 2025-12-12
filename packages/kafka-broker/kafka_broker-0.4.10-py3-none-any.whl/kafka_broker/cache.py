from logging import Logger
from uuid import UUID

from .exceptions.cache import CouldNotEditMemcache, KeyNotFoundException
from .classes import EventObject
from pymemcache.client.base import Client


class Cache:
    def __init__(self, config, logger: Logger) -> None:
        self.client = self.innitialize_connection(config)
        self.config = config
        self.logger = logger

    def innitialize_connection(self, config):
        client = Client(
            (
                config["memcached"]["cache_location"],
                config["memcached"]["cache_port"],
            )
        )
        if client is not None:
            return client
        else:
            raise ConnectionError

    def add(self, event_object: EventObject):
        res = self.client.add(
            str(event_object.correlation_id), event_object.encode()
        )
        if res is False:
            raise CouldNotEditMemcache
        self.logger.info(f"Added {str(event_object.correlation_id)} to cache.")

    def get(self, correlation_id: UUID):
        byte_string = self.get_raw(correlation_id)
        return EventObject.decode(byte_string.decode("utf-8"))

    def get_raw(self, correlation_id: UUID):
        byte_string = self.client.get(str(correlation_id))
        if byte_string is None:
            raise KeyNotFoundException
        return byte_string

    def delete(self, correlation_id: UUID):
        res = self.client.delete(str(correlation_id))
        if res is False:
            raise CouldNotEditMemcache
        self.logger.info(f"Deleted {str(correlation_id)} to cache.")
        return res

    def update(self, event_object: EventObject):
        res = self.client.set(
            str(event_object.correlation_id), event_object.encode()
        )
        if res is False:
            raise CouldNotEditMemcache
        self.logger.info(f"Updated {str(event_object.correlation_id)} in cache.")
        return res
