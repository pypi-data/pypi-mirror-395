import asyncio

from .event_object import EventObject
## from multiprocessing.connection import PipeConnection


class ConsumerStorage:
    """A simple storage for events. 
    Pulls events from pipeline and stores them in a dict.
    """
    def __init__(self, connection = None) -> None:
        self.storage = {}
        self.connection = connection
        self.consumers = 0

    def connect(self, connection) -> None:
        self.connection = connection

    async def poll(self, timeout = 0.1) -> bool:
        if self.connection.poll(timeout):
            return await self.receive()

        return False
    
    async def receive(self) -> True:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, self.connection.recv)

        self.set(data["key"], data["value"])

        if self.connection.poll(0):
            await self.receive()

        return True

    def set(self, key, value) -> None:
        if isinstance(value, EventObject):
            self.storage[key] = value
        else:
            try:
                self.storage[key] = EventObject.decode(value)
            except Exception as exc:
                raise Exception("Cannot map value to EventObject.") from exc

    def get(self, key, default = None) -> any:
        return self.storage.get(key, default)
    
    def remove(self, key) -> None:
        del self.storage[key]

    async def consume(self, key) -> any:
        while True:
            data = self.get(key)
            if data:
                self.remove(key)
                return data

            if self.consumers > 0:
                await asyncio.sleep(0.1)
            else:
                self.consumers += 1
                try:
                    await self.receive()
                finally:
                    self.consumers -= 1

    async def consume_all(self):
        if self.connection.poll(0):
            await self.receive()

        data = self.storage.copy()

        for key in data.keys():
            self.remove(key)

        return data

    def print(self) -> None:
        print(self.storage)
