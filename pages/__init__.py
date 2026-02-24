from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

_EXPORTS: dict[str, str] = {
    "AddRemoveElementsPage": "add_remove_elements_page",
    "ABTestPage": "ab_test_page",
    "BasicAuthPage": "basic_auth_page",
    "BrokenImagesPage": "broken_images_page",
    "ChallengingDomPage": "challenging_dom_page",
    "CheckboxesPage": "checkboxes_page",
    "ContextMenuPage": "context_menu_page",
    "DigestAuthPage": "digest_auth_page",
    "DisappearingElementsPage": "disappearing_elements_page",
    "DragAndDropPage": "drag_and_drop_page",
    "DropdownPage": "dropdown_page",
    "DynamicContentPage": "dynamic_content_page",
    "DynamicLoadingPage": "dynamic_loading_page",
    "EntryAdPage": "entry_ad_page",
    "HomePage": "homepage",
    "LandingPage": "landing_page",
    "LoginPage": "login_page",
    "SecureAreaPage": "secure_area_page",
    "ExitIntentPage": "exit_intent_page",
    "FileDownloadPage": "file_download_page",
    "FileUploadPage": "file_upload_page",
    "FloatingMenuPage": "floating_menu_page",

}

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