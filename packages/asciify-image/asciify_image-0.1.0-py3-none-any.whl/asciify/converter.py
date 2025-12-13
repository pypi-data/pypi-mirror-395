"""Core ASCII art conversion logic."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

from asciify.charsets import get_charset

if TYPE_CHECKING:
    from numpy.typing import NDArray


class ASCIIArtConverter:
    """Convert images to ASCII art with various options."""

    def __init__(
        self,
        charset: str = "simple",
        colored: bool = False,
        dither: bool = False,
    ) -> None:
        """Initialize the converter.

        Args:
            charset: Character set to use ('simple', 'complex', 'blocks', 'symbols')
            colored: Enable ANSI color output
            dither: Enable Floyd-Steinberg dithering
        """
        self.charset = get_charset(charset)
        self.colored = colored
        self.dither = dither
        self.terminal_width = shutil.get_terminal_size().columns

    def convert(
        self,
        image_path: str | Path,
        width: int | None = None,
        height: int | None = None,
        invert: bool = False,
        brightness: float = 1.0,
        contrast: float = 1.0,
    ) -> str:
        """Convert an image to ASCII art.

        Args:
            image_path: Path to the image file
            width: Output width in characters (auto-fits to terminal if None)
            height: Output height in characters
            invert: Invert the image colors
            brightness: Brightness adjustment factor (0.0-2.0)
            contrast: Contrast adjustment factor (0.0-2.0)

        Returns:
            ASCII art string

        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image cannot be processed
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        try:
            image = Image.open(image_path)
        except Exception as e:
            raise ValueError(f"Cannot open image: {e}") from e

        return self.convert_image(
            image,
            width=width,
            height=height,
            invert=invert,
            brightness=brightness,
            contrast=contrast,
        )

    def convert_image(
        self,
        image: Image.Image,
        width: int | None = None,
        height: int | None = None,
        invert: bool = False,
        brightness: float = 1.0,
        contrast: float = 1.0,
    ) -> str:
        """Convert a PIL Image to ASCII art.

        Args:
            image: PIL Image object
            width: Output width in characters
            height: Output height in characters
            invert: Invert the image colors
            brightness: Brightness adjustment factor
            contrast: Contrast adjustment factor

        Returns:
            ASCII art string
        """
        if image.mode != "RGB":
            image = image.convert("RGB")

        image = self._adjust_image(image, brightness, contrast)
        image = self._resize_image(image, width, height)

        grayscale = image.convert("L")
        if invert:
            grayscale = ImageOps.invert(grayscale)

        if self.dither:
            grayscale = self._apply_dithering(grayscale)

        return self._generate_ascii(image, grayscale)

    def _adjust_image(
        self,
        image: Image.Image,
        brightness: float,
        contrast: float,
    ) -> Image.Image:
        """Apply brightness and contrast adjustments."""
        if brightness != 1.0:
            image = ImageEnhance.Brightness(image).enhance(brightness)
        if contrast != 1.0:
            image = ImageEnhance.Contrast(image).enhance(contrast)
        return image

    def _resize_image(
        self,
        image: Image.Image,
        width: int | None,
        height: int | None,
    ) -> Image.Image:
        """Resize image maintaining aspect ratio."""
        orig_width, orig_height = image.size

        if width is None and height is None:
            width = min(orig_width, self.terminal_width)

        if width is not None:
            aspect_ratio = orig_height / orig_width
            # Compensate for terminal character aspect ratio (~2:1)
            new_height = int(aspect_ratio * width * 0.5)
            new_width = width
        else:
            aspect_ratio = orig_width / orig_height
            new_width = int(aspect_ratio * height * 2)
            new_height = height

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def _apply_dithering(self, image: Image.Image) -> Image.Image:
        """Apply Floyd-Steinberg dithering."""
        pixels: NDArray[np.floating] = np.array(image, dtype=np.float64)
        height, width = pixels.shape

        for y in range(height - 1):
            for x in range(width - 1):
                old_pixel = pixels[y, x]
                new_pixel = round(old_pixel / 255.0) * 255.0
                pixels[y, x] = new_pixel
                error = old_pixel - new_pixel

                # Distribute error to neighboring pixels
                pixels[y, x + 1] += error * 7 / 16
                if x > 0:
                    pixels[y + 1, x - 1] += error * 3 / 16
                pixels[y + 1, x] += error * 5 / 16
                pixels[y + 1, x + 1] += error * 1 / 16

        return Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8))

    def _pixel_to_char(self, pixel_value: int) -> str:
        """Map a grayscale pixel value to an ASCII character."""
        index = int(int(pixel_value) * (len(self.charset) - 1) // 255)
        return self.charset[min(index, len(self.charset) - 1)]

    def _get_ansi_color(self, r: int, g: int, b: int) -> str:
        """Convert RGB to ANSI 256-color escape code."""
        # Map to 6x6x6 color cube (indices 16-231)
        color_index = 16 + (36 * round(r * 5 / 255)) + (6 * round(g * 5 / 255)) + round(b * 5 / 255)
        return f"\033[38;5;{color_index}m"

    def _generate_ascii(
        self,
        color_image: Image.Image,
        grayscale_image: Image.Image,
    ) -> str:
        """Generate ASCII art from processed images."""
        gray_pixels: NDArray[np.uint8] = np.array(grayscale_image)
        color_pixels: NDArray[np.uint8] = np.array(color_image)
        lines: list[str] = []

        for y in range(gray_pixels.shape[0]):
            line_chars: list[str] = []
            for x in range(gray_pixels.shape[1]):
                char = self._pixel_to_char(gray_pixels[y, x])

                if self.colored:
                    r, g, b = color_pixels[y, x]
                    color_code = self._get_ansi_color(int(r), int(g), int(b))
                    line_chars.append(f"{color_code}{char}")
                else:
                    line_chars.append(char)

            line = "".join(line_chars)
            if self.colored:
                line += "\033[0m"  # Reset color at end of line
            lines.append(line)

        return "\n".join(lines)
