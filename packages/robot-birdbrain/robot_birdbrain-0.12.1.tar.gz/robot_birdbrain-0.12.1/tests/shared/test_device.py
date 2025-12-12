import pytest
import random

from robot.device import Device
from robot.exception import Exception
from time import sleep

def test_none_device():
    with pytest.raises(Exception) as e:
        Device.connect(None)
    assert e.value.message == "Missing device name"


def test_bad_device():
    with pytest.raises(Exception) as e:
        Device.connect("Z")
    assert e.value.message == "Invalid device name: Z"


def test_stop_all():
    hummingbird = Device.connect()

    hummingbird.stop_all()


def test_default_connect():
    hummingbird = Device.connect()

    assert hummingbird.connected
    assert hummingbird.device == 'A'


def test_connect():
    hummingbird = Device.connect("A")

    assert hummingbird.connected
    assert hummingbird.device == 'A'


def test_connect_to_disconnected_device():
    with pytest.raises(Exception) as e:
        Device.connect("C", True)
    assert e.value.message == "No connection: C"


def test_connect_to_disconnected_device_no_exception():
    hummingbird = Device.connect("C", False)

    assert not hummingbird.connected
    assert hummingbird.device == 'C'


def test_connect_to_disconnected_device_with_exception():
    with pytest.raises(Exception) as e:
        Device.connect("C", True)
    assert e.value.message == "No connection: C"


def test_is_hummingbird():
    hummingbird = Device.connect("A")

    assert hummingbird.is_hummingbird


def test_is_finch():
    hummingbird = Device.connect("A")

    assert not hummingbird.is_finch()


def test_cache():
    hummingbird = Device.connect("A")

    assert hummingbird.get_cache("something_name") is None

    assert hummingbird.set_cache("something_name", "something") == "something"
    assert hummingbird.get_cache("something_name") == "something"

    assert "something_name" in hummingbird.state.cache

    assert hummingbird.set_cache("something_name", None) is None

    assert "something_name" not in hummingbird.state.cache

    assert hummingbird.get_cache("something_name") is None

    assert hummingbird.set_cache("set_not_in_the_cache", None) is None

def test_sleep():
    hummingbird = Device.connect('A')

    hummingbird.sleep(0.1)
