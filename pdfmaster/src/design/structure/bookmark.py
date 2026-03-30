"""
Bookmark manager for PDF documents
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Union
from pathlib import Path
import fitz


@dataclass
class Bookmark:
    """PDF bookmark/outline entry"""

    title: str
    page_number: int  # 0-indexed
    level: int = 1
    children: List["Bookmark"] = field(default_factory=list)
    color: Optional[Tuple[int, int, int]] = None
    bold: bool = False
    italic: bool = False
    open: bool = True


class BookmarkManager:
    """Manage PDF bookmarks/outline"""

    def __init__(self):
        self.bookmarks: List[Bookmark] = []

    def load_from_document(self, doc: fitz.Document) -> "BookmarkManager":
        """Load bookmarks from existing PDF document"""
        toc = doc.get_toc()
        self.bookmarks = self._parse_toc(toc)
        return self

    def _parse_toc(self, toc: List) -> List[Bookmark]:
        """Parse PyMuPDF TOC into Bookmark objects"""
        bookmarks = []
        stack = [(bookmarks, 0)]  # (list, expected_level)

        for item in toc:
            level, title, page_num = item[0], item[1], item[2]

            bookmark = Bookmark(
                title=title,
                page_number=page_num - 1,  # Convert to 0-indexed
                level=level,
            )

            # Find correct parent level
            while stack and stack[-1][1] >= level:
                stack.pop()

            if stack:
                stack[-1][0].append(bookmark)
            else:
                bookmarks.append(bookmark)

            stack.append((bookmark.children, level))

        return bookmarks

    def add_bookmark(
        self, title: str, page_number: int, level: int = 1, parent: Optional[Bookmark] = None
    ) -> Bookmark:
        """Add a new bookmark"""
        bookmark = Bookmark(title=title, page_number=page_number, level=level)

        if parent:
            parent.children.append(bookmark)
        else:
            self.bookmarks.append(bookmark)

        return bookmark

    def add_chapter(self, title: str, page_number: int) -> Bookmark:
        """Add a chapter (level 1 bookmark)"""
        return self.add_bookmark(title, page_number, level=1)

    def add_section(self, title: str, page_number: int, chapter: Bookmark) -> Bookmark:
        """Add a section (level 2 bookmark) under a chapter"""
        return self.add_bookmark(title, page_number, level=2, parent=chapter)

    def add_subsection(self, title: str, page_number: int, section: Bookmark) -> Bookmark:
        """Add a subsection (level 3 bookmark) under a section"""
        return self.add_bookmark(title, page_number, level=3, parent=section)

    def remove_bookmark(self, bookmark: Bookmark) -> bool:
        """Remove a bookmark"""

        def _remove_from_list(bookmarks: List[Bookmark]) -> bool:
            if bookmark in bookmarks:
                bookmarks.remove(bookmark)
                return True
            for b in bookmarks:
                if _remove_from_list(b.children):
                    return True
            return False

        return _remove_from_list(self.bookmarks)

    def find_by_title(self, title: str) -> Optional[Bookmark]:
        """Find bookmark by title"""

        def _search(bookmarks: List[Bookmark]) -> Optional[Bookmark]:
            for b in bookmarks:
                if b.title == title:
                    return b
                found = _search(b.children)
                if found:
                    return found
            return None

        return _search(self.bookmarks)

    def get_flat_list(self) -> List[Tuple[int, str, int]]:
        """Get flat list of bookmarks as (level, title, page) tuples"""
        result = []

        def _flatten(bookmarks: List[Bookmark]):
            for b in bookmarks:
                result.append((b.level, b.title, b.page_number + 1))  # Convert to 1-indexed
                _flatten(b.children)

        _flatten(self.bookmarks)
        return result

    def save_to_document(self, doc: fitz.Document) -> None:
        """Save bookmarks to PDF document"""
        toc = self.get_flat_list()

        # Clear existing bookmarks
        doc.set_toc([])

        # Add new bookmarks
        if toc:
            doc.set_toc(toc)

    def save(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> Path:
        """Save bookmarks to a new PDF file"""
        input_path = Path(input_path)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(str(input_path))

        try:
            self.save_to_document(doc)
            doc.save(str(output_path))
            return output_path
        finally:
            doc.close()

    def import_from_headings(
        self, doc: fitz.Document, heading_patterns: Optional[List[str]] = None
    ) -> "BookmarkManager":
        """Import bookmarks from text headings in document"""
        # Default patterns for common heading formats
        patterns = heading_patterns or [
            r"^(Chapter|Section|Part)\s+\d+",
            r"^\d+\.\s+",
            r"^\d+\.\d+\s+",
            r"^[A-Z][A-Z\s]+$",  # ALL CAPS headings
        ]

        import re

        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if block["type"] == 0:  # Text block
                    for line in block["lines"]:
                        text = ""
                        for span in line["spans"]:
                            text += span["text"]

                        text = text.strip()

                        # Check if text matches heading pattern
                        for pattern in patterns:
                            if re.match(pattern, text):
                                # Determine level based on font size
                                font_size = line["spans"][0]["size"]
                                if font_size >= 18:
                                    level = 1
                                elif font_size >= 14:
                                    level = 2
                                else:
                                    level = 3

                                self.add_bookmark(text, page_num, level)
                                break

        return self

    def __len__(self) -> int:
        """Get total number of bookmarks"""

        def _count(bookmarks: List[Bookmark]) -> int:
            count = len(bookmarks)
            for b in bookmarks:
                count += _count(b.children)
            return count

        return _count(self.bookmarks)

    def __str__(self) -> str:
        """Get string representation"""
        lines = []

        def _format(bookmarks: List[Bookmark], indent: int = 0):
            for b in bookmarks:
                prefix = "  " * indent + ("• " if indent > 0 else "")
                lines.append(f"{prefix}{b.title} (Page {b.page_number + 1})")
                _format(b.children, indent + 1)

        _format(self.bookmarks)
        return "\n".join(lines) if lines else "No bookmarks"


def create_bookmarks(
    input_path: Union[str, Path], output_path: Union[str, Path], entries: List[Tuple[str, int]]
) -> Path:
    """Convenience function to create simple bookmarks"""
    manager = BookmarkManager()

    for title, page in entries:
        manager.add_chapter(title, page)

    return manager.save(input_path, output_path)


def import_bookmarks_from_toc(input_path: Union[str, Path], output_path: Union[str, Path]) -> Path:
    """Import bookmarks from existing document TOC and re-save"""
    doc = fitz.open(str(input_path))

    try:
        manager = BookmarkManager()
        manager.load_from_document(doc)

        # Re-save with same bookmarks (ensures they're properly formatted)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        manager.save(input_path, output_path)
        return output_path
    finally:
        doc.close()
