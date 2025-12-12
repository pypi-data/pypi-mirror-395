"""
Swipe Element Library — Robot Framework + Appium 

Performs swipes (`mobile: dragGesture`) on elements with configurable `direction`,
`percent` (0.01-2.0) and `speed` (ms). Applies a fixed 5% start margin.
Reuses the active AppiumLibrary session.
"""

from robot.api.deco import keyword
from ._BaseKeyword import _BaseKeyword
from . import utils
from . import validators


class SwipeElement(_BaseKeyword):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @keyword("Swipe Element")
    def swipe_element(self, *args, **kwargs):
        """
        Perform a directional swipe on a single UI element using `mobile: dragGesture` with a fixed 5% start margin.

        [Arguments]
        - locator: (str) Target element locator. Can be a single positional string like `xpath=//...`
          or a named argument using one of: `id`, `xpath`, `accessibility_id`, `class_name`,
          `android_uiautomator`, `ios_predicate`, `ios_class_chain`, `name`.
        - direction: (str) One of `up`, `down`, `left`, `right`. Default: `right`.
        - percent: (float) Distance as a fraction of the element size in `0.01..2.0`.
          Values > 1.0 allow movement beyond the element bounds. Default: `0.5`.
        - speed: (int) Gesture speed in milliseconds for `mobile: dragGesture`. Must be positive. Default: `800`.

        [Return Values]
        - None

        [Raises]
        - ValueError: Invalid locator, unsupported direction, or percent out of range.
        - TypeError: Parameters that cannot be converted to expected types.
        - RuntimeError: Driver/runtime failures may propagate from the underlying call.
        """

        # Use custom locator parsing
        locator = utils.get_locator(args, kwargs)

        # Validate locator
        if not locator:
            raise ValueError(
                "Locator not provided. Use a positional argument like 'id=my_id' or a named argument like 'xpath=//button'."
            )



        # Read optional parameters
        direction = kwargs.get("direction", "right")
        percent = float(kwargs.get("percent", 0.5))
        speed = int(kwargs.get("speed", 800))

        validators.validate_string_choice(direction, "direction", ["up", "down", "left", "right"])
        validators.validate_range(percent, "percent", 0.01, 2.0)
        validators.validate_range(speed, "speed", min_val=1)

        # Find element and get its dimensions
        driver = self.driver
        if not driver:
            raise RuntimeError("Appium driver is not available.")
        element = utils.find_element(self.appium_lib, locator)
        rect = element.rect

        # Set a fixed start margin to avoid touching the edge of the element
        start_margin = 0.05

        # Calculate coordinates and perform drag based on direction
        if direction in ["left", "right"]:
            start_x = rect["x"] + rect["width"] * start_margin
            end_x = rect["x"] + rect["width"] * percent
            y = rect["y"] + rect["height"] / 2

            driver.execute_script(
                "mobile: dragGesture",
                {"startX": round(start_x), "startY": round(y), "endX": round(end_x), "endY": round(y), "speed": speed},
            )

        elif direction in ["up", "down"]:
            x = rect["x"] + rect["width"] / 2

            start_y = rect["y"] + rect["height"] * start_margin
            end_y = rect["y"] + rect["height"] * percent

            # Invert only for 'up' (Y axis increases downward)
            if direction == "up":
                start_y, end_y = end_y, start_y

            driver.execute_script(
                "mobile: dragGesture",
                {"startX": round(x), "startY": round(start_y), "endX": round(x), "endY": round(end_y), "speed": speed},
            )

        # Log success
        self._builtin.log(f"[SUCCESS] Drag performed to {direction} with percent={percent}, speed={speed}", "INFO")
