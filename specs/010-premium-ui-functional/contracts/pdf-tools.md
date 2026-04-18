# Contract: PDF Tools

**Date**: 2026-03-30  
**Service**: PDF Manipulation Tools

## Overview

The PDF Tools service provides operations for merging, splitting, compressing, converting, and securing PDF documents.

## Interface

### Merge Tool

```python
class MergeTool:
    """Merge multiple PDF documents"""
    
    def merge(
        self,
        input_files: List[str],
        output_file: str,
        add_toc: bool = True,
        toc_title: str = "Table of Contents"
    ) -> MergeResult:
        """
        Merge multiple PDFs into one.
        
        Args:
            input_files: List of PDF file paths
            output_file: Output file path
            add_toc: Whether to add table of contents
            toc_title: Title for TOC page
            
        Returns: MergeResult with success status and metadata
        Raises: FileNotFoundError, MergeError
        """
        
    def merge_pages(
        self,
        input_files: List[Tuple[str, List[int]]],
        output_file: str
    ) -> MergeResult:
        """
        Merge specific pages from multiple PDFs.
        
        Args:
            input_files: List of (path, [page_numbers]) tuples
            output_file: Output file path
            
        Returns: MergeResult
        """
```

### Split Tool

```python
class SplitTool:
    """Split PDF documents"""
    
    def split_by_pages(
        self,
        input_file: str,
        output_dir: str,
        ranges: List[Tuple[int, int]] = None
    ) -> SplitResult:
        """
        Split PDF by page ranges.
        
        Args:
            input_file: Input PDF path
            output_dir: Output directory
            ranges: List of (start, end) page ranges, None for all pages
            
        Returns: SplitResult with output file paths
        """
        
    def split_by_size(
        self,
        input_file: str,
        output_dir: str,
        max_size_mb: float
    ) -> SplitResult:
        """
        Split PDF by maximum file size.
        
        Args:
            input_file: Input PDF path
            output_dir: Output directory
            max_size_mb: Maximum size per split file
            
        Returns: SplitResult
        """
        
    def split_by_bookmarks(
        self,
        input_file: str,
        output_dir: str
    ) -> SplitResult:
        """
        Split PDF at bookmark locations.
        
        Args:
            input_file: Input PDF path
            output_dir: Output directory
            
        Returns: SplitResult
        """
```

### Compress Tool

```python
class CompressTool:
    """Compress PDF documents"""
    
    def compress(
        self,
        input_file: str,
        output_file: str,
        quality: str = "medium"  # "low", "medium", "high"
    ) -> CompressResult:
        """
        Compress PDF file.
        
        Args:
            input_file: Input PDF path
            output_file: Output PDF path
            quality: Compression quality level
            
        Returns: CompressResult with size reduction stats
        """
        
    def get_compression_preview(
        self,
        input_file: str,
        quality: str
    ) -> CompressPreview:
        """
        Preview compression results before applying.
        
        Returns: CompressPreview with estimated size
        """
        
    QUALITY_LEVELS = {
        "low": {"dpi": 72, "image_quality": 50},
        "medium": {"dpi": 150, "image_quality": 75},
        "high": {"dpi": 300, "image_quality": 90}
    }
```

### Encryption Tool

```python
class EncryptionTool:
    """Encrypt and decrypt PDF documents"""
    
    def encrypt(
        self,
        input_file: str,
        output_file: str,
        user_password: str,
        owner_password: str = None,
        permissions: Dict[str, bool] = None
    ) -> EncryptResult:
        """
        Encrypt PDF with password.
        
        Args:
            input_file: Input PDF path
            output_file: Output PDF path
            user_password: Password to open document
            owner_password: Password for full access (defaults to user_password)
            permissions: Access permissions dict
            
        Returns: EncryptResult
        """
        
    def decrypt(
        self,
        input_file: str,
        output_file: str,
        password: str
    ) -> DecryptResult:
        """
        Decrypt PDF with password.
        
        Args:
            input_file: Encrypted PDF path
            output_file: Output PDF path
            password: Document password
            
        Returns: DecryptResult
        """
        
    DEFAULT_PERMISSIONS = {
        "print": True,
        "copy": True,
        "edit": False,
        "annotate": True,
        "form_fill": True
    }
```

### Signature Tool

```python
class SignatureTool:
    """Digital signature operations"""
    
    def add_signature(
        self,
        input_file: str,
        output_file: str,
        signature_data: bytes,
        page: int,
        x: float,
        y: float,
        width: float,
        height: float,
        reason: str = "",
        location: str = ""
    ) -> SignatureResult:
        """
        Add digital signature to PDF.
        
        Args:
            input_file: Input PDF path
            output_file: Output PDF path
            signature_data: Signature image bytes
            page: Page number
            x, y: Position coordinates
            width, height: Signature size
            reason: Signing reason
            location: Signing location
            
        Returns: SignatureResult
        """
        
    def verify_signature(
        self,
        input_file: str
    ) -> SignatureVerification:
        """
        Verify document signatures.
        
        Returns: SignatureVerification with status
        """
        
    def get_signatures(
        self,
        input_file: str
    ) -> List[SignatureInfo]:
        """
        Get all signatures in document.
        
        Returns: List of signature info
        """
```

### Redaction Tool

```python
class RedactionTool:
    """Permanently remove sensitive content"""
    
    def add_redaction(
        self,
        input_file: str,
        page: int,
        areas: List[Tuple[float, float, float, float]]
    ) -> RedactionResult:
        """
        Mark areas for redaction.
        
        Args:
            input_file: PDF path
            page: Page number
            areas: List of (x0, y0, x1, y1) rectangles
            
        Returns: RedactionResult
        """
        
    def apply_redactions(
        self,
        input_file: str,
        output_file: str
    ) -> ApplyResult:
        """
        Apply all pending redactions.
        
        Args:
            input_file: PDF with redaction marks
            output_file: Output PDF path
            
        Returns: ApplyResult
        """
        
    def find_text(
        self,
        input_file: str,
        search_text: str
    ) -> List[TextLocation]:
        """
        Find text locations for redaction.
        
        Returns: List of text locations with coordinates
        """
```

### Convert Tool

```python
class ConvertTool:
    """Convert between file formats"""
    
    def to_pdf(
        self,
        input_file: str,
        output_file: str,
        format_type: str = None  # Auto-detect if None
    ) -> ConvertResult:
        """
        Convert document to PDF.
        
        Supported formats: docx, xlsx, pptx, html, txt, images
        
        Returns: ConvertResult
        """
        
    def from_pdf(
        self,
        input_file: str,
        output_file: str,
        format_type: str  # "html", "text", "image"
    ) -> ConvertResult:
        """
        Convert PDF to other format.
        
        Returns: ConvertResult
        """
        
    def extract_images(
        self,
        input_file: str,
        output_dir: str,
        min_size: Tuple[int, int] = (50, 50)
    ) -> ExtractResult:
        """
        Extract all images from PDF.
        
        Args:
            input_file: PDF path
            output_dir: Output directory
            min_size: Minimum image size (width, height)
            
        Returns: ExtractResult with image paths
        """
```

## Result Types

```python
@dataclass
class MergeResult:
    success: bool
    output_file: str
    page_count: int
    file_size: int
    error: str = None

@dataclass
class SplitResult:
    success: bool
    output_files: List[str]
    error: str = None

@dataclass
class CompressResult:
    success: bool
    output_file: str
    original_size: int
    compressed_size: int
    reduction_percent: float
    error: str = None

@dataclass
class ConvertResult:
    success: bool
    output_file: str
    error: str = None
```

## Performance Requirements

| Operation | Max Time | Notes |
|-----------|----------|-------|
| Merge (10 files) | 30s | Depends on total size |
| Split | 10s | Per output file |
| Compress | 60s | Depends on page count |
| Encrypt | 5s | Per document |
| Convert (DOCX) | 30s | External tool dependent |

## Error Handling

| Error Type | Condition | Recovery |
|------------|-----------|----------|
| FileNotFoundError | Input doesn't exist | Show error message |
| PermissionError | Cannot write output | Prompt for location |
| PasswordError | Wrong password | Prompt retry |
| CorruptedPDFError | Invalid PDF structure | Show error, suggest re-download |
| SizeLimitError | Output too large | Suggest compression |
