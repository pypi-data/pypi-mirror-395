import time

from robot.api.deco import keyword
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from ._BaseKeyword import _BaseKeyword
from . import utils
from . import gestures
from . import validators


class ClickElements(_BaseKeyword):
    """Class to execute sequential clicks on multiple elements."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def _click_element(self, locator, click_duration):
        """
        Clicks on a specific element.
        
        Args:
            appium_lib: AppiumLibrary instance
            locator: Element locator string
            click_duration: Duration of click in milliseconds
            
        Returns:
            bool: True if click was successful, False otherwise
        """
        try:
            # Find element
            element = utils.find_element(self.appium_lib, locator)

            # Calculate center coordinates
            center_x, center_y = utils.get_element_center(element)

            # Execute click
            gestures.perform_w3c_tap(self.driver, center_x, center_y, click_duration)

            return True
        except NoSuchElementException:
            self._builtin.log(f"Element not found in DOM: {locator}", level='WARN')
            return False
        except StaleElementReferenceException:
            self._builtin.log(f"Element became stale: {locator}", level='WARN')
            return False
        except WebDriverException as wde:
            self._builtin.log(f"WebDriver error during click: {locator} - {str(wde)}", level='WARN')
            return False
        except Exception as e:
            self._builtin.log(f"Unexpected error during click: {locator} - {str(e)}", level='ERROR')
            return False

    @keyword("Click Elements")
    def click_elements(self, elements_list, click_duration=100, interval_between_clicks=0.5, stop_on_fail=False):
        """Clicks sequentially on multiple elements using Appium's touch actions.
        
        Executes clicks on each element in the provided list, in sequence. 
        If an element is not found, a WARN level log message is generated and the keyword 
        continues with the next element without failing. A delay between clicks can be configured.
        
        [Arguments]
        - ``elements_list``: List of element locators (id, xpath, accessibility_id, etc.)
        - ``click_duration``: Duration of each click in milliseconds (1-2000)
        - ``interval_between_clicks``: Time between clicks in seconds (must be non-negative)
        - ``stop_on_fail``: If True, stops execution on first click failure
        
        [Return Values]
        None. The keyword completes after all elements are clicked or attempted.
        
        [Examples]
        | @{elements}=    Create List    id=button1    xpath=//android.widget.TextView[@text="Submit"]
        | Click Elements    ${elements}    click_duration=200    interval_between_clicks=0.5
        
        | @{calculator_buttons}=    Create List    id=digit_1    id=digit_2    id=plus    id=equals
        | Click Elements    ${calculator_buttons}    stop_on_fail=True
        
        [Raises]
        - ``TypeError``: If parameters have incompatible types (non-list elements_list, non-numeric duration)
        - ``ValueError``: If parameter values are outside acceptable ranges (empty list, negative intervals)
        - ``RuntimeError``: If driver is unavailable or element operations fail
        """
        # Validation
        validators.validate_type(elements_list, "elements_list", list)
        if not elements_list:
            raise ValueError("The elements list cannot be empty - at least one locator is required")
        for item in elements_list:
            validators.validate_type(item, "element in elements_list", str)

        validators.validate_type(click_duration, "click_duration", (int, float))
        validators.validate_range(click_duration, "click_duration", min_val=1, max_val=2000)

        validators.validate_type(interval_between_clicks, "interval_between_clicks", (int, float))
        validators.validate_range(interval_between_clicks, "interval_between_clicks", min_val=0)

        stop_on_fail = self._builtin.convert_to_boolean(stop_on_fail)
        validators.validate_type(stop_on_fail, "stop_on_fail", bool)

        try:
            # Validate driver existence
            driver = self.driver
            if driver is None:
                raise RuntimeError("Appium driver is not available - ensure a session is started")

            # Validate driver session
            try:
                session_id = driver.session_id
                if not session_id:
                    raise RuntimeError("Appium driver session is not valid - session may have been closed")
                self._builtin.log(f"Driver session is valid (ID: {session_id})", level='DEBUG')
            except AttributeError:
                raise RuntimeError("Failed to validate Appium driver session - driver object is invalid")
            except Exception as session_error:
                raise RuntimeError(f"Failed to validate Appium driver session: {str(session_error)}")

            self._builtin.log(f"Starting sequential click on {len(elements_list)} elements", level='INFO')
            
            success_count = 0
            failed_count = 0
            failed_locators = []
            
            for i, locator in enumerate(elements_list, 1):
                self._builtin.log(f"Clicking element {i}/{len(elements_list)}: {locator}", level='INFO')
                success = self._click_element(locator, click_duration)
                
                if success:
                    success_count += 1
                    self._builtin.log(f"Click executed on element {i}: {locator}", level='INFO')
                else:
                    failed_count += 1
                    failed_locators.append(locator)
                    if stop_on_fail:
                        self._builtin.log(f"Stopping sequence due to click failure (stop_on_fail=True)", level='WARN')
                        break
                
                # Pause between clicks (except for the last one)
                if i < len(elements_list) and i < len(elements_list):
                    time.sleep(interval_between_clicks)
            
            # Log resumo final
            total_attempted = success_count + failed_count
            self._builtin.log(
                f"Click sequence completed: {success_count}/{total_attempted} successful, "
                f"{failed_count}/{total_attempted} failed.", 
                level='INFO'
            )
            
            if failed_count > 0:
                self._builtin.log(f"Failed locators: {failed_locators}", level='INFO')
                
        except (TypeError, ValueError) as e:
            # Re-raise parameter validation exceptions without modification
            raise
        except RuntimeError as e:
            # Re-raise runtime errors without modification
            raise
        except Exception as e:
            # Wrap other exceptions with detailed context
            raise RuntimeError(f"Error executing multiple clicks: {str(e)}")
