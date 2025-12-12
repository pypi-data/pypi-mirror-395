"""
robotframework-appium-extensions
================================
Additional keywords for Robot Framework's AppiumLibrary.

Developed within the Technology Residency Program, executed by CEPEDI,
coordinated by SOFTEX, and supported by MCTI, with the participation
of Positivo Tecnologia as the partner company that proposed the development challenge.

This package can be imported in two ways:
- Full import:     `Library    positivo_appium_extensions`
  → Loads all keywords automatically.

- Specific import: `Library    positivo_appium_extensions.keywords.ClickElements`
  → Loads only the desired keyword module.
"""

__version__ = "1.2.1"

from .keywords import get_all_keyword_classes


class positivo_appium_extensions(*get_all_keyword_classes()):
    """
    The `positivo_appium_extensions` library provides a set of custom keywords
    for mobile automation with Appium and Robot Framework.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__
