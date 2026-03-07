#!/usr/bin/env python3
"""Module defining pretty-style for PyMOL molecular visualization."""

####################################################################################################
## Import
####################################################################################################

from __future__ import annotations

from pymol import cmd, util

####################################################################################################
## Define
####################################################################################################


def pretty_surface(
    obj: str,
    color: str = "grey95",
    transparency: str = "0.5",
) -> None:
    """Style object or selection in pretty style surface with cartoon ribbon layer behind.

    Args
    ----
        obj: name of object or selection to apply styling
        color: surface color
        transparency: transparency level between 0 to 1

    Returns
    -------
        None
    """
    if not cmd.count_atoms(obj):
        raise ValueError(f"No atoms found in: '{obj}'")

    cmd.hide("everything", obj)
    cmd.show("cartoon", obj + " and polymer")
    cmd.show("surface", obj + " and polymer")
    cmd.set("surface_color", color, obj + " and polymer")
    cmd.set("transparency", transparency, obj + " and polymer")
    _set_pretty_scene()


def _set_pretty_scene() -> None:
    """Set lighting, style, and rendering parameters for pretty style rendering."""
    # Set to max performance view
    util.performance(0)

    # Pretty style
    cmd.space("cmyk")
    cmd.bg_color("white")
    cmd.set("specular", 1)
    cmd.set("depth_cue", 0)
    cmd.set("orthoscopic", 0)
    cmd.set("opaque_background", 1)
    cmd.set("show_alpha_checker", 0)
    cmd.set("ambient", 0.5)
    cmd.set("spec_count", 5)
    cmd.set("shininess", 50)
    cmd.set("reflect", 0.1)

    # Pretty rendering
    cmd.set("antialias", 2)
    cmd.set("ray_trace_mode", 1)
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
    print("\n-- PyMOL pretty style --\n")

    # Extend PyMOL commands
    cmd.extend("pretty_surface", pretty_surface)


if __name__ == "__main__":
    print("\n-- PyMOL pretty style --\n")
