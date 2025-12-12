import os
import tempfile
import logging
import io
import re
import asyncio
from typing import Tuple, Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont

from .base import Component

logger = logging.getLogger(__name__)


class HTMLComponent(Component):
    """Component for rendering HTML/CSS content onto an image."""

    def __init__(
        self,
        html_content: str,
        css_content: Optional[str] = None,
        position: Tuple[int, int] = (0, 0),
        size: Tuple[int, int] = (800, 600),
        background_transparent: bool = False,
        rendering_engine: str = "auto",
        variables: Optional[Dict[str, Any]] = None,
        add_default_styles: bool = False,
    ):
        super().__init__(position)
        self.html_content = html_content
        self.css_content = css_content or ""
        self.size = size
        self.background_transparent = background_transparent
        self.variables = variables or {}
        self.add_default_styles = add_default_styles
        self.rendering_engine = (
            "auto"
            if rendering_engine not in ["playwright", "pil", "auto"]
            else rendering_engine
        )

    async def render(self, image: Image.Image) -> Image.Image:
        if not self.html_content:
            return image
        html_image = await self._render_html_to_image()
        if html_image:
            image.paste(
                html_image,
                self.position,
                html_image if html_image.mode == "RGBA" else None,
            )
        return image

    async def _render_html_to_image(self) -> Optional[Image.Image]:
        # Choose engine based on configuration and availability
        if self.rendering_engine == "pil" or (
            self.rendering_engine == "auto" and not self._playwright_available()
        ):
            return self._render_with_pil_fallback()

        if self.rendering_engine in ("playwright", "auto") and self._playwright_available():
            try:
                return await self._render_with_playwright()
            except Exception as e:
                logger.error(f"Playwright rendering failed: {e}")
                logger.warning("Falling back to PIL renderer.")
                raise "playwright rendering failed"

        logger.warning("Playwright unavailable. Falling back to PIL renderer.")
        return self._render_with_pil_fallback()

    def _playwright_available(self) -> bool:
        try:
            import playwright  # noqa: F401
            return True
        except ImportError:
            return False

    async def _render_with_playwright(self) -> Optional[Image.Image]:
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)

                page = await browser.new_page(
                    viewport={"width": self.size[0], "height": self.size[1]},
                    device_scale_factor=2,
                )

                html_content = self._create_full_html()
                await page.set_content(html_content, wait_until="domcontentloaded", timeout=10000)

                if self.add_default_styles:
                    await page.evaluate(
                        "document.body.style.margin = '0'; document.body.style.padding = '0';"
                    )
                # Wait for the page to load
                await asyncio.sleep(0.5)
                screenshot_bytes = await page.screenshot(
                    type="png",
                    timeout=10000,
                    full_page=True,
                )

                await browser.close()

                image = Image.open(io.BytesIO(screenshot_bytes))
                if image.size != self.size:
                    image = image.resize(self.size, Image.Resampling.LANCZOS)

                return image

        except ImportError:
            logger.error(
                "Playwright not installed. Run: pip install playwright && playwright install chromium"
            )
            return None
        except Exception as e:
            logger.error(f"Playwright rendering failed: {e}")
            return None

    def _render_with_pil_fallback(self) -> Image.Image:
        try:
            img = Image.new(
                "RGBA",
                self.size,
                (0, 0, 0, 0) if self.background_transparent else (255, 255, 255, 255),
            )
            draw = ImageDraw.Draw(img)
            text_content = self._extract_text_from_html(
                self._substitute_variables(self.html_content)
            )
            font = ImageFont.load_default()
            margin, line_height = 20, 20
            x, y = margin, margin
            max_width = self.size[0] - 2 * margin

            if "title" in self.variables:
                draw.text(
                    (x, y), str(self.variables["title"]), fill=(0, 0, 0), font=font
                )
                y += 34
            if "subtitle" in self.variables:
                draw.text(
                    (x, y), str(self.variables["subtitle"]), fill=(0, 0, 0), font=font
                )
                y += 28

            lines, line = [], ""
            for word in text_content.split():
                test_line = f"{line}{word} "
                if draw.textlength(test_line, font=font) <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = f"{word} "
            if line:
                lines.append(line)

            for line in lines:
                draw.text((x, y), line, fill=(0, 0, 0), font=font)
                y += line_height
            return img
        except Exception as e:
            logger.error(f"PIL rendering failed: {e}")
            return Image.new("RGBA", self.size, (255, 255, 255, 255))

    def _extract_text_from_html(self, html_content: str) -> str:
        text = re.sub(r"<[^>]*>", " ", html_content)
        text = (
            text.replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
        )
        text = text.replace("&quot;", '"').replace("&#39;", "'")
        return re.sub(r"\s+", " ", text).strip()

    def _create_full_html(self) -> str:
        processed_html = self._substitute_variables(self.html_content)
        style_content = self._substitute_variables(self.css_content)

        default_body_styles = ""
        if self.add_default_styles:
            background = "transparent" if self.background_transparent else "#000"
            default_body_styles = (
                f"margin: 0; padding: 0; width: {self.size[0]}px; height: {self.size[1]}px; "
                f"background: {background}; overflow: hidden;"
            )

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width={self.size[0]}, height={self.size[1]}, initial-scale=1.0">
            <style>
                body {{ {default_body_styles} }}
                {style_content}
            </style>
        </head>
        <body>
            {processed_html}
        </body>
        </html>
        """

    def _substitute_variables(self, content: str) -> str:
        if not content or not self.variables:
            return content
        return re.sub(
            r"\${([^}]+)}",
            lambda m: str(self.variables.get(m.group(1), m.group(0))),
            content,
        )

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "HTMLComponent":
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )
        size = (
            config.get("size", {}).get("width", 800),
            config.get("size", {}).get("height", 600),
        )
        return cls(
            html_content=config.get("html_content", ""),
            css_content=config.get("css_content"),
            position=position,
            size=size,
            background_transparent=config.get("background_transparent", False),
            rendering_engine=config.get("rendering_engine", "auto"),
            variables=config.get("variables", {}),
            add_default_styles=config.get("add_default_styles", False),
        )
