"""Tests for file format detection (.txt.acmi, .zip.acmi)."""

import tempfile
import zipfile
from pathlib import Path
import pytest

from tacview_duckdb.parser.utils import open_acmi_file


def test_open_txt_acmi():
    """Test opening uncompressed .txt.acmi files."""
    content = """FileType=text/acmi/tacview
FileVersion=2.2
0,Title=Test Recording
#0
1,Name=Test,Type=Air+FixedWing
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt.acmi", delete=False) as f:
        f.write(content)
        temp_path = f.name

    try:
        # Open file
        with open_acmi_file(temp_path) as stream:
            lines = stream.readlines()

        # Verify content
        assert lines[0].strip() == "FileType=text/acmi/tacview"
        assert lines[1].strip() == "FileVersion=2.2"
    finally:
        Path(temp_path).unlink()


def test_open_zip_acmi():
    """Test opening compressed .zip.acmi files."""
    content = """FileType=text/acmi/tacview
FileVersion=2.2
0,Title=Test Recording
#0
1,Name=Test,Type=Air+FixedWing
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create temporary .txt.acmi file
        txt_path = Path(tmpdir) / "recording.txt.acmi"
        txt_path.write_text(content, encoding="utf-8")

        # Create ZIP archive
        zip_path = Path(tmpdir) / "recording.zip.acmi"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(txt_path, arcname="recording.txt.acmi")

        # Open ZIP file
        with open_acmi_file(zip_path) as stream:
            lines = stream.readlines()

        # Verify content
        assert lines[0].strip() == "FileType=text/acmi/tacview"
        assert lines[1].strip() == "FileVersion=2.2"


def test_open_acmi_auto_detect():
    """Test auto-detection of .acmi files."""
    content = """FileType=text/acmi/tacview
FileVersion=2.2
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test plain text .acmi
        plain_path = Path(tmpdir) / "recording.acmi"
        plain_path.write_text(content, encoding="utf-8")

        with open_acmi_file(plain_path) as stream:
            lines = stream.readlines()
        assert lines[0].strip() == "FileType=text/acmi/tacview"

        # Test compressed .acmi
        txt_path = Path(tmpdir) / "compressed.txt.acmi"
        txt_path.write_text(content, encoding="utf-8")

        zip_path = Path(tmpdir) / "compressed.acmi"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(txt_path, arcname="compressed.txt.acmi")

        with open_acmi_file(zip_path) as stream:
            lines = stream.readlines()
        assert lines[0].strip() == "FileType=text/acmi/tacview"


def test_open_zip_acmi_no_txt_acmi():
    """Test error when ZIP doesn't contain .txt.acmi file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = Path(tmpdir) / "invalid.zip.acmi"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("other_file.txt", "content")

        with pytest.raises(ValueError, match="No .txt.acmi or .acmi file found"):
            open_acmi_file(zip_path)


def test_utf8_bom_handling():
    """Test UTF-8 BOM handling."""
    # UTF-8 BOM + content
    content_with_bom = "\ufeffFileType=text/acmi/tacview\nFileVersion=2.2"

    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8-sig", suffix=".txt.acmi", delete=False
    ) as f:
        f.write(content_with_bom)
        temp_path = f.name

    try:
        with open_acmi_file(temp_path) as stream:
            first_line = stream.readline()

        # BOM should be stripped
        assert first_line.strip() == "FileType=text/acmi/tacview"
        assert "\ufeff" not in first_line
    finally:
        Path(temp_path).unlink()

