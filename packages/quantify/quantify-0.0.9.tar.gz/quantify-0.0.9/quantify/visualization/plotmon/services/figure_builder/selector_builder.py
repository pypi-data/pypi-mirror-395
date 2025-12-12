# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""
selector_builder module: Provides a builder for
Bokeh dropdown selectors for Plotmon applications.
"""

from collections.abc import Callable

from bokeh.events import MenuItemClick
from bokeh.models import Dropdown, FlexBox

from quantify.visualization.plotmon.utils.tuid_data import TuidData


def get_prev_selector_from_layout(current_layout: FlexBox | None) -> Dropdown | None:
    """
    Extract the previous selector from the current layout if it exists.
    Parameters.
    ----------
    current_layout : Column | None
        The current Bokeh layout of the application.
    Returns.
    -------
    Dropdown | None
        The previous Dropdown selector if found, else None.
    """
    if not (current_layout and current_layout.document):
        return None
    select = current_layout.document.get_model_by_name("experiment_select")
    if not isinstance(select, Dropdown):
        return None

    return select


def build_selector(
    tuids: TuidData,
    on_select_callback: Callable = lambda menu_item: print(
        f"Selection changed: {menu_item.item}"
    ),
    titles: dict[int, str] | None = None,
    selector: Dropdown | None = None,
) -> Dropdown:
    """
    Build or update the dropdown selector.
    Parameters.
    ----------
    tuids : TuidData
        TUID related data for the application.
    """
    if titles is None:
        titles = {}
    disabled = tuids.active_tuid != ""
    if selector:
        selector.disabled = disabled
        selector.update(
            menu=list(map(lambda item: (item[1], str(item[0])), titles.items()))
        )
        return selector

    selector = Dropdown(
        name="experiment_select",
        menu=list(map(lambda item: (item[1], str(item[0])), titles.items())),
        disabled=disabled,
        label="Archives",
        button_type="primary",
        width=300,
        height=50,
        styles={"margin-left": "auto", "margin-top": "auto", "font-size": "larger"},
    )

    selector.on_event(MenuItemClick, on_select_callback)
    return selector
