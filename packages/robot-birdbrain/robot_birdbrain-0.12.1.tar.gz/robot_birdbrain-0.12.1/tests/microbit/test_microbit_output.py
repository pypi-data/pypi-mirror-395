import pytest
import time

from robot.exception import Exception
from robot.microbit_output import MicrobitOutput
from robot.request import Request
from robot.state import State


def test_display():
    state = State()

    MicrobitOutput.display(state, "A", [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

    time.sleep(0.15)

    Request.stop_all("A")


def test_display_wrong_size():
    with pytest.raises(Exception) as e:
        state = State()

        list = [0, 1]

        MicrobitOutput.display(state, "A", list)
    assert e.value.message == "Error: display() requires a list of length 25"


def test_point_and_clear_display():
    state = State()

    for i in range(2):
        assert MicrobitOutput.point(state, "A", 1, 1, 1)
        assert MicrobitOutput.point(state, "A", 1, 5, 1)
        assert MicrobitOutput.point(state, "A", 5, 1, 1)
        assert MicrobitOutput.point(state, "A", 5, 5, 1)

        time.sleep(0.15)

        MicrobitOutput.clear_display(state, "A")


def test_point_true_or_false():
    state = State()

    assert MicrobitOutput.point(state, "A", 3, 3, True)

    time.sleep(0.15)

    assert MicrobitOutput.point(state, "A", 3, 3, False)


def test_point_out_of_range():
    with pytest.raises(Exception) as e:
        state = State()

        assert MicrobitOutput.point(state, "A", 999, 1, 1)
    assert e.value.message == "Error: point out of range"


def test_print():
    state = State()

    assert MicrobitOutput.print(state, "A", "B")
    time.sleep(1)

    assert MicrobitOutput.print(state, "A", " ")
    time.sleep(1)


def test_print_nothing():
    state = State()

    assert MicrobitOutput.print(state, "A", "")
    time.sleep(1)

    assert MicrobitOutput.print(state, "A", None)
    time.sleep(1)


def test_play_note():
    assert MicrobitOutput.play_note("A", 50, 0.25)
