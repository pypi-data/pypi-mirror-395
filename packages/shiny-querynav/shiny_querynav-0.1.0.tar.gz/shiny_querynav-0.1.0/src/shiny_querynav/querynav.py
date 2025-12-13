from __future__ import annotations

from typing import Optional
from urllib.parse import parse_qs

from htmltools import HTMLDependency
from shiny import reactive
from shiny import session as shiny_session
from shiny import ui

from . import __version__


def dependency() -> HTMLDependency:
    """
    Create the HTML dependency for shiny-querynav.

    This function returns an HTMLDependency object that registers the JavaScript
    handler for synchronizing navigation with URL search parameters. Include this
    dependency in your Shiny UI (typically within a navigation component).

    Returns
    -------
    HTMLDependency
        The HTML dependency object containing the JavaScript handler.

    Examples
    --------
    >>> from shiny import ui
    >>> from shiny_querynav import querynav
    >>>
    >>> app_ui = ui.page_fluid(
    ...     ui.navset_bar(
    ...         querynav.dependency(),
    ...         ui.nav_panel("Home", "content", value="home"),
    ...         ui.nav_panel("About", "content", value="about"),
    ...         id="nav"
    ...     )
    ... )
    """
    return HTMLDependency(
        name="shiny_querynav",
        version=__version__,
        source={"package": "shiny_querynav", "subdir": "www"},
        script=[{"src": "shiny_querynav.js"}],
    )


def sync(
    nav_id: str,
    *,
    param_name: Optional[str] = None,
    home_value: Optional[str] = None,
) -> None:
    """
    Synchronize a navigation component with URL search parameters.

    This function enables bidirectional synchronization between a Shiny navigation
    component (such as navset_bar, navset_tab, etc.) and URL search parameters:

    - When the user clicks a navigation panel, the URL is updated with the
      corresponding search parameter.
    - When the page loads with a search parameter in the URL, the navigation
      component automatically selects the matching panel.

    Must be called from within a Shiny server function.

    Parameters
    ----------
    nav_id : str
        The ID of the navigation component to synchronize (e.g., the `id` parameter
        passed to ui.navset_bar() or similar navigation functions).
    param_name : str, optional
        The name of the URL search parameter to use. If not provided, defaults to
        the value of `nav_id`.
    home_value : str, optional
        The navigation value that represents the "home" or default page. When this
        panel is selected, the search parameter will be removed from the URL instead
        of being set. This keeps the home page URL clean (e.g., "/" instead of "/?tab=home").
        If not provided, all navigation values will be shown in the URL.

    Returns
    -------
    None

    Examples
    --------
    >>> from shiny import App, ui
    >>> from shiny_querynav import querynav
    >>>
    >>> app_ui = ui.page_fluid(
    ...     ui.navset_bar(
    ...         querynav.dependency(),
    ...         ui.nav_panel("Home", "Welcome", value="home"),
    ...         ui.nav_panel("About", "About us", value="about"),
    ...         id="page"
    ...     )
    ... )
    >>>
    >>> def server(input, output, session):
    ...     # Sync navigation with URL parameter "p"
    ...     # URL will show / for home, ?p=about for about
    ...     querynav.sync("page", param_name="p", home_value="home")
    >>>
    >>> app = App(app_ui, server)

    Notes
    -----
    - The navigation panel values (specified by the `value` parameter in
      ui.nav_panel()) will be used as the search parameter values.
    - The URL is updated using window.history.replaceState(), so navigation
      changes don't create new browser history entries.
    - When home_value is set, navigating to that panel removes the search parameter,
      resulting in a clean URL.
    - Ensure querynav.dependency() is included in your UI before using this function.
    """
    sess = shiny_session.get_current_session()
    if sess is None:
        return

    input = sess.input
    param: str = param_name or nav_id
    nav_value = getattr(input, nav_id)

    @reactive.effect
    @reactive.event(nav_value)
    async def _send_message() -> None:
        value: Optional[str] = nav_value()
        if value is None:
            return

        # If this is the home value, send empty string to remove the parameter
        send_value: str = "" if value == home_value else value

        await sess.send_custom_message(
            "queryNav", {"name": param, "value": send_value}
        )

    @reactive.effect
    def _update_nav() -> None:
        search: str = sess.clientdata.url_search()
        qs: dict[str, list[str]] = parse_qs(search.lstrip(" ?"))
        values: Optional[list[str]] = qs.get(param)

        # If no parameter in URL and home_value is set, navigate to home
        if not values and home_value is not None:
            ui.update_navset(nav_id, selected=home_value)
            return

        if not values:
            return

        value: str = values[0]
        ui.update_navset(nav_id, selected=value)
