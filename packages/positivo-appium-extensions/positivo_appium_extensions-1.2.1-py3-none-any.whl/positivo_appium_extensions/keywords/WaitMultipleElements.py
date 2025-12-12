import time
import re

from robot.api.deco import keyword
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
from ._BaseKeyword import _BaseKeyword
from . import validators


class WaitMultipleElements(_BaseKeyword):
    """Class to wait for multiple elements simultaneously."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # Estratégias de localização válidas
    VALID_STRATEGIES = ['id', 'xpath', 'accessibility_id', 'class_name', 'css selector', 'name', 
                        'android uiautomator', 'ios class chain', 'ios predicate']
    # Tempo máximo permitido para timeout (5 minutos)
    MAX_TIMEOUT = 300
    # Limite para exibição de elementos em logs
    MAX_LOG_ELEMENTS = 10

    def _validate_locator(self, locator):
        """
        Valida se um locator está no formato strategy=value e usa uma estratégia válida.
        """
        if not isinstance(locator, str):
            raise ValueError(f"Locator must be a string, got {type(locator).__name__}: {repr(locator)}")
            
        # Aceita xpath começando com // sem precisar de prefixo
        if locator.startswith('//'):
            return True
            
        # Verifica o formato strategy=value
        match = re.match(r'^([a-zA-Z_\s]+)=(.+)$', locator)
        if not match:
            raise ValueError(f"Invalid locator format: {locator}. Must be 'strategy=value' or start with '//'")
            
        strategy = match.group(1).lower().strip()
        if strategy not in self.VALID_STRATEGIES:
            valid_strategies_str = ', '.join(self.VALID_STRATEGIES)
            raise ValueError(f"Invalid strategy in locator '{locator}'. Valid strategies are: {valid_strategies_str}")
            
        return True
        
    def _check_elements_visibility(self, elements_list):
        """
        Verifica a visibilidade de cada elemento na lista.
        
        Args:
            elements_list: Lista de locators
            appium_lib: Instância da AppiumLibrary
            
        Returns:
            tuple: (resultados como dicionário, contagem de elementos visíveis)
        """
        results = {}
        visible_count = 0
        
        for locator in elements_list:
            try:
                element = self.appium_lib._element_find(locator, True, False)
                if element and element.is_displayed():
                    results[locator] = True
                    visible_count += 1
                    self._builtin.log(f"Element visible: {locator}", level='DEBUG')
                else:
                    results[locator] = False
                    self._builtin.log(f"Element found but not visible: {locator}", level='DEBUG')
            except StaleElementReferenceException:
                # Elemento estava no DOM mas foi removido
                results[locator] = False
                self._builtin.log(f"Element became stale: {locator}", level='DEBUG')
            except WebDriverException as wde:
                results[locator] = False
                self._builtin.log(f"WebDriver error for element: {locator} - {str(wde)}", level='DEBUG')
            except Exception as e:
                results[locator] = False
                self._builtin.log(f"Element not found or error: {locator} - {str(e)}", level='DEBUG')
                
        return results, visible_count

    def _format_element_list(self, elements, limit=None):
        """
        Formata uma lista de elementos para exibição em logs,
        limitando o número de itens exibidos.
        """
        if limit is None:
            limit = self.MAX_LOG_ELEMENTS
            
        if len(elements) <= limit:
            return str(elements)
        
        displayed = elements[:limit]
        return f"{displayed} e mais {len(elements) - limit} elemento(s)..."

    @keyword("Wait Multiple Elements")
    def wait_multiple_elements(self, elements_list, timeout=10, wait_for_all=True, polling_interval=0.5):
        """Waits for multiple elements to be visible with configurable strategies.
        
        Continuously polls for element visibility using the provided locators
        and applies different waiting strategies based on the wait_for_all parameter.
        
        [Arguments]
        - ``elements_list``: List of element locators in format 'strategy=value' or XPath starting with '//'
        - ``timeout``: Maximum time to wait in seconds (1-300)
        - ``wait_for_all``: If True, waits until ALL elements are visible; if False, waits until ANY element is visible
        - ``polling_interval``: Time between visibility checks in seconds (must be less than timeout)
        
        [Return Values]
        Dictionary with locator strings as keys and boolean visibility status as values:
        - True: Element is visible
        - False: Element is not visible
        
        [Examples]
        | @{locators}=    Create List    id=button1    xpath=//android.widget.TextView[@text="Submit"]
        | ${result}=      Wait Multiple Elements    ${locators}    timeout=15    wait_for_all=True
        | Should Be True  ${result['id=button1']}
        
        | @{locators}=    Create List    id=loading    id=error
        | ${result}=      Wait Multiple Elements    ${locators}    wait_for_all=False
        | Log             ${result}
        
        [Raises]
        - ``ValueError``: If parameters are invalid (empty list, malformed locators, invalid timeout values)
        - ``TimeoutError``: If elements do not become visible within the timeout period
        - ``RuntimeError``: If Appium driver is unavailable or session is invalid
        """
        # Input validation
        validators.validate_type(elements_list, "elements_list", list)
        if not elements_list:
            raise ValueError("The elements list cannot be empty")

        for idx, locator in enumerate(elements_list):
            try:
                self._validate_locator(locator)
            except ValueError as e:
                raise ValueError(f"Invalid locator at position {idx}: {str(e)}")

        timeout = float(timeout)
        validators.validate_type(timeout, "timeout", float)
        validators.validate_range(timeout, "timeout", 0.001, self.MAX_TIMEOUT)

        polling_interval = float(polling_interval)
        validators.validate_type(polling_interval, "polling_interval", float)
        validators.validate_range(polling_interval, "polling_interval", min_val=0.001)
        if polling_interval >= timeout:
            raise ValueError("polling_interval must be smaller than timeout")

        wait_for_all = self._builtin.convert_to_boolean(wait_for_all)
        validators.validate_type(wait_for_all, "wait_for_all", bool)

        try:
            # Validar disponibilidade do driver
            driver = self.driver
            if driver is None:
                raise RuntimeError("Appium driver is not available - ensure Appium session is initialized")
                
            # Validar sessão do driver
            try:
                session_id = driver.session_id
                if not session_id:
                    raise RuntimeError("Appium driver session is not valid - session may have been closed")
                self._builtin.log(f"Driver session is valid (ID: {session_id})", level='DEBUG')
            except Exception as session_error:
                raise RuntimeError(f"Failed to validate Appium driver session: {str(session_error)}")

            # Log uma versão limitada da lista para evitar poluição visual
            log_elements = self._format_element_list(elements_list)
            self._builtin.log(f"Starting wait for {len(elements_list)} elements to be visible: {log_elements} (wait_for_all={wait_for_all}, timeout={timeout}s)", level='INFO')
            
            # Usar time.monotonic para evitar problemas com alterações do relógio do sistema
            start_time = time.monotonic()
            attempt_count = 0
            
            while time.monotonic() - start_time < timeout:
                attempt_count += 1
                
                # Usar o método auxiliar para verificar visibilidade
                results, visible_elements = self._check_elements_visibility(elements_list)
                
                # Check success conditions
                if wait_for_all and visible_elements == len(elements_list):
                    elapsed_time = time.monotonic() - start_time
                    self._builtin.log(f"All {len(elements_list)} elements are visible (attempts: {attempt_count}, time: {elapsed_time:.2f}s)", level='INFO')
                    return results
                elif not wait_for_all and visible_elements > 0:
                    elapsed_time = time.monotonic() - start_time
                    self._builtin.log(f"{visible_elements} out of {len(elements_list)} elements are visible (attempts: {attempt_count}, time: {elapsed_time:.2f}s)", level='INFO')
                    return results
                
                # Log progress periodically (a cada 5 tentativas)
                if attempt_count % 5 == 0:
                    elapsed = time.monotonic() - start_time
                    remaining = max(0, timeout - elapsed)
                    self._builtin.log(f"Still waiting... Found {visible_elements}/{len(elements_list)} visible elements (attempts: {attempt_count}, elapsed: {elapsed:.2f}s, remaining: {remaining:.2f}s)", level='DEBUG')
                
                # Avoid unnecessary sleep on last iteration
                remaining_time = timeout - (time.monotonic() - start_time)
                if remaining_time > polling_interval:
                    time.sleep(polling_interval)
            
            # Timeout reached - use método auxiliar para resultado final
            elapsed_time = time.monotonic() - start_time
            final_results, visible_count = self._check_elements_visibility(elements_list)
            
            # More specific error messages
            if wait_for_all:
                visible_locators = [loc for loc, status in final_results.items() if status]
                missing_locators = [loc for loc, status in final_results.items() if not status]
                
                # Formatar listas para evitar mensagens muito grandes
                visible_str = self._format_element_list(visible_locators)
                missing_str = self._format_element_list(missing_locators)
                
                error_msg = f"Timeout waiting for all elements to be visible. Found {visible_count}/{len(elements_list)} visible elements after {attempt_count} attempts in {elapsed_time:.2f}s.\n"
                error_msg += f"Visible: {visible_str}\n"
                error_msg += f"Missing: {missing_str}"
                
                raise TimeoutError(error_msg)
            else:
                if visible_count == 0:
                    error_msg = f"Timeout waiting for any element to be visible. No visible elements found after {attempt_count} attempts in {elapsed_time:.2f}s"
                    raise TimeoutError(error_msg)
                else:
                    # Este caso não deveria acontecer, mas mantemos por segurança
                    return final_results
                    
        except WebDriverException as wde:
            raise RuntimeError(f"WebDriver error: {str(wde)}")
        except Exception as e:
            if isinstance(e, (TimeoutError, ValueError)):
                raise
            elif isinstance(e, RuntimeError) and "Appium driver" in str(e):
                raise
            elif "Invalid locator" in str(e):
                raise ValueError(str(e))
            else:
                raise RuntimeError(f"Error waiting for multiple elements visibility: {str(e)}")
