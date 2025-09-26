#!/usr/bin/env python3
"""Module defining custom color palettes for PyMOL molecular visualization.

This module loads color palettes defined in palette.yaml into PyMOL.
"""

####################################################################################################
## Import
####################################################################################################

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pymol  # type: ignore[import-untyped]
import yaml
from pymol import cmd

if TYPE_CHECKING:
    from typing import Any

####################################################################################################
## Define
####################################################################################################


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
        if path.is_file():
            return path

    raise FileNotFoundError("No palette.yaml found!")


def load_palette_colors(yaml_path: str | Path) -> dict[str, dict[str, list[Any]]]:
    """Load color palette definitions from a YAML file.

    Args
    ----
        yaml_path: Path to the YAML file containing palette definitions

    Returns
    -------
        Dict[str, List[str, Tuple[int, int, int]]]: Validated data structure
    """
    palette_data = _load_yaml(yaml_path)

    # return palette_colors
    return palette_data


def add_palette_colors(palettes: dict[str, dict[str, list[Any]]]) -> str:
    """Add palette colors to PyMOL's color definitions.

    Args
    ----
        Palettes loaded from yaml

    Raises
    ------
        ValueError: If specified palette is not found.

    Examples
    --------
        >>> msg = add_palette_colors({'oranges': {'darkorange': [198, 101, 38]}})  # Apply palette
    """
    for name, palette in palettes.items():
        added_colors = []
        color_tuples = []
        for color_name, rgb_list in palette.items():
            rgb_normalized = _get_normalized_rgb(rgb_list)
            rgb_short_code = _get_short_code(rgb_list)
            cmd.set_color(color_name, rgb_normalized)
            added_colors.append(f"    {color_name}")
            color_tuples.append((rgb_short_code, color_name))
        menu_colors = (name, color_tuples)
        try:
            all_colors = pymol.pymol.menu.all_colors_list
        except (ImportError, AttributeError) as e:
            raise ImportError(
                "PyMOL version too old for colors menu. Requires 1.6.0 or later."
            ) from e

        if menu_colors in all_colors:
            msg = f"  - Menu for {name} was already added!"
        else:
            all_colors.append(menu_colors)
            msg = f"\nThe {name} palette is now available:"
            msg += "\n".join(added_colors)
    return msg


def _load_yaml(file_path: str | Path) -> dict[str, dict[str, list[Any]]]:
    """Check input values from palette yaml file.

    Args
    ----
        file_path: Path to the YAML file containing palette definitions

    Returns
    -------
        Dict[str, Dict[str, List[int, int, int]]]: Validated data structure

    Raises
    ------
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the file contains invalid YAML
        ValueError: If the data structure doesn't match expected format
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as yf:
            data = yaml.safe_load(yf)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}") from e
    except Exception as e:
        raise Exception(f"Error reading file: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("YAML root must be a dictionary")

    if not data:
        raise ValueError("YAML file is empty or contains no data")

    validated_data = {}
    for name, items in data.items():
        if not isinstance(name, str):
            raise ValueError(f"Palette name must be a string, got {type(name).__name__}: {name}")

        if not isinstance(items, dict):
            raise ValueError(f"'{name}' palette must be a dictionary, got {type(items).__name__}")

        if not items:
            raise ValueError(f"No items found for name '{name}'")

        validated_items = {}
        for color_name, rgb_list in items.items():
            if not isinstance(color_name, str):
                raise ValueError(
                    f"Colors keys must be strings, got {type(color_name).__name__}: {color_name}"
                )

            if not isinstance(rgb_list, list):
                raise ValueError(
                    f"Value for '{name}.{color_name}' must be a list, got {type(rgb_list).__name__}"
                )

            if not rgb_list:
                raise ValueError(f"Empty list found for '{name}.{color_name}'")

            # Validate and convert rgb ints
            validated_ints = []
            if len(rgb_list) != 3:  # noqa: PLR2004
                raise ValueError(
                    f"RGB list must have exactly 3 values at '{name}.{color_name}': {rgb_list}"
                )

            for ii, value in enumerate(rgb_list):
                try:
                    # Convert to int if it's a valid number
                    if isinstance(value, (int, float)):
                        vv = int(value)
                    elif isinstance(value, str) and value.strip().lstrip("-").isdigit():
                        vv = int(value)
                    else:
                        raise ValueError(f"Invalid integer at '{name}.{color_name}[{ii}]': {value}")
                except (ValueError, TypeError):
                    raise ValueError(
                        f"Cannot convert to integer at '{name}.{color_name}[{ii}]': {value}"
                    ) from None
                if 0 <= vv <= 255:  # noqa: PLR2004
                    validated_ints.append(vv)
                else:
                    raise ValueError(
                        "RGB values must be numbers in range 0-255 at"
                        + f"'{name}.{color_name}[{ii}]': {value}"
                    )
            validated_items[color_name] = validated_ints
        validated_data[name] = validated_items
    return validated_data


def _get_normalized_rgb(rgb: list[Any]) -> tuple[float, float, float]:
    """Return RGB values normalized to 0-1 range for PyMOL.

    Returns
    -------
        RGB values as floats in 0-1 range.
    """
    r, g, b = rgb
    return (r / 255.0, g / 255.0, b / 255.0)


def _get_short_code(rgb: list[Any]) -> str:
    """Return a 3-digit string approximating the RGB color.

    Returns
    -------
        3-digit string representing RGB values in 0-9 range.
    """
    r, g, b = rgb
    return f"{int(r / 255.1 * 10)}{int(g / 255.1 * 10)}{int(b / 255.1 * 10)}"


####################################################################################################
## RUN
####################################################################################################

# Initialize menus when module is loaded by PyMOL
if __name__ == "pymol":
    print("PyMOL color palettes loaded and menus added.")

    # Load palettes from YAML
    palette_path = find_palette_file()
    palette_colors = load_palette_colors(palette_path)
    msg = add_palette_colors(palette_colors)
    print(msg)


if __name__ == "__main__":
    print("-- PyMOL custom color palettes --")

    # Load palettes from YAML
    palette_path = find_palette_file()
    palette_colors = load_palette_colors(palette_path)
    msg = add_palette_colors(palette_colors)
    print(msg)
