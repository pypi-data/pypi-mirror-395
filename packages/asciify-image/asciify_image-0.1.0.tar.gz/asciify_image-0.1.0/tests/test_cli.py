"""Tests for CLI."""

import tempfile
from pathlib import Path

import pytest
from PIL import Image

from asciify.cli import create_parser, main


@pytest.fixture
def sample_image(tmp_path: Path) -> Path:
    """Create a simple test image."""
    img = Image.new("RGB", (50, 50), color=(128, 128, 128))
    path = tmp_path / "test.png"
    img.save(path)
    return path


class TestParser:
    """Test argument parser."""

    def test_parser_required_args(self) -> None:
        """Test parser requires image argument."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_parser_basic(self) -> None:
        """Test parser with just image path."""
        parser = create_parser()
        args = parser.parse_args(["test.png"])
        assert args.image == Path("test.png")

    def test_parser_all_options(self) -> None:
        """Test parser with all options."""
        parser = create_parser()
        args = parser.parse_args([
            "test.png",
            "-W", "80",
            "-H", "40",
            "-c", "complex",
            "--color",
            "--dither",
            "--invert",
            "-b", "1.5",
            "--contrast", "1.2",
            "-o", "output.txt",
        ])
        assert args.image == Path("test.png")
        assert args.width == 80
        assert args.height == 40
        assert args.charset == "complex"
        assert args.color is True
        assert args.dither is True
        assert args.invert is True
        assert args.brightness == 1.5
        assert args.contrast == 1.2
        assert args.output == Path("output.txt")

    def test_parser_charset_choices(self) -> None:
        """Test parser validates charset choices."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["test.png", "-c", "invalid"])


class TestMain:
    """Test main function."""

    def test_main_basic(self, sample_image: Path, capsys: pytest.CaptureFixture) -> None:
        """Test basic main execution."""
        result = main([str(sample_image), "-W", "20"])
        assert result == 0
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_main_with_output_file(self, sample_image: Path, tmp_path: Path) -> None:
        """Test main with output file."""
        output = tmp_path / "output.txt"
        result = main([str(sample_image), "-W", "20", "-o", str(output)])
        assert result == 0
        assert output.exists()
        content = output.read_text()
        assert len(content) > 0

    def test_main_nonexistent_file(self, capsys: pytest.CaptureFixture) -> None:
        """Test main with nonexistent file."""
        result = main(["/nonexistent/image.png"])
        assert result == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err

    def test_main_with_color(self, sample_image: Path, capsys: pytest.CaptureFixture) -> None:
        """Test main with color option."""
        result = main([str(sample_image), "-W", "20", "--color"])
        assert result == 0
        captured = capsys.readouterr()
        assert "\033[" in captured.out  # ANSI escape

    def test_main_all_charsets(self, sample_image: Path) -> None:
        """Test main with different charsets."""
        for charset in ["simple", "complex", "blocks", "symbols"]:
            result = main([str(sample_image), "-W", "20", "-c", charset])
            assert result == 0
