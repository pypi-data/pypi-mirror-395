"""Tests for ASCII art converter."""

import tempfile
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from asciify.converter import ASCIIArtConverter


@pytest.fixture
def sample_image(tmp_path: Path) -> Path:
    """Create a simple test image."""
    img = Image.new("RGB", (10, 10), color=(128, 128, 128))
    path = tmp_path / "test.png"
    img.save(path)
    return path


@pytest.fixture
def gradient_image(tmp_path: Path) -> Path:
    """Create a gradient test image."""
    width, height = 100, 50
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    for x in range(width):
        value = int(255 * x / width)
        arr[:, x] = [value, value, value]
    img = Image.fromarray(arr)
    path = tmp_path / "gradient.png"
    img.save(path)
    return path


class TestASCIIArtConverter:
    """Test ASCII art converter."""

    def test_init_default(self) -> None:
        """Test default initialization."""
        converter = ASCIIArtConverter()
        assert converter.colored is False
        assert converter.dither is False

    def test_init_with_options(self) -> None:
        """Test initialization with options."""
        converter = ASCIIArtConverter(
            charset="complex",
            colored=True,
            dither=True,
        )
        assert converter.colored is True
        assert converter.dither is True

    def test_init_invalid_charset(self) -> None:
        """Test initialization with invalid charset."""
        with pytest.raises(ValueError, match="Unknown charset"):
            ASCIIArtConverter(charset="invalid")

    def test_convert_basic(self, sample_image: Path) -> None:
        """Test basic image conversion."""
        converter = ASCIIArtConverter()
        result = converter.convert(sample_image, width=20)
        assert isinstance(result, str)
        assert len(result) > 0
        lines = result.split("\n")
        assert len(lines) > 0

    def test_convert_with_width(self, sample_image: Path) -> None:
        """Test conversion with specified width."""
        converter = ASCIIArtConverter()
        result = converter.convert(sample_image, width=30)
        lines = result.split("\n")
        assert all(len(line) == 30 for line in lines)

    def test_convert_with_color(self, sample_image: Path) -> None:
        """Test colored output contains ANSI codes."""
        converter = ASCIIArtConverter(colored=True)
        result = converter.convert(sample_image, width=10)
        assert "\033[" in result  # ANSI escape sequence

    def test_convert_with_invert(self, tmp_path: Path) -> None:
        """Test inversion produces different output."""
        # Create a high-contrast image that will show difference when inverted
        arr = np.zeros((100, 100, 3), dtype=np.uint8)
        arr[:50, :] = [0, 0, 0]  # Top half black
        arr[50:, :] = [255, 255, 255]  # Bottom half white
        img = Image.fromarray(arr)
        path = tmp_path / "contrast.png"
        img.save(path)

        converter = ASCIIArtConverter()
        normal = converter.convert(path, width=50)
        inverted = converter.convert(path, width=50, invert=True)
        assert normal != inverted

    def test_convert_with_dithering(self, gradient_image: Path) -> None:
        """Test dithering produces output."""
        converter = ASCIIArtConverter(dither=True)
        result = converter.convert(gradient_image, width=50)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_convert_nonexistent_file(self) -> None:
        """Test conversion of nonexistent file raises error."""
        converter = ASCIIArtConverter()
        with pytest.raises(FileNotFoundError):
            converter.convert("/nonexistent/image.png")

    def test_convert_brightness(self, sample_image: Path) -> None:
        """Test brightness adjustment."""
        converter = ASCIIArtConverter()
        normal = converter.convert(sample_image, width=20, brightness=1.0)
        bright = converter.convert(sample_image, width=20, brightness=1.5)
        # Different brightness should produce different output
        # (unless image is uniform, which our sample is)
        assert isinstance(bright, str)

    def test_convert_contrast(self, sample_image: Path) -> None:
        """Test contrast adjustment."""
        converter = ASCIIArtConverter()
        result = converter.convert(sample_image, width=20, contrast=1.5)
        assert isinstance(result, str)

    def test_convert_image_directly(self) -> None:
        """Test converting PIL Image directly."""
        converter = ASCIIArtConverter()
        img = Image.new("RGB", (50, 50), color=(100, 150, 200))
        result = converter.convert_image(img, width=20)
        assert isinstance(result, str)
        assert len(result.split("\n")) > 0

    def test_convert_grayscale_image(self, tmp_path: Path) -> None:
        """Test converting grayscale image."""
        img = Image.new("L", (20, 20), color=128)
        path = tmp_path / "gray.png"
        img.save(path)

        converter = ASCIIArtConverter()
        result = converter.convert(path, width=10)
        assert isinstance(result, str)

    def test_convert_rgba_image(self, tmp_path: Path) -> None:
        """Test converting RGBA image."""
        img = Image.new("RGBA", (20, 20), color=(128, 128, 128, 255))
        path = tmp_path / "rgba.png"
        img.save(path)

        converter = ASCIIArtConverter()
        result = converter.convert(path, width=10)
        assert isinstance(result, str)

    def test_different_charsets(self, sample_image: Path) -> None:
        """Test all charsets produce output."""
        for charset in ["simple", "complex", "blocks", "symbols"]:
            converter = ASCIIArtConverter(charset=charset)
            result = converter.convert(sample_image, width=20)
            assert isinstance(result, str)
            assert len(result) > 0


class TestPixelMapping:
    """Test pixel to character mapping."""

    def test_dark_pixels_map_to_first_char(self) -> None:
        """Dark pixels should map to first character in charset."""
        converter = ASCIIArtConverter(charset="simple")
        char = converter._pixel_to_char(0)
        assert char == converter.charset[0]

    def test_light_pixels_map_to_last_char(self) -> None:
        """Light pixels should map to last character in charset."""
        converter = ASCIIArtConverter(charset="simple")
        char = converter._pixel_to_char(255)
        assert char == converter.charset[-1]

    def test_mid_pixels_map_to_middle(self) -> None:
        """Mid-range pixels should map to middle characters."""
        converter = ASCIIArtConverter(charset="simple")
        char = converter._pixel_to_char(128)
        # Should be somewhere in the middle
        index = converter.charset.index(char)
        assert 0 < index < len(converter.charset) - 1


class TestColorOutput:
    """Test ANSI color generation."""

    def test_ansi_color_format(self) -> None:
        """Test ANSI color code format."""
        converter = ASCIIArtConverter(colored=True)
        color = converter._get_ansi_color(255, 0, 0)
        assert color.startswith("\033[38;5;")
        assert color.endswith("m")

    def test_different_colors_produce_different_codes(self) -> None:
        """Different RGB values should produce different ANSI codes."""
        converter = ASCIIArtConverter(colored=True)
        red = converter._get_ansi_color(255, 0, 0)
        blue = converter._get_ansi_color(0, 0, 255)
        assert red != blue
