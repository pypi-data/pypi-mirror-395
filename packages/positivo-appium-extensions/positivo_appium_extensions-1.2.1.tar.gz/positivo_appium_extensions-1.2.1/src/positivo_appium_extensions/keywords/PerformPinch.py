"""
    Perform Pinch
    =====================

    Performs a pinch gesture on the specified element or at the screen center if no locator is provided.
    The gesture simulates a realistic "pinch" action by moving two fingers toward each other along a chosen axis.

    The gesture parameters such as scale, movement, duration, and direction are configurable.
    Optional pause and step interpolation can be used to adjust the smoothness of the gesture.

    Example:
        | Perform Pinch | id=imagePreview | scale=0.6 | duration=800 | direction=vertical | movement=350 |
        | Perform Pinch | xpath=//android.widget.ImageView | direction=horizontal | movement=300 | steps=40 |

    [Arguments]
        | locator   | (string) Element locator in the format strategy=value. Optional; if not provided, gesture occurs at screen center. |
        | scale     | (float) Scale of the gesture between 0.1 and less than 1.0. Defines the proportion of movement for each finger. Default is 0.5. |
        | duration  | (integer) Total duration of the gesture in milliseconds. Must be positive and below 5000 to prevent long blocking operations. Default is 500. |
        | direction | (string) Axis of the gesture: "vertical" or "horizontal". Default is "vertical". |
        | movement  | (integer or float) Distance, in pixels, that each finger moves during the gesture. Must be positive. Default is 400. |
        | pause     | (integer or float) Pause in seconds before movement begins. Must be ≥ 0. Default is 0.1. |
        | steps     | (integer) Number of interpolation steps to simulate smooth finger movement. Must be ≥ 1. Default is 50. |

    [Return Values]
        None. The keyword performs the gesture and logs a success message upon completion.

    [Raises]
        | ValueError   | If one or more arguments are invalid (e.g., out of range values or malformed locator). |
        | TypeError    | If an argument has an incorrect type (e.g., string instead of numeric). |
        | RuntimeError | If the gesture cannot be performed or the element is not found. |

    Notes:
        - Locators must follow the 'strategy=value' format. Supported strategies are: id, xpath, accessibility_id, class_name.
        - The gesture automatically adjusts finger positions to stay within screen boundaries.
        - If a locator is not specified, the gesture defaults to the screen center.
        - Minor random perturbations are applied to improve gesture realism.
"""

import random

from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from ._BaseKeyword import _BaseKeyword
from . import utils
from . import validators


class PerformPinch(_BaseKeyword):
    """Custom Gesture Extension Class for AppiumLibrary with enhanced pinch gesture."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def _calculate_finger_initial_positions(self, x, y, scale, movement, direction):
        # Defines the initial finger positions based on gesture center, scale, and movement range
        displacement = scale * movement
        if direction == "vertical":
            return (x, y - displacement), (x, y + displacement)
        else:
            return (x - displacement, y), (x + displacement, y)

    def _validate_pinch_args(self, locator, scale, duration, direction, movement, pause, steps):
        # Validates gesture arguments for correctness, types, and safety
        if locator is not None:
            validators.validate_locator(locator)

        scale = float(scale)
        validators.validate_type(scale, "scale", float)
        validators.validate_range(scale, "scale", 0.1, 0.999)

        duration = int(duration)
        validators.validate_type(duration, "duration", int)
        validators.validate_range(duration, "duration", 1, 5000)

        validators.validate_type(direction, "direction", str)
        direction = direction.lower()
        validators.validate_string_choice(direction, "direction", ["vertical", "horizontal"])

        movement = float(movement)
        validators.validate_type(movement, "movement", (int, float))
        validators.validate_range(movement, "movement", min_val=1)

        pause = float(pause)
        validators.validate_type(pause, "pause", (int, float))
        validators.validate_range(pause, "pause", min_val=0)

        steps = int(steps)
        validators.validate_type(steps, "steps", int)
        validators.validate_range(steps, "steps", min_val=1)

        return direction

    @keyword("Perform Pinch")
    def perform_pinch(self,locator=None,scale=0.5,duration=500,direction="vertical",movement=400,pause=0.1,steps=50):
        """
        Performs a realistic pinch gesture with perturbation.

        Args:
            locator (str): Element locator (optional; if None, uses screen center).
            scale (float): Gesture scale (0.1 to 1.0).
            duration (int): Total duration of the gesture in milliseconds.
            direction (str): Gesture direction ("vertical" or "horizontal").
            movement (int/float): Gesture amplitude in pixels.
            pause (int/float): Pause in seconds before movement begins.
            steps (int): Number of interpolation steps for gesture realism.
        """

        # Validate arguments with type and range enforcement
        direction = self._validate_pinch_args(locator, scale, duration, direction, movement, pause, steps)

        try:
            driver = self.driver
            if not driver:
                raise RuntimeError("The Appium driver is not available.")

            screen_width, screen_height = utils.get_screen_size(driver)

            if locator is None:
                center_x = screen_width / 2
                center_y = screen_height / 2
                self._builtin.log("No locator provided. Using center of the screen.", "INFO")
            else:
                element = utils.find_element(self.appium_lib, locator)
                center_x, center_y = utils.get_element_center(element)
                self._builtin.log(f"Element center at ({center_x}, {center_y})", "INFO")

            f1_start, f2_start = self._calculate_finger_initial_positions(center_x, center_y, scale, movement, direction)

            offset = 10
            if direction == "vertical":
                f1_end = (center_x, center_y - offset)
                f2_end = (center_x, center_y + offset)
            else:
                f1_end = (center_x - offset, center_y)
                f2_end = (center_x + offset, center_y)

            f1_start, f1_end, f2_start, f2_end = utils.adjust_to_screen_bounds(
                [f1_start, f1_end, f2_start, f2_end], screen_width, screen_height
            )

            self._builtin.log(f"Finger 1 starts at ({f1_start})", "INFO")
            self._builtin.log(f"Finger 2 starts at ({f2_start})", "INFO")

            actions = ActionChains(driver)
            actions.w3c_actions.devices = []
            finger1 = actions.w3c_actions.add_pointer_input("touch", "finger1")
            finger2 = actions.w3c_actions.add_pointer_input("touch", "finger2")

            finger1.create_pointer_move(x=f1_start[0], y=f1_start[1])
            finger2.create_pointer_move(x=f2_start[0], y=f2_start[1])

            finger1.create_pointer_down(button=MouseButton.LEFT)
            finger2.create_pointer_down(button=MouseButton.LEFT)

            finger1.create_pause(pause)
            finger2.create_pause(pause)

            for i in range(1, steps + 1):
                t = i / steps
                interp_f1_x = f1_start[0] + t * (f1_end[0] - f1_start[0])
                interp_f1_y = f1_start[1] + t * (f1_end[1] - f1_start[1])
                interp_f2_x = f2_start[0] + t * (f2_end[0] - f2_start[0])
                interp_f2_y = f2_start[1] + t * (f2_end[1] - f2_start[1])

                interp_f1_x, interp_f1_y = max(0, min(interp_f1_x, screen_width)), max(0, min(interp_f1_y, screen_height))
                interp_f2_x, interp_f2_y = max(0, min(interp_f2_x, screen_width)), max(0, min(interp_f2_y, screen_height))
                interp_f1_x = f1_start[0] + t * (f1_end[0] - f1_start[0]) + random.uniform(-0.0, 0.0)
                interp_f1_y = f1_start[1] + t * (f1_end[1] - f1_start[1]) + random.uniform(-0.0, 0.0)
                interp_f2_x = f2_start[0] + t * (f2_end[0] - f2_start[0]) + random.uniform(-0.0, 0.0)
                interp_f2_y = f2_start[1] + t * (f2_end[1] - f2_start[1]) + random.uniform(-0.0, 0.0)

                interp_f1_x, interp_f1_y = max(0, min(interp_f1_x, screen_width)), max(
                    0, min(interp_f1_y, screen_height)
                )
                interp_f2_x, interp_f2_y = max(0, min(interp_f2_x, screen_width)), max(
                    0, min(interp_f2_y, screen_height)
                )

                move_duration = int(duration / steps)
                finger1.create_pointer_move(x=interp_f1_x, y=interp_f1_y, duration=move_duration)
                finger2.create_pointer_move(x=interp_f2_x, y=interp_f2_y, duration=move_duration)

            finger1.create_pointer_up(button=MouseButton.LEFT)
            finger2.create_pointer_up(button=MouseButton.LEFT)

            actions.perform()
            self._builtin.log("Pinch gesture performed successfully.", "INFO")

        except Exception as e:
            raise RuntimeError(f"Error while performing the pinch gesture: {str(e)}")