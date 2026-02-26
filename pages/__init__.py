from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any


__all__ = sorted(_EXPORTS.keys())

def __getattr__(name: str) -> Any:
    module_name = _EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = import_module(f"{__name__}.{module_name}")

    try:
        value = getattr(module, name)
    except AttributeError as e:
        raise AttributeError(
            f"Module {module.__name__!r} does not define {name!r}"
        ) from e

    globals()[name] = value  # cache it
    return value


# IDE / type checker support (not executed at runtime)
if TYPE_CHECKING:
    from .add_remove_elements_page import AddRemoveElementsPage
    from .basic_auth_page import BasicAuthPage
    from .broken_images_page import BrokenImagesPage
    from .challenging_dom_page import ChallengingDomPage
    from .checkboxes_page import CheckboxesPage
    from .context_menu_page import ContextMenuPage
    from .digest_auth_page import DigestAuthPage
    from .disappearing_elements_page import DisappearingElementsPage
    from .drag_and_drop_page import DragAndDropPage
    from .dropdown_page import DropdownPage
    from .dynamic_content_page import DynamicContentPage
    from .dynamic_loading_page import DynamicLoadingPage
    from .landing_page import LandingPage
    from .login_page import LoginPage
    from .secure_area_page import SecureAreaPage