import logging
from confluent_kafka import Consumer
from multiprocessing import Pipe, Process

# from multiprocessing.connection import PipeConnection

from .classes.consumer_storage import ConsumerStorage
from .classes.event_object import EventObject


def init_consumer(
    config: dict, logger: logging.Logger, consumer_storage: ConsumerStorage, app
):
    """Initialize the consumer for FastAPI."""
    global consumer_storage_
    consumer_storage_ = consumer_storage

    @app.on_event("startup")
    async def startup_event():
        global consuming, consumer_storage_

        logging.info("Starting consumer...")

        consuming, consumer_storage_ = initialize(config, logger, consumer_storage_)

    @app.on_event("shutdown")
    async def shutdown_event():
        logging.info("Stopping consumer...")

        consuming.join()

    return app, consumer_storage_


def initialize(config: dict, logger: logging.Logger, consumer_storage: ConsumerStorage):
    """Initialize the consumer in a second process.

    This process can communicate with the current process through a pipe.
    """
    parent_conn, child_conn = Pipe()
    consumer_storage.connect(parent_conn)

    consuming = Process(
        target=multiprocess_consume,
        args=(
            config,
            logger,
            child_conn,
        ),
    )
    consuming.start()

    return consuming, consumer_storage


def multiprocess_consume(config: dict, logger: logging.Logger, pipe):
    """Consumer loop."""
    kafka_config = config["kafka.default"]
    kafka_config.update(config["kafka.consumer"])
    consumer = Consumer(kafka_config)
    consumer.subscribe([config["general"]["current_location"]])

    try:
        while True:
            msg = consumer.poll(1.0)

            logger.debug("[*] Waiting...")

            if msg is None:
                ...

            elif msg.error():
                logger.error(msg.error())

            else:
                handle_multiprocess(pipe, logger, msg)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()


def consume(consumer: Consumer, logger: logging.Logger):
    """Consumer loop."""
    try:
        while True:
            msg = consumer.poll(1.0)

            logger.debug("[*] Waiting...")

            if msg is None:
                continue

            if msg.error():
                logger.error(msg.error())

            else:
                return handle(logger, msg)

    except KeyboardInterrupt:
        consumer.close()


def handle(logger: logging.Logger, msg):
    """Handle a non error event."""
    topic = msg.topic()
    key = msg.key().decode("utf-8")
    value = msg.value().decode("utf-8")

    logger.info(
        "Consumed - topic {topic}: key = {key} value = {value}".format(
            topic=topic, key=key, value=f"{value}"
        )
    )

    obj: EventObject = EventObject.decode(value)
    obj.update_audit_log()
    return obj


def handle_multiprocess(pipe, logger: logging.Logger, msg):
    obj = handle(logger, msg)
    pipe.send({"key": msg.key().decode("utf-8"), "value": obj})
