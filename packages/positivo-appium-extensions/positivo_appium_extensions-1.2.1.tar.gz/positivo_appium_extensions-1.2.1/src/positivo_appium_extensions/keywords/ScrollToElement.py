"""
Scroll To Element

Scrolls the mobile screen or a container element until the specified target element becomes visible.
Uses swipe gestures internally through Appium.

This keyword repeatedly performs swipe gestures in the specified direction until the target element
is located or the maximum number of swipes is reached.

The keyword allows control of swipe direction, distance, duration, and number of attempts.
It can also restrict scrolling inside a specific container element.

Example:
    | Scroll To Element | id=login-button | max_swipes=7 | direction=down | swipe_distance_ratio=0.4 | duration=500 |
    | Scroll To Element | xpath=//android.widget.TextView[@text="Settings"] | direction=up | max_swipes=5 |
    | Scroll To Element | accessibility_id=NextButton | direction=right | container_locator=id=listContainer |

[Arguments]
    | locator              | (string) Locator of the target element to be found. Required. |
    | max_swipes           | (integer) Maximum number of swipes before failing. Default is 5. |
    | direction            | (string) Scroll direction: "down", "up", "left", or "right". Default is "down". |
    | swipe_distance_ratio | (float) Fraction of screen or container size for each swipe. Valid range: 0.1–0.99. Default is 0.4. |
    | duration             | (integer) Duration of each swipe in milliseconds. Default is 500. |
    | container_locator    | (string) Locator of the container element where scrolling is performed. Optional. |

[Return Values]
    None. The keyword stops when the target element becomes visible or raises an exception if it cannot be found.

[Raises]
    | ValueError   | If invalid parameters are provided (e.g., invalid direction or ratio). |
    | RuntimeError | If the target element is not found after the maximum number of swipes. |

Notes:
    - The keyword stops as soon as the target element becomes visible.
    - If a container locator is provided, scrolling occurs only inside that element.
    - Uses the Appium "mobile: swipeGesture" command internally.
"""
import warnings
import time
from robot.api.deco import keyword
from ._BaseKeyword import _BaseKeyword
from . import utils
from . import gestures
from . import validators


class ScrollToElement(_BaseKeyword):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def _is_element_visible(self, locator):
        try:
            appium_lib = self._builtin.get_library_instance("AppiumLibrary")
            element = appium_lib._element_find(locator, True, True)
            return element.is_displayed()
        except:
            return False

    @keyword("Scroll To Element")
    def scroll_into_element(self, locator, max_swipes=5, direction="down", swipe_distance_ratio=0.4,
                            duration=500, container_locator=None):
        """
        Swipes vertically or horizontally (optionally within a container element) until the target element is visible.

        Args:
            locator (str): Target element to find.
            max_swipes (int): Maximum number of swipes to attempt.
            direction (str): 'down', 'up', 'left', or 'right'.
            swipe_distance_ratio (float): Fraction of screen/container size to swipe (0.1 to 0.99).
            duration (int): Duration of the swipe in milliseconds.
            container_locator (str): Optional. Element within which the swipe should be confined.
        """

        # --- Validation section ---
        max_swipes = int(max_swipes)
        validators.validate_type(max_swipes, "max_swipes", int)
        validators.validate_range(max_swipes, "max_swipes", min_val=1)

        direction = direction.lower()
        validators.validate_string_choice(direction, "direction", ["down", "up", "left", "right"])

        swipe_distance_ratio = float(swipe_distance_ratio)
        validators.validate_type(swipe_distance_ratio, "swipe_distance_ratio", float)
        validators.validate_range(swipe_distance_ratio, "swipe_distance_ratio", 0.01, 1.0)
        if swipe_distance_ratio == 1.0:
            swipe_distance_ratio = 0.99

        duration = int(duration)
        validators.validate_type(duration, "duration", int)
        validators.validate_range(duration, "duration", min_val=1)
        if duration > 5000:
            warnings.warn(
                f"Duration {duration}ms is unusually long; consider values below 5000ms for performance.")

        container_element = None
        if container_locator:
            validators.validate_locator(container_locator)
            container_element = utils.find_element(self.appium_lib, container_locator)

        # --- End of validation section ---

        driver = self.driver
        screen_width, screen_height = utils.get_screen_size(driver)

        if container_element:
            self._builtin.log(f"Using swipe area from container: {container_locator}", "INFO")
            x, y, width, height = utils.get_element_area(container_element)
            center_x, center_y = utils.get_element_center(container_element)
        else:
            self._builtin.log("Using entire screen for swipe", "INFO")
            x, y, width, height = 0, 0, screen_width, screen_height
            center_x = screen_width // 2
            center_y = screen_height // 2

        swipe_distance_x = swipe_distance_ratio * width
        swipe_distance_y = swipe_distance_ratio * height

        start_x, start_y = 0, 0
        end_x, end_y = 0, 0

        if direction == "down":
            start_x, end_x = center_x, center_x
            start_y = y + height // 2 + swipe_distance_y / 2
            end_y = y + height // 2 - swipe_distance_y / 2
        elif direction == "up":
            start_x, end_x = center_x, center_x
            start_y = y + height // 2 - swipe_distance_y / 2
            end_y = y + height // 2 + swipe_distance_y / 2
        elif direction == "right":
            start_y, end_y = center_y, center_y
            start_x = x + width // 2 + swipe_distance_x / 2
            end_x = x + width // 2 - swipe_distance_x / 2
        elif direction == "left":
            start_y, end_y = center_y, center_y
            start_x = x + width // 2 - swipe_distance_x / 2
            end_x = x + width // 2 + swipe_distance_x / 2

        start_x, start_y = int(start_x), int(start_y)
        end_x, end_y = int(end_x), int(end_y)

        for attempt in range(max_swipes):
            self._builtin.log(f"[SwipeAttempt {attempt + 1}] Trying to locate '{locator}'", "DEBUG")

            if self._is_element_visible(locator):
                self._builtin.log(f"Element '{locator}' found on attempt {attempt + 1}", "INFO")
                return

            self._builtin.log(f"Swiping from ({start_x}, {start_y}) to ({end_x}, {end_y})", "DEBUG")
            gestures.perform_w3c_scroll(driver, start_x, start_y, end_x, end_y, duration)
            time.sleep(0.5)

        raise RuntimeError(f"Element '{locator}' not found after {max_swipes} swipe attempts.")
