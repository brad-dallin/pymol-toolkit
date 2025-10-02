#!/usr/bin/env python3
"""Module defining Goodsell-style spheres for PyMOL molecular visualization."""

####################################################################################################
## Import
####################################################################################################

from __future__ import annotations

from psico.viewing import goodsell_lighting
from pymol import cmd, util

####################################################################################################
## Define
####################################################################################################

def goodsell_spheres(
    obj: str,
    transparency: str = "0",
    ) -> None:
    """Style object or selection in Goodsell-like style spheres.

    Args
    ----
        obj: name of object or selection to apply styling
        transparency: transparency level between 0 to 1

    Returns
    -------
        None
    """
    if not cmd.count_atoms(obj):
        raise ValueError(f"No atoms found in: '{obj}'")

    cmd.hide("everything", obj)
    cmd.show("spheres", obj)
    cmd.set("sphere_transparency", transparency, obj)
    _set_goodsell_scene()


def _set_goodsell_scene() -> None:
    """Set lighting, style, and rendering parameters for David Goodsell-like style rendering."""
    # Set to max performance view
    util.performance(0)

    # Goodsell-like style
    cmd.space("cmyk")
    cmd.bg_color("white")
    cmd.set("specular", 0)
    cmd.set("depth_cue", 0)
    cmd.set("opaque_background", 1)
    cmd.set("show_alpha_checker", 0)

    # Goodsell-like lighting
    goodsell_lighting()

    # Goodsell-like rendering
    cmd.set("antialias", 2)
    cmd.set("ray_trace_mode", 3)
    cmd.set("ray_trace_gain", 0)
    cmd.set("ray_trace_color", "black")
    cmd.set("ray_trace_disco_factor", 1)
    cmd.set("ray_opaque_background", 1)
    cmd.set("ray_transparency_oblique")
    cmd.set("ray_transparency_oblique_power", 0)
    cmd.set("ray_transparency_contrast", 3)


####################################################################################################
## RUN
####################################################################################################

# Initialize function when loaded into PyMOL
if __name__ == "pymol":
    print("-- PyMOL David Goodsell-like style function added --")

    # Extend PyMOL commands
    cmd.extend("goodsell_spheres", goodsell_spheres)


if __name__ == "__main__":
    print("-- PyMOL David Goodsell-like style --")
