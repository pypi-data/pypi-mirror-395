from robot.libraries.BuiltIn import BuiltIn


class _BaseKeyword:
    """
    Classe base para todas as keywords, centralizando o acesso ao BuiltIn e AppiumLibrary.
    """

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @property
    def appium_lib(self):
        return self._builtin.get_library_instance("AppiumLibrary")