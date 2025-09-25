#!/usr/bin/env python3
"""Module defining custom color palettes for PyMOL molecular visualization.

This module loads color palettes defined in ~/.pymol/palette.yaml into PyMOL.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from typing import Any, Optional

import pymol  # type: ignore[import-untyped]
from pymol import cmd


class PaletteColor:
    """Container for storing color information with multiple naming options.

    This class stores RGB color values along with primary and alternative names,
    and provides methods for color code generation and name management.

    Args:
        name: Primary name for the color.
        rgb: RGB color values in 0-255 range.
        alt_names: Alternative names for the color.
        short_code: 3-digit string approximating the RGB color for GUI menus.
                   If None, will be calculated from RGB values.

    Note:
        The short_code can be set explicitly in the palette definition. This is
        helpful for very dark colors, as it ensures that the color code used in
        the GUI menu provides sufficient contrast against the dark menu background.

    Examples
    --------
        >>> color = PaletteColor("red", (255, 0, 0))
        >>> color = PaletteColor("blue", (0, 0, 255), ["navy"], "009")
    """

    def __init__(
        self,
        name: str,
        rgb: tuple[int, int, int],
        alt_names: Optional[list[str]] = None,
        short_code: Optional[str] = None,
    ) -> None:
        self.name = name
        self.rgb = rgb
        self.alt_names = alt_names or []
        self.short_code = short_code

        # Validate RGB values
        if len(rgb) != 3:  # noqa: PLR2004
            raise ValueError(f"RGB tuple must have exactly 3 values, got {len(rgb)}: {rgb}")

        try:
            if not all(isinstance(value, (int, float)) and 0 <= value <= 255 for value in rgb):  # noqa: PLR2004
                raise ValueError(f"RGB values must be numbers in range 0-255, got: {rgb}")
        except TypeError as e:
            raise ValueError(f"RGB values must be numeric, got: {rgb}") from e

    def get_all_names(self) -> list[str]:
        """Return a list of all names for this color.

        Returns
        -------
            List containing primary name and any alternative names.
        """
        return [self.name, *self.alt_names]

    def get_short_code(self) -> str:
        """Return a 3-digit string approximating the RGB color.

        Returns
        -------
            3-digit string representing RGB values in 0-9 range.
        """
        if self.short_code:
            return self.short_code
        return "".join(str(math.floor(value / 255.0 * 10)) for value in self.rgb)

    def get_normalized_rgb(self) -> tuple[float, float, float]:
        """Return RGB values normalized to 0-1 range for PyMOL.

        Returns
        -------
            RGB values as floats in 0-1 range.
        """
        r, g, b = self.rgb
        return (r / 255.0, g / 255.0, b / 255.0)

    def __repr__(self) -> str:  # noqa: D105
        return f"PaletteColor('{self.name}', {self.rgb})"


class Palette:
    """Container for storing color palette information.

    This class manages a collection of colors with optional naming prefixes
    and provides methods for installation into PyMOL.

    Args:
        name: Name of the color palette.
        colors: List of PaletteColor objects in the palette.
        prefix: Prefix to add to color names when installing.

    Examples
    --------
        >>> colors = [PaletteColor("red", (255, 0, 0)), PaletteColor("blue", (0, 0, 255))]
        >>> palette = Palette("primary", colors, prefix="p_")
    """

    def __init__(self, name: str, colors: list[PaletteColor], prefix: str = "") -> None:
        self.name = name
        self.colors = colors
        self.prefix = prefix

        if not colors:
            raise ValueError("Palette must contain at least one color")

    def install(self) -> None:
        """Install the palette, adding colors and the GUI menu.

        This method registers the palette in the global palette map and
        adds it to the PyMOL color menu.
        """
        _PALETTES_MAP[self.name] = self
        add_palette_menu(self.name)
        print(f"Installed palette '{self.name}' with {len(self.colors)} colors")

    def get_color_names(self, include_prefix: bool = True) -> list[str]:
        """Get all color names in the palette.

        Args:
            include_prefix: Whether to include the palette prefix in names.

        Returns
        -------
            List of all color names in the palette.
        """
        names = []
        for color in self.colors:
            for name in color.get_all_names():
                if include_prefix and self.prefix:
                    names.append(f"{self.prefix}{name}")
                else:
                    names.append(name)
        return names

    def __len__(self) -> int:  # noqa: D105
        return len(self.colors)

    def __repr__(self) -> str:  # noqa: D105
        return f"Palette('{self.name}', {len(self.colors)} colors)"


def _get_palettes(palette_name: Optional[str] = None) -> list[Palette]:
    """Get the desired Palette(s).

    Args:
        palette_name: Name of specific palette to get, or None for all.

    Returns
    -------
        List of Palette objects.

    Raises
    ------
        ValueError: If specified palette name is not found.
    """
    if palette_name is None:
        return list(_PALETTES_MAP.values())

    if palette_name not in _PALETTES_MAP:
        available = ", ".join(_PALETTES_MAP.keys())
        raise ValueError(f'Palette "{palette_name}" not found. Available: {available}')

    return [_PALETTES_MAP[palette_name]]


def _add_palette_to_menu(palette: Palette) -> None:
    """Add a color palette to the PyMOL OpenGL menu.

    Args:
        palette: Palette object to add to menu.
    """
    # Ensure colors are installed
    print(f"Checking for {palette.name} colors...")
    try:
        for color in palette.colors:
            color_name = f"{palette.prefix}{color.name}" if palette.prefix else color.name
            if cmd.get_color_index(color_name) == -1:
                # Mimic pre-1.7.4 behavior
                raise pymol.CmdException
    except pymol.CmdException:
        print(f"Adding {palette.name} palette colors...")
        apply_palette_colors(palette_name=palette.name)

    # Add the menu
    print(f"Adding {palette.name} menu...")

    # Create menu items in the format PyMOL expects
    # Each item is a tuple: ('short_code', 'color_name')
    color_tuples = [
        (color.get_short_code(), f"{palette.prefix}{color.name}") for color in palette.colors
    ]
    menu_colors = (palette.name, color_tuples)

    # Add to PyMOL's color menu
    try:
        all_colors = pymol.pymol.menu.all_colors_list
    except (ImportError, AttributeError):
        print("PyMOL version too old for colors menu. Requires 1.6.0 or later.")
        return

    if menu_colors in all_colors:
        print(f"  - Menu for {palette.name} was already added!")
    else:
        all_colors.append(menu_colors)

    print("    done.\n")


def apply_palette_colors(
    palette_name: Optional[str] = None,
    *,
    replace_builtin: bool = False,
) -> None:
    """Add palette colors to PyMOL's color definitions.

    Args:
        palette_name: Name of the palette to add colors from.
                     If None, adds colors from all palettes.
        replace_builtin: Whether to replace built-in PyMOL colors with
                        palette colors when names conflict.

    Raises
    ------
        ValueError: If specified palette is not found.

    Examples
    --------
        # >>> apply_palette_colors("pastel")
        >>> apply_palette_colors()  # Apply all palettes
    """
    palettes = _get_palettes(palette_name)

    for palette in palettes:
        max_name_length = max(len(color.name) for color in palette.colors)
        added_colors = []

        for color in palette.colors:
            rgb_normalized = color.get_normalized_rgb()

            # Set colors for all names
            for name in color.get_all_names():
                # Add prefixed version
                prefixed_name = f"{palette.prefix}{name}" if palette.prefix else name
                cmd.set_color(prefixed_name, rgb_normalized)

                # Optionally replace built-in colors
                if replace_builtin:
                    cmd.set_color(name, rgb_normalized)
                    spacer = " " * (max_name_length - len(name) + 4)
                    added_colors.append(f"    {name}{spacer}{prefixed_name}")
                else:
                    added_colors.append(f"    {prefixed_name}")

        # Report newly available colors
        print(f"These {palette.name} colors are now available:")
        print("\n".join(added_colors))


def add_palette_menu(palette_name: Optional[str] = None) -> None:
    """Add color palette(s) to the PyMOL OpenGL menu.

    Args:
        palette_name: Name of the palette to add menu for.
                     If None, adds menus for all palettes.

    Raises
    ------
        ValueError: If specified palette is not found.

    Examples
    --------
        # >>> add_palette_menu("pastel")
        >>> add_palette_menu()  # Add all palette menus
    """
    palettes = _get_palettes(palette_name)
    for palette in palettes:
        _add_palette_to_menu(palette)


def remove_palette_menu(palette_name: Optional[str] = None) -> None:
    """Remove color palette menu(s) from PyMOL.

    Args:
        palette_name: Name of the palette menu to remove.
                     If None, removes all palette menus.

    Raises
    ------
        ValueError: If specified palette is not found.

    Examples
    --------
        # >>> remove_palette_menu("pastel")
        # >>> remove_palette_menu()  # Remove all palette menus
    """
    palettes = _get_palettes(palette_name)

    try:
        all_colors_list = pymol.pymol.menu.all_colors_list
    except (ImportError, AttributeError):
        print("PyMOL version does not support menu manipulation.")
        return

    for palette in palettes:
        initial_length = len(all_colors_list)
        all_colors_list[:] = [
            color_menu for color_menu in all_colors_list if color_menu[0] != palette.name
        ]

        if len(all_colors_list) == initial_length:
            print(f"No menu for {palette.name} palette found. Nothing deleted.")
        else:
            print(f"Deleted menu for {palette.name} palette.")


def list_available_palettes() -> None:
    """Print information about all available color palettes."""
    print("Available color palettes:")
    print("-" * 40)

    for name, palette in _PALETTES_MAP.items():
        print(f"{name:12} - {len(palette.colors):2d} colors")
        if palette.prefix:
            print(f"             Prefix: '{palette.prefix}'")

    print(f"\nTotal palettes: {len(_PALETTES_MAP)}")


def get_palette_info(palette_name: str) -> dict[str, Any]:
    """Get detailed information about a specific palette.

    Args:
        palette_name: Name of the palette to get information for.

    Returns
    -------
        Dictionary containing palette information.

    Raises
    ------
        ValueError: If palette is not found.

    Examples
    --------
        # >>> info = get_palette_info("pastel")
        # >>> print(f"Colors: {info['color_count']}")
    """
    if palette_name not in _PALETTES_MAP:
        available = ", ".join(_PALETTES_MAP.keys())
        raise ValueError(f'Palette "{palette_name}" not found. Available: {available}')

    palette = _PALETTES_MAP[palette_name]

    return {
        "name": palette.name,
        "color_count": len(palette.colors),
        "prefix": palette.prefix,
        "colors": [
            {
                "name": color.name,
                "rgb": color.rgb,
                "alt_names": color.alt_names,
                "short_code": color.get_short_code(),
                "all_names": color.get_all_names(),
            }
            for color in palette.colors
        ],
    }


def load_palette_colors(yaml_path: str | Path) -> dict[str, list[PaletteColor]]:
    """Load color palette definitions from a YAML file.

    Args:
        yaml_path: Path to the YAML file containing palette definitions

    Returns
    -------
        Dictionary mapping palette names to lists of PaletteColor objects
    """
    with open(yaml_path, "r") as f:
        palette_data = yaml.safe_load(f)

    palette_colors = {}
    for palette_name, colors in palette_data.items():
        color_list = []
        for name, rgb in colors.items():
            color_list.append(PaletteColor(name, tuple(rgb)))
        palette_colors[palette_name] = color_list

    return palette_colors


def create_palettes(palette_colors: dict[str, list[PaletteColor]]) -> dict[str, Palette]:
    """Create Palette objects from loaded palette colors.

    Args:
        palette_colors: Dictionary of palette names and their color lists

    Returns
    -------
        Dictionary mapping palette names to Palette objects
    """
    palettes = {}
    for name, colors in palette_colors.items():
        # Strip '_colors' suffix from palette name if present
        palette_name = name.replace("_colors", "")
        palettes[palette_name] = Palette(palette_name, colors)
    return palettes


def find_palette_file() -> Path:
    """Search for palette.yaml in multiple locations.

    Returns
    -------
        Path to the first found palette.yaml file

    Raises
    ------
        FileNotFoundError: If no palette.yaml is found in any location
    """
    # Search locations in order of precedence
    search_paths = [
        Path.cwd() / "palette.yaml",  # Current directory
        Path(os.getenv("PYMOL_CUSTOM_PALETTE", "")).expanduser(),  # Environment variable
        Path.home() / ".pymol" / "palette.yaml",  # User config directory
    ]

    for path in search_paths:
        print(path)
        if path.is_file():
            return path

    raise FileNotFoundError("No palette.yaml found!")


# Register PyMOL commands
cmd.extend("apply_palette_colors", apply_palette_colors)
cmd.extend("add_palette_menu", add_palette_menu)
cmd.extend("remove_palette_menu", remove_palette_menu)
cmd.extend("list_available_palettes", list_available_palettes)
cmd.extend("get_palette_info", get_palette_info)

# Define global instance
_PALETTES_MAP = {}

# Initialize menus when module is loaded by PyMOL
if __name__ == "pymol":
    print("PyMOL color palettes loaded and menus added.")

    # Load palettes from YAML
    palette_path = find_palette_file()
    palette_colors = load_palette_colors(palette_path)

    # Create palette objects and registry dynamically
    _PALETTES_MAP = create_palettes(palette_colors)
    add_palette_menu()


if __name__ == "__main__":
    print("PyMOL color palettes module loaded successfully.")
    print("Available commands: apply_palette_colors, add_palette_menu, remove_palette_menu")
    print("                    list_available_palettes, get_palette_info")
