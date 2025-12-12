import time

from robot.api.deco import keyword
from ._BaseKeyword import _BaseKeyword
from . import utils
from . import gestures


class TapElementAtCoordinates(_BaseKeyword):
    """
    Library for performing clicks on elements at specific coordinates using Appium and W3C Actions.
    Supports both percentage and pixel offsets for flexible mobile automation.
    """

    @keyword("Tap Element At Coordinates")
    def tap_element_at_coordinates(self, locator, xoffset=0.5, yoffset=0.5):
        """Click on mobile element at specified coordinates using touch actions.
        Supports percentage or pixel offsets from element's top-left corner.

        [Arguments]
        locator    Element locator string (id=submit, xpath=//button, etc)
        xoffset    Horizontal offset from left edge (default 0.5)
                  Values 0-1: percentage of element width
                  Values >1: absolute pixels from left
        yoffset    Vertical offset from top edge (default 0.5)
                  Values 0-1: percentage of element height 
                  Values >1: absolute pixels from top

        [Returns]
        None. Keyword passes if click action completes successfully.

        [Raises]
        RuntimeError    When Appium driver is not initialized
        ValueError     When element is not found
                      When offsets are not valid numbers
                      When click position is outside screen
        """
        driver = self.driver

        self._builtin.log("Checking if driver is active", level="INFO")
        if not driver:
            raise RuntimeError("Driver is not initialized or not connected to the device.")

        self._builtin.log(f"Searching for element with locator: {locator}", level="INFO")
        element = utils.find_element(self.appium_lib, locator)

        el_x, el_y, el_width, el_height = utils.get_element_area(element)
        self._builtin.log(f"Element area: x={el_x}, y={el_y}, width={el_width}, height={el_height}", level="INFO")

        xoffset = float(xoffset)
        yoffset = float(yoffset)

        screen_width, screen_height = utils.get_screen_size(driver)
        # If offset is between 0 and 1, treat as percentage
        if 0 <= xoffset <= 1:
            xoffset_px = int(el_width * xoffset)
        else:
            xoffset_px = int(xoffset)

        if 0 <= yoffset <= 1:
            yoffset_px = int(el_height * yoffset)
        else:
            yoffset_px = int(yoffset)

        # Final click coordinate on the screen
        x = el_x + xoffset_px
        y = el_y + yoffset_px
        self._builtin.log(
            f"Calculated click coordinates: ({x}, {y}) (offsets: {xoffset_px}, {yoffset_px})", level="INFO"
        )

        self._builtin.log(f"Screen size: width={screen_width}, height={screen_height}", level="INFO")

        if not (0 <= x <= screen_width and 0 <= y <= screen_height):
            raise ValueError(f"Coordinates ({x}, {y}) are out of device screen bounds.")

        self._builtin.log("Performing click using W3C Actions", level="INFO")
        gestures.perform_w3c_tap(driver, x, y, duration_ms=200)
        self._builtin.log("Click performed successfully via W3C Actions", level="INFO")
