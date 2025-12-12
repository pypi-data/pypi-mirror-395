import logging
from typing import Callable
from confluent_kafka import Producer
from .exceptions.cache import KeyNotFoundException

from .classes.cache import Cache
from .classes.event_object import EventObject


def default_callback(err, msg):
    if err:
        logging.error("Message failed delivery: {}".format(err))


def produce(
    config: dict,
    cache: Cache,
    logger: logging.Logger,
    topic: str,
    event_object: EventObject,
    callback: Callable = default_callback,
    skip_cache: bool = False,
):
    """Produce an event to the kafka message queue."""
    kafka_config = config["kafka.default"]
    kafka_config.update(config["kafka.producer"])

    producer = Producer(kafka_config)
    event_object.add_audit_log(config["general"]["current_location"])
    event_json = event_object.encode()

    producer.produce(
        topic,
        key=str(event_object.correlation_id),
        value=event_json,
        callback=callback,
    )

    producer.poll(100)
    producer.flush()
    
    if skip_cache:
        try:
            cache.update(event_object)
        except KeyNotFoundException:
            cache.add(event_object)

    logger.info(
        "Produced - topic {topic}: key = {key} value = {value}".format(
            topic=topic,
            key=f"{str(event_object.correlation_id)}",
            value=f"{event_json}",
        )
    )
