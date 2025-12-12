from src.kafka_broker import EventObject


def test_encoding():
    class SomeClass:
        ...

    data = {"thing": SomeClass()}
    event_object = EventObject(data=data)
    success = 1

    try:
        event_object.encode()

    except TypeError:
        success = 0

    finally:
        assert success == 0, "Should have failed"
