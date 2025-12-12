import time

from robot.hummingbird import Hummingbird
from robot.hummingbird_output import HummingbirdOutput


def test_led():
    hummingbird = Hummingbird("A")

    HummingbirdOutput.led(hummingbird.device, 1, 50)
    time.sleep(0.15)

    HummingbirdOutput.led(hummingbird.device, 1, "0")


def test_tri_led():
    hummingbird = Hummingbird("A")

    HummingbirdOutput.tri_led(hummingbird.device, 1, 50, "50", 0)
    time.sleep(0.15)

    HummingbirdOutput.tri_led(hummingbird.device, 1, 0, 0, 0)


def test_position_servo():
    hummingbird = Hummingbird("A")

    HummingbirdOutput.position_servo(hummingbird.device, 1, 20)
    time.sleep(0.15)

    HummingbirdOutput.position_servo(hummingbird.device, 1, 160)
    time.sleep(0.15)


def test_rotation_servo():
    hummingbird = Hummingbird("A")

    HummingbirdOutput.rotation_servo(hummingbird.device, 2, 25)
    time.sleep(0.15)

    HummingbirdOutput.rotation_servo(hummingbird.device, "2", "-25")
    time.sleep(0.15)

    HummingbirdOutput.rotation_servo(hummingbird.device, 2, 0)
