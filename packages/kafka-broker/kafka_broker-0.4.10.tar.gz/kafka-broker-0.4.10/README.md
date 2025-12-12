# Kafka Broker

A python package implementation for the confluent kafka package. Managing producing and consuming.

Has built-in implementation for FastAPI.

## About this package

The package allows for easy setup and connecting to the Apache Kafka message broker.

Easily run a consumer in a second process so it does not act as a blocking operation.

To read the received data from the broker, poll the consumer storage. To wait for a specific item (based on correlation ID), await the consume function.

## The BrokerManager

Has 3 simple functions:

`produce` - produce an event to the message broker.

`init_consumer_app` - initialize the consumer together with an FastAPI app.

`init_consumer` - initialize a regular consumer.

It has an attribute called the `consumer_storage`. This is where everything the consumer finds will be stored. Though in reality, you have to call `receive()` to actually get any data.

`receive()` is a blocking operation; `poll()` is not. And `consume()` finds a certain event object based on `correlation_id`, which is also a blocking operation.

These `consumer_storage` functions are all asyncronous so they do not block any process. For example for if you were using FastAPI.

There is also `consume_all()`, which is basicly a `poll()`, but also returns everything found within the storage.

## The EventRouter

Our event router is based on RabbitMQ's routing keys and on FastAPI's router.

### Exmaple implementation
_app/\_\_init\_\_.py_
```python
from app.test import test_router


event_router = EventRouter("module")


event_router.include_binder(test_router)
```
>_Sidenote: We give the highest router the name of the module._

_app/test/\_\_init\_\_.py_
```python
test_router = EventRouter("test")


@test_router.bind_event("return")
def return_event(event_object: EventObject):
    event_object.data = some_funtion()
    event_object.event = "respond"

    broker_manager.produce("SomeModule", event_object)
```

With the event string `"test.return"`, the event router will first find the corresponding bind called `'test'`. If `'test'` is found, based on whether it's another `EventRouter` or a `function`, it will either continue the search chain in the next router or execute the found `function`.

## The EventObject

A simple class intended to be used for communicating with other microservices.

A `correlation_id` to track if an object is the same one as the one you sent off.

An `event`-string to route the EventObject to the right place.

A `data` field containing any JSON serializable information.

An `audit_log` to track where this EventObject has been.

## Examples

Send event and wait for response:
```python
from kafka_broker import broker_manager, EventObject


correlation_id = str(uuid.uuid4())
event = "test.return"

event_object = EventObject(
    correlation_id=correlation_id, 
    event=event,
)

broker_manager.produce("SomeModule", event_object)

data = await broker_manager.consumer_storage.consume(correlation_id)
return data
```

Run a process based on all events:
```python
from kafka_broker import broker_manager


async def main():
    broker_manager.init_consumer()

    while True:
        await asyncio.sleep(1)

        data = await broker_manager.consumer_storage.consume_all()

        if data:
            for _, event_object in data.items():
                event_router.execute_event(event_object)
```
