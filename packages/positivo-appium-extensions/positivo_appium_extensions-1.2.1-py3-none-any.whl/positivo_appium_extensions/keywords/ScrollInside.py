"""
Scroll Inside Library — Robot Framework + Appium

Performs scroll/swipe gestures (`mobile: swipeGesture`) inside a scrollable element.
Configurable `direction`, `percent` (0.01–1.0) and `speed` (ms). Reuses AppiumLibrary session.
"""


from robot.api.deco import keyword
from ._BaseKeyword import _BaseKeyword
from . import utils
from . import validators

# Defines the custom keyword class
class ScrollInside(_BaseKeyword):
    # Defines the library scope as GLOBAL (same instance will be reused across all tests)
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @keyword("Scroll Inside")
    def scroll_inside(self, *args, **kwargs):
        """
        Perform a scroll/swipe gesture inside a single scrollable element using `mobile: swipeGesture`.

        [Arguments]
        - locator: (str) Target element locator. Single positional string like `xpath=//...`
          or a named argument using one of: `id`, `xpath`, `accessibility_id`, `class_name`,
          `android_uiautomator`, `ios_predicate`, `ios_class_chain`, `name`.
        - direction: (str) One of `up`, `down`, `left`, `right`. Default: `down`.
        - percent: (float) Distance as a fraction of the element size in `0.01..1.0`. Default: `0.75`.
        - speed: (int) Gesture speed in milliseconds. Must be positive. Default: `800`.

        [Return Values]
        - None

        [Raises]
        - ValueError: Invalid locator, unsupported direction, or percent out of range.
        - TypeError: Parameters that cannot be converted to the expected types.
        - Exception: Driver/runtime failures propagated from the underlying Appium call.
        """

        locator = utils.get_locator(args, kwargs)

        # If still no valid locator, raise an error
        if not locator:
            raise ValueError(
                "Locator not provided. Use a positional argument like 'id=my_id' or a named argument like 'xpath=//button'."
            )

        # Read optional parameters
        direction = kwargs.get("direction", "down")       # Scroll direction
        percent = float(kwargs.get("percent", 0.75))      # Scroll percentage (0.01 to 1.0)
        speed = int(kwargs.get("speed", 800))             # Gesture speed in milliseconds

        # Validate direction and limits
        validators.validate_string_choice(direction, "direction", ["up", "down", "left", "right"])
        validators.validate_range(percent, "percent", 0.01, 1.0)
        validators.validate_range(speed, "speed", min_val=1)

        try:
            # Get driver and AppiumLibrary instance
            driver = self.driver
            if not driver:
                raise RuntimeError("Appium driver is not available.")

            # Find the element on screen using the provided locator
            element = utils.find_element(self.appium_lib, locator)

            # Adjust only vertical directions (Appium interprets as finger movement)
            gesture_direction = direction
            if direction == "down":
                gesture_direction = "up"    # To scroll content down, finger goes up
            elif direction == "up":
                gesture_direction = "down"  # To scroll content up, finger goes down

            driver.execute_script("mobile: swipeGesture", {
                "elementId": element.id,
                "direction": gesture_direction,
                "percent": percent,
                "speed": speed
            })

            # Log success message
            self._builtin.log(
                f"[SUCCESS] Scroll performed with locator='{locator}', direction='{direction}', percent={percent}, speed={speed}",
                "INFO"
            )

        except Exception as e:
            # Log error and raise it so Robot Framework can handle it properly
            self._builtin.log(f"[ERROR] Scroll failed: {str(e)}", "ERROR")
            raise
