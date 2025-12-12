"""
Components package for template rendering.

This package contains various components that can be used to build templates.
"""
from typing import Dict, Any, Type, Optional
from .base import Component
from .text import TextComponent
from .image import ImageComponent
from .shapes import CircleComponent, RectangleComponent, PolygonComponent,RibbonFrame
from .buttons import CTAButtonComponent
from .footer import FooterComponent
from .button_group import CTAButtonGroupComponent
from .html import HTMLComponent
import copy

# Map of component types to their corresponding classes
COMPONENT_CLASSES: Dict[str, Type[Component]] = {
    "text": TextComponent,
    "image": ImageComponent,
    "circle": CircleComponent,
    "rectangle": RectangleComponent,
    "polygon": PolygonComponent,
    "cta_button": CTAButtonComponent,
    "footer": FooterComponent,
    "ribbon_frame": RibbonFrame,
    "cta_button_group": CTAButtonGroupComponent,
    "html": HTMLComponent
}


def create_component_from_config(config: Dict[str, Any], variables: Optional[Dict[str, Any]] = None) -> Optional[Component]:
    """
    Factory function to create a component from a configuration dictionary.

    Args:
        config: Configuration dictionary with a "type" field
        variables: Optional dictionary of variables to substitute in component content

    Returns:
        A component instance or None if the type is unknown
    """
    if not isinstance(config, dict):
        return None

    component_type = config.get("type")
    if not component_type:
        return None

    component_class = COMPONENT_CLASSES.get(component_type)
    if not component_class:
        print(f"Warning: Unknown component type: {component_type}")
        return None

    try:
        # Special handling for HTML component to pass variables
        if component_type == "html" and variables:
            # Make a deep copy of the config and add variables
            component_config = copy.deepcopy(config)
            component_config["variables"] = variables
            return component_class.from_config(component_config)
        else:
            return component_class.from_config(config)
    except Exception as e:
        print(f"Error creating component {component_type}: {e}")
        return None


# Export all component classes for easier importing
__all__ = [
    'Component',
    'TextComponent',
    'ImageComponent',
    'CircleComponent',
    'RectangleComponent',
    'CTAButtonComponent',
    'FooterComponent',
    'CTAButtonGroupComponent',
    'HTMLComponent',
    'create_component_from_config',
]
