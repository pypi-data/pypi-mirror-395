"""Perform Zoom
        =======================

        Performs a realistic zoom-in (pinch-out) gesture on a specific element or at the
        center of the screen when no locator is provided. Simulates a two-finger gesture
        expanding outward, using Selenium W3C Pointer Actions integrated with Appium.

        [Arguments]
        -----------
        - ``locator``: Locator of the element to perform the zoom gesture on.
          Supports ``id``, ``xpath``, ``accessibility_id`` and ``class_name``.
          If omitted, the gesture is applied at the screen center.
        - ``scale``: Zoom scale factor (must be greater than 1.0). Defines the
          proportional distance each finger will move from the center. Default is ``1.5``.
        - ``duration``: Duration of the zoom gesture in milliseconds. Default is ``500``.
        - ``direction``: Orientation of finger movement, either ``vertical`` or ``horizontal``.
          Default is ``vertical``.
        - ``movement``: Distance (in pixels) that each finger travels from the center.
          Default is ``300``.
        - ``pause``: Pause time in seconds before the movement begins. Default is ``0.1``.
        - ``steps``: Number of incremental interpolation steps used to create a smooth,
          realistic gesture. Default is ``50``.

        [Return Values]
        ---------------
        - Returns ``True`` if the zoom gesture completes successfully.
        - Raises an exception if any validation or execution step fails.

        [Raises]
        --------
        - ``ValueError``: If invalid arguments are provided (e.g., ``scale`` ≤ 1.0,
          negative duration or movement, malformed locator).
        - ``RuntimeError``: If the Appium driver is unavailable, the element cannot
          be located, or any gesture execution error occurs.

        [Examples]
        ----------
        | Perform Zoom | locator=id=map_view | scale=1.8 | duration=700 | direction=vertical | movement=280 |
        | Perform Zoom | scale=2.0 | direction=horizontal | movement=300 | steps=60 |
        | Perform Zoom | locator=xpath=//android.view.View[@content-desc="photo"] | scale=1.6 |

        [Notes]
        -------
        - Uses Selenium W3C Pointer Actions under Appium for realistic multi-touch simulation.
        - If ``locator`` is provided, zoom occurs around the element’s center; otherwise, around
          the screen’s center.
        - Finger coordinates are constrained within screen bounds to prevent invalid gestures.
        - To perform the opposite gesture (zoom-out), use the ``Pinch`` keyword.
"""

import random

from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from ._BaseKeyword import _BaseKeyword
from . import utils
from . import validators


class PerformZoom(_BaseKeyword):
    """Custom Gesture Extension Class for AppiumLibrary with enhanced zoom gesture."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def _calculate_finger_final_positions(self, x, y, scale, movement, direction):
        # Defines the final finger positions based on gesture center, scale, and movement range
        displacement = scale * movement
        if direction == "vertical":
            return (x, y - displacement), (x, y + displacement)
        else:
            return (x - displacement, y), (x + displacement, y)

    def _validate_zoom_args(self, locator, scale, duration, direction, movement, pause, steps):
        # Validates gesture arguments for correctness and safety
        if locator is not None:
            validators.validate_locator(locator)

        scale = float(scale)
        validators.validate_type(scale, "scale", float)
        validators.validate_range(scale, "scale", min_val=1.001)

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

        return direction  # Return normalized direction for reuse

    @keyword("Perform Zoom")
    def perform_zoom(
        self, locator=None, scale=1.5, duration=500, direction="vertical", movement=300, pause=0.1, steps=50
    ):
        """
        Performs a realistic zoom gesture with perturbation.
        """

        direction = self._validate_zoom_args(locator, scale, duration, direction, movement, pause, steps)

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

            offset = 10
            f1_start = (center_x, center_y - offset) if direction == "vertical" else (center_x - offset, center_y)
            f2_start = (center_x, center_y + offset) if direction == "vertical" else (center_x + offset, center_y)

            f1_end, f2_end = self._calculate_finger_final_positions(center_x, center_y, scale, movement, direction)

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
            self._builtin.log("Zoom gesture performed successfully.", "INFO")

        except Exception as e:
            raise RuntimeError(f"Error while performing the zoom gesture: {str(e)}")
