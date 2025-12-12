import time
import urllib.request

from robot.constant import Constant
from robot.exception import Exception
from robot.utility import Utility


class Request:
    @classmethod
    def uri(self, *args):
        return "http://127.0.0.1:30061/" + Utility.flatten_string(args)

    @classmethod
    def is_not_connected_response(self, response):
        return response.lower() == "not connected"

    @classmethod
    def response(self, *args):
        if "false" in args:
            return False

        try:
            if Constant.BIRDBRAIN_TEST:
                print("Test: URI", self.uri(*args))

            response_request = urllib.request.urlopen(self.uri(*args))
        except (ConnectionError, urllib.error.URLError, urllib.error.HTTPError):
            raise (Exception("Error: Request to device failed"))

        response = response_request.read().decode('utf-8').lower()

        if Constant.BIRDBRAIN_TEST:
            print("Test: response", response)

        if self.is_not_connected_response(response):
            raise (Exception("Error: The device is not connected"))

        time.sleep(0.01)  # hack to prevent http requests from overloading the BlueBird Connector

        return response

    @classmethod
    def response_status(self, *args):
        return Request.request_status(Request.response(args))

    @classmethod
    def is_connected(self, device):
        try:
            self.response('hummingbird', 'in', 'orientation', 'Shake', device)
        except Exception:
            return False

        return True

    @classmethod
    def is_not_connected(self, device):
        return not self.is_connected(device)

    @classmethod
    def stop_all(self, device):
        return self.request_status(self.response('hummingbird', 'out', 'stopall', device))

    @classmethod
    def request_status(self, status):
        if Constant.BIRDBRAIN_TEST:
            print("Test: request status is", status)

        if status is None:
            return None

        if status == 'true':
            return True
        if status == 'led set':
            return True
        if status == 'triled set':
            return True
        if status == 'servo set':
            return True
        if status == 'buzzer set':
            return True
        if status == 'symbol set':
            return True
        if status == 'print set':
            return True
        if status == 'all stopped':
            return True

        if status == 'finch moved':
            return True
        if status == 'finch turned':
            return True
        if status == 'finch wheels started':
            return True
        if status == 'finch wheels stopped':
            return True
        if status == 'finch encoders reset':
            return True

        if status == 'false':
            return False
        if status == 'not connected':
            return False
        if status == 'invalid orientation':
            return False
        if status == 'invalid port':
            return False

        return None

    @classmethod
    def calculate_angle(self, intensity):
        return int(int(intensity) * 255 / 180)

    @classmethod
    def calculate_intensity(self, intensity):
        return int(int(Utility.bounds(intensity, 0, 100)) * 255 / 100)

    @classmethod
    def calculate_speed(self, speed):
        if int(speed) in range(-10, 10):
            return 255

        # QUESTION: why this calculation instead of normal mapping to 0..255 (and 255 means stop)
        # return ((int(speed) * 23 / 100) + 122)

        if int(speed) < 0:
            return int(119 - (-int(speed) / 100 * 45))
        else:
            return int((int(speed) / 100 * 25) + 121)

    @classmethod
    def calculate_left_or_right(self, direction):
        if direction == Constant.LEFT:
            return 'Left'
        if direction == Constant.RIGHT:
            return 'Right'

        return 'None'

    @classmethod
    def validate(self, validate, valid_range, validate_message):
        if not str(validate) in valid_range:
            raise Exception(validate_message)

        return True

    @classmethod
    def validate_port(self, port, valid_range, allow_all=False):
        if allow_all and str(port) == 'all':
            return True

        return Request.validate(port, valid_range, f"Port {str(port)} out of range.")

    @classmethod
    def sensor_response(self, device, sensor, other=None, options={}):
        if other is False:
            return False  # for invalid directions

        factor = options["factor"] if "factor" in options else Constant.DEFAULT_FACTOR
        min_response = options["min_response"] if "min_response" in options else Constant.DEFAULT_UNLIMITED_MIN_RESPONSE
        max_response = options["max_response"] if "max_response" in options else Constant.DEFAULT_UNLIMITED_MAX_RESPONSE
        type_method = options["type_method"] if "type_method" in options else Constant.DEFAULT_TYPE_METHOD

        request = ['hummingbird', 'in', sensor]
        if other is not None:
            request.append(other)
        request.append(device)

        response = float(Request.response(request)) * factor

        response = round(Utility.decimal_bounds(response, min_response, max_response), 3)

        if type_method == 'int':
            return int(response)

        return response

    @classmethod
    def xyz_response(self, device, sensor, type_method='int'):
        x = round(float(Request.response('hummingbird', 'in', sensor, 'X', device)), 3)
        y = round(float(Request.response('hummingbird', 'in', sensor, 'Y', device)), 3)
        z = round(float(Request.response('hummingbird', 'in', sensor, 'Z', device)), 3)

        if type_method == 'int':
            return [int(x), int(y), int(z)]
        else:
            return [float(x), float(y), float(z)]

    @classmethod
    def tri_led_response(self, device, port, r_intensity, g_intensity, b_intensity, valid_range, allow_all=False):
        """Set TriLED  of a certain port requested to a valid intensity."""
        self.validate_port(port, valid_range, allow_all)

        calc_r = Request.calculate_intensity(r_intensity)
        calc_g = Request.calculate_intensity(g_intensity)
        calc_b = Request.calculate_intensity(b_intensity)

        return Request.response_status('hummingbird', 'out', 'triled', port, calc_r, calc_g, calc_b, device)

    @classmethod
    def orientation_response(self, device, sensor, orientations, orientation_results, orientation_in_between):
        for index, target_orientation in enumerate(orientations):
            response = self.response("hummingbird", "in", sensor, target_orientation, device)

            if response == "true":
                return orientation_results[index]

        return orientation_in_between
