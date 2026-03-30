"""
PDF Merge and Split Operations

This module provides functionality for merging multiple PDF files
and splitting PDFs by page ranges or into individual pages.
"""

import logging
import re
from pathlib import Path
from typing import List, Optional, Tuple, Union, Callable

import fitz

logger = logging.getLogger(__name__)


class PageRangeError(ValueError):
    """Raised when page range is invalid"""

    pass


class PDFMerger:
    """Merge multiple PDF files into a single PDF"""

    def __init__(self):
        self._documents: List[Tuple[str, fitz.Document]] = []

    def add_pdf(self, file_path: Union[str, Path], password: Optional[str] = None) -> "PDFMerger":
        """Add a PDF to the merge list"""
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        try:
            doc = fitz.open(str(file_path))

            if doc.is_encrypted:
                if password:
                    if not doc.authenticate(password):
                        doc.close()
                        raise ValueError(f"Invalid password for: {file_path.name}")
                else:
                    doc.close()
                    raise ValueError(f"PDF is password protected: {file_path.name}")

            self._documents.append((str(file_path), doc))
            logger.info(f"Added PDF to merge list: {file_path.name} ({len(doc)} pages)")
            return self

        except fitz.FitzError as e:
            raise ValueError(f"Cannot open PDF {file_path.name}: {str(e)}")

    def add_pdfs(
        self, file_paths: List[Union[str, Path]], password: Optional[str] = None
    ) -> "PDFMerger":
        """Add multiple PDFs to the merge list"""
        for path in file_paths:
            self.add_pdf(path, password)
        return self

    def get_total_pages(self) -> int:
        """Get total number of pages across all added PDFs"""
        return sum(len(doc) for _, doc in self._documents)

    def get_file_info(self) -> List[dict]:
        """Get information about added PDFs"""
        info = []
        for path, doc in self._documents:
            info.append(
                {"path": path, "name": Path(path).name, "pages": len(doc), "metadata": doc.metadata}
            )
        return info

    def merge(
        self,
        output_path: Union[str, Path],
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> Path:
        """
        Merge all added PDFs into a single file

        Args:
            output_path: Path for the output PDF
            progress_callback: Optional callback(current_page, message)

        Returns:
            Path to the merged PDF
        """
        if not self._documents:
            raise ValueError("No PDF files added to merge")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        total_pages = self.get_total_pages()
        processed = 0

        try:
            # Create output document
            merged = fitz.open()

            for file_idx, (file_path, doc) in enumerate(self._documents):
                if progress_callback:
                    progress_callback(
                        int((processed / total_pages) * 100), f"Adding {Path(file_path).name}..."
                    )

                # Insert all pages from this document
                merged.insert_pdf(doc)
                processed += len(doc)

                logger.info(f"Added {len(doc)} pages from {Path(file_path).name}")

            # Save the merged document
            merged.save(str(output_path))
            merged.close()

            if progress_callback:
                progress_callback(100, "Merge complete")

            logger.info(f"Merged {len(self._documents)} PDFs into {output_path.name}")
            return output_path

        except Exception as e:
            logger.error(f"Merge failed: {str(e)}")
            raise
        finally:
            self.close()

    def close(self):
        """Close all opened documents"""
        for _, doc in self._documents:
            try:
                doc.close()
            except:
                pass
        self._documents.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class PDFSplitter:
    """Split a PDF into multiple files by page ranges or individual pages"""

    def __init__(self, input_path: Union[str, Path]):
        self.input_path = Path(input_path)
        self._document: Optional[fitz.Document] = None

    def open(self) -> "PDFSplitter":
        """Open the PDF file"""
        if not self.input_path.exists():
            raise FileNotFoundError(f"PDF file not found: {self.input_path}")

        self._document = fitz.open(str(self.input_path))

        if self._document.is_encrypted:
            raise ValueError(f"PDF is password protected: {self.input_path.name}")

        logger.info(
            f"Opened PDF for splitting: {self.input_path.name} ({len(self._document)} pages)"
        )
        return self

    @property
    def page_count(self) -> int:
        """Get the number of pages in the PDF"""
        if self._document is None:
            return 0
        return len(self._document)

    @staticmethod
    def parse_page_range(range_str: str, max_pages: int) -> List[int]:
        """
        Parse page range string into list of page numbers (0-indexed)

        Supported formats:
        - "1-3" -> [0, 1, 2]
        - "5-" -> [4, 5, ..., max-1]
        - "-3" -> [0, 1, 2]
        - "1,3,5" -> [0, 2, 4]
        - "1-3,5,7-" -> [0, 1, 2, 4, 6, 7, ...]

        Returns:
            List of 0-indexed page numbers
        """
        pages = set()

        # Split by comma for multiple ranges
        parts = [p.strip() for p in range_str.split(",")]

        for part in parts:
            if not part:
                continue

            # Check for range pattern
            if "-" in part:
                start_str, end_str = part.split("-", 1)

                # Parse start
                if start_str == "":
                    start = 0
                else:
                    start = int(start_str) - 1  # Convert to 0-indexed

                # Parse end
                if end_str == "":
                    end = max_pages - 1
                else:
                    end = int(end_str) - 1  # Convert to 0-indexed

                # Validate
                if start < 0:
                    raise PageRangeError(f"Page numbers must be >= 1: {part}")
                if end >= max_pages:
                    raise PageRangeError(
                        f"Page number {end + 1} exceeds document length ({max_pages})"
                    )
                if start > end:
                    raise PageRangeError(f"Invalid range: {part}")

                pages.update(range(start, end + 1))
            else:
                # Single page number
                page = int(part) - 1  # Convert to 0-indexed
                if page < 0:
                    raise PageRangeError(f"Page numbers must be >= 1: {part}")
                if page >= max_pages:
                    raise PageRangeError(
                        f"Page number {page + 1} exceeds document length ({max_pages})"
                    )
                pages.add(page)

        return sorted(pages)

    def split_by_range(
        self,
        page_range: str,
        output_path: Union[str, Path],
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> Path:
        """
        Split PDF by page range

        Args:
            page_range: Page range string (e.g., "1-3", "5-", "1,3,5")
            output_path: Path for the output PDF
            progress_callback: Optional callback(percentage, message)

        Returns:
            Path to the output PDF
        """
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")

        pages = self.parse_page_range(page_range, self.page_count)

        if not pages:
            raise ValueError("No pages selected")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            output = fitz.open()

            for idx, page_num in enumerate(pages):
                if progress_callback:
                    progress = int(((idx + 1) / len(pages)) * 100)
                    progress_callback(progress, f"Adding page {page_num + 1}...")

                output.insert_pdf(self._document, from_page=page_num, to_page=page_num)

            output.save(str(output_path))
            output.close()

            if progress_callback:
                progress_callback(100, "Split complete")

            logger.info(f"Split {len(pages)} pages to {output_path.name}")
            return output_path

        except Exception as e:
            logger.error(f"Split failed: {str(e)}")
            raise

    def split_into_individual(
        self,
        output_dir: Union[str, Path],
        base_name: Optional[str] = None,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> List[Path]:
        """
        Split PDF into individual single-page PDFs

        Args:
            output_dir: Directory to save individual pages
            base_name: Base name for output files (default: original filename)
            progress_callback: Optional callback(percentage, message)

        Returns:
            List of paths to created files
        """
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        if base_name is None:
            base_name = self.input_path.stem

        created_files = []
        total_pages = self.page_count

        try:
            for page_num in range(total_pages):
                if progress_callback:
                    progress = int(((page_num + 1) / total_pages) * 100)
                    progress_callback(progress, f"Creating page {page_num + 1} of {total_pages}...")

                output = fitz.open()
                output.insert_pdf(self._document, from_page=page_num, to_page=page_num)

                output_path = output_dir / f"{base_name}_page_{page_num + 1}.pdf"
                output.save(str(output_path))
                output.close()

                created_files.append(output_path)

            if progress_callback:
                progress_callback(100, f"Created {len(created_files)} files")

            logger.info(f"Split into {len(created_files)} individual pages")
            return created_files

        except Exception as e:
            logger.error(f"Individual split failed: {str(e)}")
            raise

    def split_every_n_pages(
        self,
        n: int,
        output_dir: Union[str, Path],
        base_name: Optional[str] = None,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> List[Path]:
        """
        Split PDF into chunks of N pages each

        Args:
            n: Number of pages per chunk
            output_dir: Directory to save chunks
            base_name: Base name for output files
            progress_callback: Optional callback(percentage, message)

        Returns:
            List of paths to created files
        """
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")

        if n < 1:
            raise ValueError("N must be at least 1")

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        if base_name is None:
            base_name = self.input_path.stem

        total_pages = self.page_count
        created_files = []
        chunk_num = 1

        try:
            for start_page in range(0, total_pages, n):
                end_page = min(start_page + n - 1, total_pages - 1)

                if progress_callback:
                    progress = int(((start_page + 1) / total_pages) * 100)
                    progress_callback(progress, f"Creating chunk {chunk_num}...")

                output = fitz.open()
                output.insert_pdf(self._document, from_page=start_page, to_page=end_page)

                output_path = output_dir / f"{base_name}_part_{chunk_num}.pdf"
                output.save(str(output_path))
                output.close()

                created_files.append(output_path)
                chunk_num += 1

            if progress_callback:
                progress_callback(100, f"Created {len(created_files)} chunks")

            logger.info(f"Split into {len(created_files)} chunks of up to {n} pages")
            return created_files

        except Exception as e:
            logger.error(f"Chunk split failed: {str(e)}")
            raise

    def close(self):
        """Close the PDF document"""
        if self._document is not None:
            self._document.close()
            self._document = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def merge_pdfs(
    input_paths: List[Union[str, Path]],
    output_path: Union[str, Path],
    password: Optional[str] = None,
    progress_callback: Optional[Callable[[int, str], None]] = None,
) -> Path:
    """
    Convenience function to merge multiple PDFs

    Args:
        input_paths: List of PDF file paths
        output_path: Path for the output PDF
        password: Optional password for protected PDFs
        progress_callback: Optional callback(percentage, message)

    Returns:
        Path to the merged PDF
    """
    with PDFMerger() as merger:
        merger.add_pdfs(input_paths, password)
        return merger.merge(output_path, progress_callback)


def split_pdf(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    page_range: Optional[str] = None,
    individual: bool = False,
    chunk_size: Optional[int] = None,
    progress_callback: Optional[Callable[[int, str], None]] = None,
) -> Union[Path, List[Path]]:
    """
    Convenience function to split a PDF

    Args:
        input_path: Input PDF path
        output_path: Output path (file or directory)
        page_range: Page range string for range split
        individual: If True, split into individual pages
        chunk_size: If set, split into chunks of this size
        progress_callback: Optional callback(percentage, message)

    Returns:
        Path(s) to output files
    """
    with PDFSplitter(input_path) as splitter:
        if individual:
            return splitter.split_into_individual(output_path, progress_callback=progress_callback)
        elif chunk_size:
            return splitter.split_every_n_pages(
                chunk_size, output_path, progress_callback=progress_callback
            )
        elif page_range:
            return splitter.split_by_range(page_range, output_path, progress_callback)
        else:
            raise ValueError("Must specify page_range, individual=True, or chunk_size")
