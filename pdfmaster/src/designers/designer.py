import logging
from typing import Dict, List, Optional, Union
from pathlib import Path

from pdfmaster.src.core.creator import PDFCreator
from pdfmaster.src.designers.styles import StyleManager, TemplateManager

logger = logging.getLogger(__name__)


class PDFDesigner:
    def __init__(self):
        self.style_manager = StyleManager()
        self.template_manager = TemplateManager()
        self.template_manager.create_default_templates()

    def create_from_template(
        self,
        template_name: str,
        values: Dict[str, str],
        output_path: Union[str, Path],
    ) -> Path:
        template = self.template_manager.get_template(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")

        creator = PDFCreator()
        layout = template["layout"]
        page_size = layout.get("page_size", "A4")
        creator.page_size = page_size

        placeholders = template["placeholders"]
        for placeholder in placeholders:
            name = placeholder.name
            value = values.get(name, placeholder.default_value or "")
            if placeholder.required and not value:
                logger.warning(f"Required placeholder '{name}' is empty")

        creator.new_page()

        if template_name == "simple":
            y = 720
            if "title" in values:
                creator.add_text(
                    values["title"],
                    font_size=24,
                    font_name="Helvetica-Bold",
                    y=y,
                )
                y -= 40
            if "author" in values:
                creator.add_text(
                    f"By {values['author']}",
                    font_size=12,
                    font_name="Helvetica-Oblique",
                    y=y,
                )
                y -= 30
            if "content" in values:
                for line in values["content"].split("\n"):
                    creator.add_text(line, y=y, font_size=12)
                    y -= 15
                    if y < 50:
                        creator.new_page()
                        y = 720

        elif template_name == "letter":
            y = 720
            if "sender_address" in values:
                for line in values["sender_address"].split("\n"):
                    creator.add_text(line, y=y, font_size=10)
                    y -= 12
                y -= 20

            if "date" in values:
                creator.add_text(values["date"], y=y, font_size=10)
                y -= 30

            if "recipient_name" in values:
                creator.add_text(values["recipient_name"], y=y, font_size=12)
                y -= 15

            y -= 20

            if "subject" in values:
                creator.add_text(
                    f"Subject: {values['subject']}",
                    y=y,
                    font_size=12,
                    font_name="Helvetica-Bold",
                )
                y -= 30

            if "body" in values:
                for line in values["body"].split("\n"):
                    creator.add_text(line, y=y, font_size=12)
                    y -= 15
                    if y < 100:
                        creator.new_page()
                        y = 720

            y = 100
            if "signature" in values:
                creator.add_text(values["signature"], y=y, font_size=12)

        elif template_name == "report":
            creator.new_page()
            y = 500

            if "report_title" in values:
                creator.add_text(
                    values["report_title"],
                    font_size=28,
                    font_name="Helvetica-Bold",
                    y=y,
                )
                y -= 40

            if "subtitle" in values and values["subtitle"]:
                creator.add_text(
                    values["subtitle"],
                    font_size=16,
                    y=y,
                )
                y -= 30

            if "author" in values:
                creator.add_text(
                    f"By {values['author']}",
                    font_size=14,
                    y=y,
                )
                y -= 25

            if "date" in values:
                creator.add_text(
                    values["date"],
                    font_size=12,
                    y=y,
                )

        output_path = creator.save(output_path)
        logger.info(f"Created PDF from template '{template_name}': {output_path}")
        return output_path

    def apply_style_to_text(
        self,
        creator: PDFCreator,
        text: str,
        style_name: str,
        x: float = 72,
        y: float = 720,
    ):
        style = self.style_manager.get_style(style_name)
        creator.add_text(
            text,
            x=x,
            y=y,
            font_size=style.font_size,
            font_name=style.font_name,
            font_color=style.font_color,
        )

    def list_available_templates(self) -> List[str]:
        return self.template_manager.list_templates()

    def list_available_styles(self) -> List[str]:
        return self.style_manager.list_styles()
