import logging
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class StyleConfig:
    font_name: str = "Helvetica"
    font_size: int = 12
    font_color: Tuple[int, int, int] = (0, 0, 0)
    background_color: Optional[Tuple[int, int, int]] = None
    alignment: str = "left"


@dataclass
class ElementStyle:
    margin_top: float = 0
    margin_bottom: float = 0
    margin_left: float = 0
    margin_right: float = 0
    padding: float = 0
    border_width: float = 0
    border_color: Tuple[int, int, int] = (0, 0, 0)


class StyleManager:
    DEFAULT_STYLES: Dict[str, StyleConfig] = {
        "heading1": StyleConfig(font_size=24, font_name="Helvetica-Bold"),
        "heading2": StyleConfig(font_size=18, font_name="Helvetica-Bold"),
        "heading3": StyleConfig(font_size=14, font_name="Helvetica-Bold"),
        "body": StyleConfig(font_size=12, font_name="Helvetica"),
        "caption": StyleConfig(font_size=10, font_name="Helvetica"),
        "code": StyleConfig(font_size=10, font_name="Courier"),
    }

    def __init__(self):
        self._custom_styles: Dict[str, StyleConfig] = {}

    def get_style(self, name: str) -> StyleConfig:
        if name in self._custom_styles:
            return self._custom_styles[name]
        return self.DEFAULT_STYLES.get(name, StyleConfig())

    def add_style(self, name: str, config: StyleConfig):
        self._custom_styles[name] = config
        logger.debug(f"Added custom style: {name}")

    def list_styles(self) -> List[str]:
        return list(self.DEFAULT_STYLES.keys()) + list(self._custom_styles.keys())


@dataclass
class Placeholder:
    name: str
    description: str = ""
    default_value: Optional[str] = None
    required: bool = True


class TemplateManager:
    def __init__(self):
        self._templates: Dict[str, Dict] = {}

    def register_template(
        self,
        name: str,
        layout: Dict,
        placeholders: Optional[List[Placeholder]] = None,
    ):
        self._templates[name] = {
            "layout": layout,
            "placeholders": placeholders or [],
        }
        logger.debug(f"Registered template: {name}")

    def get_template(self, name: str) -> Optional[Dict]:
        return self._templates.get(name)

    def list_templates(self) -> List[str]:
        return list(self._templates.keys())

    def create_default_templates(self):
        self.register_template(
            "simple",
            {
                "page_size": "A4",
                "margins": {"top": 72, "bottom": 72, "left": 72, "right": 72},
                "elements": [
                    {"type": "header", "height": 50},
                    {"type": "content", "flex": True},
                    {"type": "footer", "height": 30},
                ],
            },
            [
                Placeholder("title", "Document title", "Untitled"),
                Placeholder("author", "Document author", ""),
            ],
        )

        self.register_template(
            "letter",
            {
                "page_size": "Letter",
                "margins": {"top": 72, "bottom": 72, "left": 72, "right": 72},
                "elements": [
                    {"type": "sender", "height": 40},
                    {"type": "date", "height": 20},
                    {"type": "recipient", "height": 40},
                    {"type": "subject", "height": 20},
                    {"type": "body", "flex": True},
                    {"type": "signature", "height": 40},
                ],
            },
            [
                Placeholder("sender_address", "Sender address"),
                Placeholder("date", "Letter date"),
                Placeholder("recipient_name", "Recipient name"),
                Placeholder("subject", "Subject line"),
                Placeholder("body", "Letter content"),
                Placeholder("signature", "Signature", required=False),
            ],
        )

        self.register_template(
            "report",
            {
                "page_size": "A4",
                "margins": {"top": 72, "bottom": 72, "left": 72, "right": 72},
                "elements": [
                    {"type": "title_page", "height": "full"},
                ],
            },
            [
                Placeholder("report_title", "Report title"),
                Placeholder("subtitle", "Subtitle", required=False),
                Placeholder("author", "Author"),
                Placeholder("date", "Date"),
            ],
        )

        logger.info("Created default templates: simple, letter, report")
