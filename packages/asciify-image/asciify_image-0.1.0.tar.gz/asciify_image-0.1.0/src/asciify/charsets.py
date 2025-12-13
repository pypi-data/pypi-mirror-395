"""Character sets for ASCII art conversion."""

CHARSETS = {
    "simple": " .:-=+*#%@",
    "complex": ' .",:;!~+-xmo*#W&8@',
    "blocks": "⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏",  # Braille patterns
    "symbols": " ▀▄█",  # Block elements
}


def get_charset(name: str) -> str:
    """Get a character set by name.

    Args:
        name: Name of the character set ('simple', 'complex', 'blocks', 'symbols')

    Returns:
        String of characters ordered from darkest to lightest

    Raises:
        ValueError: If charset name is not recognized
    """
    if name not in CHARSETS:
        valid = ", ".join(CHARSETS.keys())
        raise ValueError(f"Unknown charset '{name}'. Valid options: {valid}")
    return CHARSETS[name]
