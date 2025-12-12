from robot.api.deco import keyword
from ._BaseKeyword import _BaseKeyword
from . import utils
from . import gestures
from . import validators


class TapAtPercentage(_BaseKeyword):
    """Class to tap at a specific point on the screen using percentage coordinates."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    @keyword("Tap At Percentage")
    def tap_at_percentage(self, x, y, duration=100):
        """
        Taps at a specific point on the screen using percentage coordinates.

        Args:
            x (float): X coordinate as a percentage of the screen (0.0 to 1.0).
            y (float): Y coordinate as a percentage of the screen (0.0 to 1.0).
            duration (int): Duration of the tap in milliseconds.
        """
        x = float(x)
        y = float(y)
        duration = int(duration)
        validators.validate_type(x, "x", float)
        validators.validate_type(y, "y", float)
        validators.validate_range(x, "x", 0.0, 1.0)
        validators.validate_range(y, "y", 0.0, 1.0)
        validators.validate_type(duration, "duration", int)
        validators.validate_range(duration, "duration", min_val=1)

        try:
            driver = self.driver
            if not driver:
                raise RuntimeError("Appium driver is not available.")

            screen_width, screen_height = utils.get_screen_size(driver)

            x_px = int(screen_width * x)
            y_px = int(screen_height * y)

            self._builtin.log(f"Tapping at ({x_px}, {y_px}) [percentages: ({x}, {y})]", level="INFO")

            gestures.perform_w3c_tap(driver, x_px, y_px, duration)

            self._builtin.log(f"Tap performed at ({x_px}, {y_px})", level="INFO")
            return True

        except Exception as e:
            raise RuntimeError(f"Error performing tap: {str(e)}")
