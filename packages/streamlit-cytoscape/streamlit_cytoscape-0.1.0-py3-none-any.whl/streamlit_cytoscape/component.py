import os
import streamlit.components.v1 as components
from typing import Optional, Union, Callable, Literal, Dict, Any, List

from streamlit_cytoscape.layouts import LAYOUTS
from streamlit_cytoscape.styles import NodeStyle, EdgeStyle
from streamlit_cytoscape.events import Event


_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_cytoscape",
        url="http://localhost:3001",  # For development
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "streamlit_cytoscape",
        path=build_dir,  # For distribution
    )


def streamlit_cytoscape(
    elements: Dict[str, Any],
    layout: Union[str, Dict[str, Any]] = "cose",
    node_styles: List[NodeStyle] = [],
    edge_styles: List[EdgeStyle] = [],
    height: int = 500,
    key: Optional[str] = None,
    on_change: Optional[Callable[..., None]] = None,
    node_actions: List[Literal["remove", "expand"]] = [],
    events: List[Event] = [],
) -> Any:
    """
    Renders a link analysis graph using Cytoscape in Streamlit.

    Parameters
    ----------
    elements : dict
        Graph elements data including nodes and edges. Each node
        should have an 'id', and 'label'. Each edge should have
        an 'id', 'source', 'target', and 'label'.
    layout : Union[str, dict], default 'cose'
        Layout configuration for Cytoscape. If a string is
        provided, it specifies the layout name. If a dictionary
        is provided, it should contain layout options. Default is
        "cose". A list of support layouts and default settings is
        available in `streamlit_cytoscape.layouts`
    node_styles : list[NodeStyle], default []
        A list of custom NodeStyle instances to apply styles to
        node groups in the graph
    edge_styles : list[EdgeStyle], default []
        A list of custom EdgeStyle instances to apply styles to
        edge groups in the graph
    height: int, default 500
        Component's height in pixels. NOTE: only defined once.
        Changing the value requires remounting the component.
    key : str, default None
        A unique key for the component. If provided, this key
        allows multiple instances of the component to exist in
        the same Streamlit app without conflicts. Setting this
        parameter is also important to avoid unnecessary
        re-rendering of the component.
    node_actions: list[Literal['remove', 'expand']], default []
        Specifies the actions to enable for nodes. Valid options
        are 'remove' and 'expand'. 'remove' allows nodes to be
        removed via delete keydown or a remove button click.
        'expand' allows nodes to be expanded via double-click or
        an expand button click. When any of these actions are
        triggered, the event information is sent back to the
        Streamlit app as the component's return value. CAUTION:
        keeping an edge with missing source or target IDs will
        lead to an error.
    events: list[Event], default []
        For advanced usage only. A list of events to listen to.
        When any of these events are triggered, the event
        information is sent back to the Streamlit app as the
        component's return value. NOTE: only defined once.
        Changing the list of events requires remounting the
        component.
    """
    node_styles_dump = [n.dump() for n in node_styles]
    edge_styles_dump = [e.dump() for e in edge_styles]
    style = node_styles_dump + edge_styles_dump

    height_str = str(height) + "px"

    if isinstance(layout, str):
        layout_config = LAYOUTS[layout]
    else:
        layout_config = layout

    events_dump = [e.dump() for e in events]

    return _component_func(
        elements=elements,
        style=style,
        layout=layout_config,
        height=height_str,
        key=key,
        on_change=on_change,
        nodeActions=node_actions,
        events=events_dump,
    )
