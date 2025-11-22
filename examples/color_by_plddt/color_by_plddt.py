#!/usr/bin/env python3
"""Module defining Goodsell-style spheres for PyMOL molecular visualization."""

####################################################################################################
## Import
####################################################################################################

from __future__ import annotations

####################################################################################################
## Define
####################################################################################################

def color_by_plddt(
        obj: str,
        very_high_threshold: float = 90.0,
        high_threshold: float = 70.0,
        low_threshold: float = 50.0,
    ) -> None:
    """Color atoms by AlphaFold pLDDT (predicted Local Distance Difference Test) score.

    Args
    ----
        obj: name of object or selection to apply styling
        very_high_threshold: very high confidence level (default: 90.0)
        high_threshold: high confidence level (default: 70.0)
        low_threshold: low confidence level (default: 50.0)

    Returns
    -------
        None
    """
    if not cmd.count_atoms(obj):
        raise ValueError(f"No atoms found in: '{obj}'")

    if not (very_high_threshold > high_threshold > low_threshold):
        raise ValueError("Thresholds must be in descending order: very_high > high > low")

    _setup_plddt_colors()

    atom_data = []
    cmd.iterate(obj, 'atom_data.append((index, b))', space={'atom_data': atom_data})

    if not atom_data:
        raise ValueError(f"No B-factor data found for selection: '{obj}'")

    for atom_index, b_factor in atom_data:
        color_name = _get_plddt_color_name(
            b_factor,
            very_high_threshold,
            high_threshold,
            low_threshold
        )
        cmd.color(color_name, f"index {atom_index}")


def _setup_plddt_colors() -> None:
    """Set up pLDDT color definitions in PyMOL."""
    colors = {
        'very_high': (33, 81, 204),
        'high': (127, 201, 239),
        'low': (249, 220, 77),
        'very_low': (238, 132, 83)
    }

    # Set PyMOL colors (convert from 0-255 to 0-1 range)
    for confidence_level, rgb in colors.items():
        color_name = f"plddt_{confidence_level}"
        rgb_normalized = [c / 255.0 for c in rgb]
        cmd.set_color(color_name, rgb_normalized)


def _get_plddt_color_name(
        b_factor: float,
        very_high_threshold: float,
        high_threshold: float,
        low_threshold: float) -> str:
    """Determine the appropriate pLDDT color name based on B-factor value."""
    if b_factor > very_high_threshold:
        return "plddt_very_high"
    elif b_factor > high_threshold:
        return "plddt_high"
    elif b_factor > low_threshold:
        return "plddt_low"
    else:
        return "plddt_very_low"


####################################################################################################
## RUN
####################################################################################################

# Initialize function when loaded into PyMOL
if __name__ == "pymol":
    print("\n-- PyMOL Color by PLDDT --\n")

    # Extend PyMOL commands
    cmd.extend("color_by_plddt", color_by_plddt)


if __name__ == "__main__":
    print("\n-- PyMOL Color by PLDDT --\n")
