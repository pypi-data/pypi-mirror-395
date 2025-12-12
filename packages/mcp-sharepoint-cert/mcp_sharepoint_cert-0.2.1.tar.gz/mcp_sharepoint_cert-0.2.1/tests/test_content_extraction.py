"""Tests for content extraction utilities."""

import pytest

from mcp_sharepoint.resources import (
    extract_text_from_excel,
    extract_text_from_pdf,
    extract_text_from_word,
)


class TestPdfExtraction:
    """Tests for PDF text extraction."""

    def test_extract_from_valid_pdf(self):
        """Should extract text from valid PDF bytes."""
        # Create a minimal PDF with text
        # This is a real minimal PDF structure
        pdf_content = b"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length 44 >> stream
BT /F1 12 Tf 100 700 Td (Hello World) Tj ET
endstream endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000266 00000 n
0000000359 00000 n
trailer << /Size 6 /Root 1 0 R >>
startxref
434
%%EOF"""
        text, page_count = extract_text_from_pdf(pdf_content)
        assert page_count == 1
        assert isinstance(text, str)

    def test_extract_from_invalid_pdf_raises(self):
        """Should raise on invalid PDF."""
        with pytest.raises((RuntimeError, ValueError, Exception)):
            extract_text_from_pdf(b"not a pdf")


class TestExcelExtraction:
    """Tests for Excel text extraction."""

    def test_extract_from_invalid_excel_raises(self):
        """Should raise on invalid Excel file."""
        with pytest.raises((ValueError, Exception)):
            extract_text_from_excel(b"not an excel file")


class TestWordExtraction:
    """Tests for Word document text extraction."""

    def test_extract_from_invalid_word_raises(self):
        """Should raise on invalid Word file."""
        with pytest.raises((ValueError, Exception)):
            extract_text_from_word(b"not a word doc")
