from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from ._BaseKeyword import _BaseKeyword
from . import utils
from . import validators


class PerformLongPress(_BaseKeyword):
    """
    Library for performing long press actions on elements using Appium.
    Provides keywords for mobile automation requiring long press gestures.
    """

    @keyword("Perform Long Press")
    def perform_long_press(self, locator, duration=1000):
        """Perform a long press gesture on a mobile element.

        Locates an element using the given locator strategy and value, then
        performs a long press gesture on it for the specified duration.

        [Arguments]
        locator    Element locator in format 'strategy=value'. Supported strategies:
                  id, xpath, accessibility_id, class name, css selector, name
        duration   Time in milliseconds to hold the press (default 1000)

        [Return Values]
        None. Passes if gesture is performed successfully.

        [Raises]
        ValueError     If locator is None, empty or malformed
                      If strategy is not supported
                      If element cannot be found
                      If duration is not a positive number
        RuntimeError   If Appium driver is not initialized
                      If gesture cannot be performed
        """
        validators.validate_locator(locator)
        duration = int(duration)
        validators.validate_type(duration, "duration", int)
        validators.validate_range(duration, "duration", min_val=1)

        driver = self.driver
        if not driver:
            raise RuntimeError("Appium driver is not available.")

        element = utils.find_element(self.appium_lib, locator)

        actions = ActionChains(driver)
        actions.click_and_hold(element).pause(duration/1000).release().perform()
