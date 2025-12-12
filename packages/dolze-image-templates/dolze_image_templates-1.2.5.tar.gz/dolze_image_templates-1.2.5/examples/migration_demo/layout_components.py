"""
NEW LAYOUT COMPONENTS FOR MIGRATION
====================================

These components demonstrate the migration strategy from HTML templates
to reusable, flexible component-based architecture.

Usage:
    from dolze_image_templates.components.layout import ContentBlockComponent, LogoFooterComponent
"""

from typing import Tuple, Optional, Dict, Any, List
from PIL import Image
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dolze_image_templates.components.base import Component
from dolze_image_templates.components.text import TextComponent
from dolze_image_templates.components.image import ImageComponent


class ContentBlockComponent(Component):
    """
    Flexible content block with preheading, title, and subtitle.
    
    This component replaces the hardcoded HTML/CSS pattern found in
    holiday/event templates like world_aids_day, world_cancer_day, etc.
    
    Features:
    - Automatic vertical spacing
    - Flexible alignment (left, center, right)
    - Optional preheading badge
    - Customizable fonts and colors
    - Runtime positioning
    
    Example:
        component = ContentBlockComponent(
            position=(60, 120),
            preheading="📅 Dec 1 — World AIDS Day",
            title="Support. Awareness. Hope.",
            subtitle="Standing together in the fight against HIV/AIDS.",
            alignment="center"
        )
    """
    
    def __init__(
        self,
        position: Tuple[int, int],
        preheading: Optional[str] = None,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        alignment: str = "center",
        text_color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        max_width: int = 960,
        title_font_size: int = 64,
        subtitle_font_size: int = 36,
        preheading_font_size: int = 18,
        title_font: str = "Outfit-Bold",
        subtitle_font: str = "Outfit-Regular",
        preheading_font: str = "Outfit-Medium",
        spacing: int = 20,
    ):
        super().__init__(position)
        self.preheading = preheading
        self.title = title
        self.subtitle = subtitle
        self.alignment = alignment
        self.text_color = text_color
        self.max_width = max_width
        self.title_font_size = title_font_size
        self.subtitle_font_size = subtitle_font_size
        self.preheading_font_size = preheading_font_size
        self.title_font = title_font
        self.subtitle_font = subtitle_font
        self.preheading_font = preheading_font
        self.spacing = spacing
        
        self._components: List[Component] = []
        self._build_components()
    
    def _build_components(self):
        """Build internal text components with proper spacing"""
        x, y = self.position
        current_y = y
        
        # Preheading (badge/pill style)
        if self.preheading:
            self._components.append(
                TextComponent(
                    text=self.preheading,
                    position=(x, current_y),
                    font_size=self.preheading_font_size,
                    color=self.text_color,
                    font_path=self.preheading_font,
                    alignment=self.alignment,
                    max_width=self.max_width
                )
            )
            current_y += self.preheading_font_size + self.spacing + 10
        
        # Title (main heading)
        if self.title:
            self._components.append(
                TextComponent(
                    text=self.title,
                    position=(x, current_y),
                    font_size=self.title_font_size,
                    color=self.text_color,
                    font_path=self.title_font,
                    alignment=self.alignment,
                    max_width=self.max_width
                )
            )
            # Estimate height based on font size and potential wrapping
            estimated_lines = max(1, len(self.title) // 30)
            current_y += (self.title_font_size * estimated_lines) + self.spacing
        
        # Subtitle (secondary text)
        if self.subtitle:
            self._components.append(
                TextComponent(
                    text=self.subtitle,
                    position=(x, current_y),
                    font_size=self.subtitle_font_size,
                    color=self.text_color,
                    font_path=self.subtitle_font,
                    alignment=self.alignment,
                    max_width=self.max_width
                )
            )
    
    async def render(self, image: Image.Image) -> Image.Image:
        """Render all sub-components"""
        for component in self._components:
            image = await component.render(image)
        return image
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "ContentBlockComponent":
        """Create component from JSON configuration"""
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0)
        )
        return cls(
            position=position,
            preheading=config.get("preheading"),
            title=config.get("title"),
            subtitle=config.get("subtitle"),
            alignment=config.get("alignment", "center"),
            text_color=tuple(config.get("text_color", [255, 255, 255, 255])),
            max_width=config.get("max_width", 960),
            title_font_size=config.get("title_font_size", 64),
            subtitle_font_size=config.get("subtitle_font_size", 36),
            preheading_font_size=config.get("preheading_font_size", 18),
            title_font=config.get("title_font", "Outfit-Bold"),
            subtitle_font=config.get("subtitle_font", "Outfit-Regular"),
            preheading_font=config.get("preheading_font", "Outfit-Medium"),
            spacing=config.get("spacing", 20)
        )


class LogoFooterComponent(Component):
    """
    Footer with logo and text, commonly used in social media posts.
    
    This component replaces the hardcoded footer HTML/CSS pattern found
    in many templates.
    
    Features:
    - Vertical or horizontal layout
    - Flexible positioning
    - Automatic spacing
    - Customizable logo size
    - Runtime configuration
    
    Example:
        component = LogoFooterComponent(
            position=(390, 1150),
            logo_url="https://example.com/logo.png",
            text="@dolze.ai",
            layout="vertical",
            alignment="center"
        )
    """
    
    def __init__(
        self,
        position: Tuple[int, int],
        logo_url: str,
        text: str,
        logo_size: int = 80,
        text_font_size: int = 22,
        text_color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        text_font: str = "Outfit-Medium",
        layout: str = "vertical",  # "vertical", "horizontal"
        alignment: str = "center",
        spacing: int = 10
    ):
        super().__init__(position)
        self.logo_url = logo_url
        self.text = text
        self.logo_size = logo_size
        self.text_font_size = text_font_size
        self.text_color = text_color
        self.text_font = text_font
        self.layout = layout
        self.alignment = alignment
        self.spacing = spacing
        
        self._components: List[Component] = []
        self._build_components()
    
    def _build_components(self):
        """Build logo and text components based on layout"""
        x, y = self.position
        
        if self.layout == "vertical":
            # Logo on top, text below (centered)
            logo_x = x
            logo_y = y
            text_y = y + self.logo_size + self.spacing
            
            self._components.append(
                ImageComponent(
                    image_url=self.logo_url,
                    position=(logo_x, logo_y),
                    size=(self.logo_size * 3, self.logo_size),  # Allow wider logos
                    aspect_ratio="contain"
                )
            )
            
            self._components.append(
                TextComponent(
                    text=self.text,
                    position=(x - 100, text_y),  # Offset for centering
                    font_size=self.text_font_size,
                    color=self.text_color,
                    font_path=self.text_font,
                    alignment=self.alignment,
                    max_width=400
                )
            )
        else:
            # Horizontal layout (logo left, text right)
            logo_width = self.logo_size * 2
            
            self._components.append(
                ImageComponent(
                    image_url=self.logo_url,
                    position=(x, y),
                    size=(logo_width, self.logo_size),
                    aspect_ratio="contain"
                )
            )
            
            self._components.append(
                TextComponent(
                    text=self.text,
                    position=(x + logo_width + self.spacing, y + self.logo_size // 3),
                    font_size=self.text_font_size,
                    color=self.text_color,
                    font_path=self.text_font,
                    alignment="left",
                    max_width=400
                )
            )
    
    async def render(self, image: Image.Image) -> Image.Image:
        """Render logo and text"""
        for component in self._components:
            image = await component.render(image)
        return image
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "LogoFooterComponent":
        """Create component from JSON configuration"""
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0)
        )
        return cls(
            position=position,
            logo_url=config.get("logo_url", ""),
            text=config.get("text", ""),
            logo_size=config.get("logo_size", 80),
            text_font_size=config.get("text_font_size", 22),
            text_color=tuple(config.get("text_color", [255, 255, 255, 255])),
            text_font=config.get("text_font", "Outfit-Medium"),
            layout=config.get("layout", "vertical"),
            alignment=config.get("alignment", "center"),
            spacing=config.get("spacing", 10)
        )


# Example usage
if __name__ == "__main__":
    print("Layout Components for Migration")
    print("=" * 50)
    print("\n1. ContentBlockComponent")
    print("   - Replaces hardcoded HTML content blocks")
    print("   - Used in 8+ holiday/event templates")
    print("   - Saves ~1,500 chars per template")
    print("\n2. LogoFooterComponent")
    print("   - Replaces hardcoded footer HTML")
    print("   - Used in 40+ templates")
    print("   - Saves ~500 chars per template")
    print("\nTotal estimated savings: ~50KB across all templates")
