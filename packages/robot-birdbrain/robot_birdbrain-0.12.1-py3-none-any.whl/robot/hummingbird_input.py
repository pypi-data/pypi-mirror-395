from robot.constant import Constant
from robot.microbit_input import MicrobitInput
from robot.request import Request


class HummingbirdInput(Request):
    @classmethod
    def acceleration(self, device):
        """Gives the acceleration of X,Y,Z in m/sec2, relative
        to the Finch's position."""

        return MicrobitInput.acceleration(device)

    @classmethod
    def compass(self, device):
        """Returns values 0-359 indicating the orentation of the Earth's
        magnetic field, relative to the Finch's position."""

        return MicrobitInput.compass(device)

    @classmethod
    def magnetometer(self, device):
        """Return the values of X,Y,Z of a magnetommeter, relative to the Finch's position."""

        return MicrobitInput.magnetometer(device)

    @classmethod
    def orientation(self, device):
        """Return the orentation of the Hummingbird. Results found in Constant.HUMMINGBIRD_ORIENTATION_RESULTS"""

        return MicrobitInput.orientation(device)

    @classmethod
    def sensor(self, device, port):
        """Read the value of the sensor attached to a certain port."""

        sensor_options = {}
        sensor_options['min_response'] = Constant.DEFAULT_UNLIMITED_MIN_RESPONSE
        sensor_options['max_response'] = Constant.DEFAULT_UNLIMITED_MAX_RESPONSE
        sensor_options['type_method'] = 'float'

        return self.sensor_response(device, 'sensor', port, sensor_options)

    @classmethod
    def light(self, device, port):
        """Read the value of the light sensor attached to a certain port."""

        sensor_options = {}
        sensor_options['factor'] = Constant.LIGHT_FACTOR
        sensor_options['min_response'] = Constant.DEFAULT_MIN_RESPONSE
        sensor_options['max_response'] = Constant.DEFAULT_MAX_RESPONSE

        return self.sensor_response(device, 'sensor', port, sensor_options)

    @classmethod
    def sound(self, device, port):
        """Read the value of the sound sensor attached to a certain port."""

        port = str(port).lower()

        if port == "microbit" or port == "micro:bit":
            return MicrobitInput.sound(device)

        sensor_options = {}
        sensor_options['factor'] = Constant.SOUND_FACTOR
        sensor_options['min_response'] = Constant.DEFAULT_MIN_RESPONSE
        sensor_options['max_response'] = Constant.DEFAULT_MAX_RESPONSE

        return self.sensor_response(device, 'sensor', port, sensor_options)

    @classmethod
    def distance(self, device, port):
        """Read the value of the distance sensor attached to a certain port."""

        sensor_options = {}
        sensor_options['factor'] = Constant.DISTANCE_FACTOR
        sensor_options['min_response'] = Constant.DEFAULT_MIN_RESPONSE
        sensor_options['max_response'] = Constant.DEFAULT_UNLIMITED_MAX_RESPONSE

        return self.sensor_response(device, 'sensor', port, sensor_options)

    @classmethod
    def dial(self, device, port):
        """Read the value of the dial attached to a certain port."""

        sensor_options = {}
        sensor_options['factor'] = Constant.DIAL_FACTOR
        sensor_options['min_response'] = Constant.DEFAULT_MIN_RESPONSE
        sensor_options['max_response'] = Constant.DEFAULT_MAX_RESPONSE

        return self.sensor_response(device, 'sensor', port, sensor_options)

    @classmethod
    def voltage(self, device, port):
        """Read the value of  the dial attached to a certain port."""

        sensor_options = {}
        sensor_options['factor'] = Constant.VOLTAGE_FACTOR
        sensor_options['min_response'] = Constant.VOLTAGE_MIN
        sensor_options['max_response'] = Constant.VOLTAGE_MAX
        sensor_options['type_method'] = 'float'

        return self.sensor_response(device, 'sensor', port, sensor_options)
