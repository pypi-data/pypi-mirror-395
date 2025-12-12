from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton


def perform_w3c_tap(driver, x, y, duration_ms=100):
    """
    Executa um toque (tap) em coordenadas específicas usando W3C Actions.
    """
    actions = ActionChains(driver)
    finger = actions.w3c_actions.add_pointer_input("touch", "finger")

    finger.create_pointer_move(x=int(x), y=int(y))
    finger.create_pointer_down(button=MouseButton.LEFT)
    finger.create_pause(duration_ms / 1000)
    finger.create_pointer_up(button=MouseButton.LEFT)

    actions.perform()


def perform_w3c_scroll(driver, start_x, start_y, end_x, end_y, duration_ms=500):
    """
    Executa uma rolagem (scroll/swipe) usando W3C Actions.
    """
    actions = ActionChains(driver)
    finger = actions.w3c_actions.add_pointer_input("touch", "finger")

    finger.create_pointer_move(duration=0, x=int(start_x), y=int(start_y))
    finger.create_pointer_down(button=MouseButton.LEFT)
    finger.create_pointer_move(duration=duration_ms, x=int(end_x), y=int(end_y))
    finger.create_pointer_up(button=MouseButton.LEFT)

    actions.perform()