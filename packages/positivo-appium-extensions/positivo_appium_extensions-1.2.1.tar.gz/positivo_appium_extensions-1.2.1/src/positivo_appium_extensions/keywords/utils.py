import warnings


def find_element(appium_lib, locator):
    """Encontra um elemento de forma segura."""
    element = appium_lib._element_find(locator, True, False)
    if not element:
        raise RuntimeError(f"Element not found for locator: {locator}")
    return element


def get_screen_size(driver):
    """Retorna o tamanho da tela (width, height)."""
    size = driver.get_window_size()
    return size["width"], size["height"]


def get_element_area(element):
    """Retorna a localização e o tamanho de um elemento."""
    location = element.location
    size = element.size
    return location["x"], location["y"], size["width"], size["height"]


def get_element_center(element):
    """Calcula o ponto central de um elemento."""
    x, y, width, height = get_element_area(element)
    return x + width / 2, y + height / 2


def adjust_to_screen_bounds(positions, screen_width, screen_height):
    """Garante que as coordenadas dos dedos estejam dentro dos limites da tela."""
    adjusted_positions = []
    for x, y in positions:
        new_x = max(0, min(x, screen_width))
        new_y = max(0, min(y, screen_height))
        if (x, y) != (new_x, new_y):
            warnings.warn(f"Finger position ({x}, {y}) adjusted to ({new_x}, {new_y}) to fit within screen bounds.")
        adjusted_positions.append((new_x, new_y))
    return adjusted_positions


def get_locator(args, kwargs):
    """
    Extracts the locator from args or kwargs, supporting AppiumLibrary-style strategies.
    
    Strategies supported via kwargs:
    - id
    - xpath
    - accessibility_id
    - class_name
    - android_uiautomator
    - ios_predicate
    - ios_class_chain
    - name
    
    If a positional argument is provided, it is assumed to be the locator (e.g., "id=my_element").
    """
    if args:
        return args[0]
    
    # Check known strategies in kwargs
    strategies = [
        "id", "xpath", "accessibility_id", "class_name", 
        "android_uiautomator", "ios_predicate", "ios_class_chain", 
        "name", "css", "link"
    ]
    
    for strategy in strategies:
        if strategy in kwargs:
            return f"{strategy}={kwargs[strategy]}"
            
    # Fallback/Check for explicit 'locator' kwarg
    if "locator" in kwargs:
        return kwargs["locator"]
        
    return None
