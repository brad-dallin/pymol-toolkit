#!/usr/bin/env python3
"""Module providing custom styles for PyMOL.

This module defines custom styling configurations for PyMOL molecular visualization,
including Van der Waals radii settings and rendering parameters.
"""

from __future__ import annotations

from pymol import cmd  # type: ignore[import-untyped]

# Bondi Van der Waals radii values (in Angstroms)
BONDI_VDW_RADII: dict[str, float] = {
    "H": 1.00,  # 1
    "He": 1.40,  # 2
    "Li": 1.82,  # 3
    "Be": 2.00,  # 4
    "B": 2.00,  # 5
    "C": 1.70,  # 6
    "N": 1.55,  # 7
    "O": 1.52,  # 8
    "F": 1.47,  # 9
    "Ne": 1.54,  # 10
    "Na": 2.27,  # 11
    "Mg": 1.73,  # 12
    "Al": 2.00,  # 13
    "Si": 2.10,  # 14
    "P": 1.80,  # 15
    "S": 1.80,  # 16
    "Cl": 1.75,  # 17
    "Ar": 1.88,  # 18
    "K": 2.75,  # 19
    "Ca": 2.00,  # 20
    "Sc": 2.00,  # 21
    "Ti": 2.00,  # 22
    "V": 2.00,  # 23
    "Cr": 2.00,  # 24
    "Mn": 2.00,  # 25
    "Fe": 2.00,  # 26
    "Co": 2.00,  # 27
    "Ni": 1.63,  # 28
    "Cu": 1.40,  # 29
    "Zn": 1.39,  # 30
    "Ga": 1.87,  # 31
    "Ge": 2.00,  # 32
    "As": 1.85,  # 33
    "Se": 1.90,  # 34
    "Br": 1.85,  # 35
    "Kr": 2.02,  # 36
    "Rb": 2.00,  # 37
    "Sr": 2.00,  # 38
    "Y": 2.00,  # 39
    "Zr": 2.00,  # 40
    "Nb": 2.00,  # 41
    "Mo": 2.00,  # 42
    "Tc": 2.00,  # 43
    "Ru": 2.00,  # 44
    "Rh": 2.00,  # 45
    "Pd": 1.63,  # 46
    "Ag": 1.72,  # 47
    "Cd": 1.58,  # 48
    "In": 1.93,  # 49
    "Sn": 2.17,  # 50
    "Sb": 2.00,  # 51
    "Te": 2.06,  # 52
    "I": 1.98,  # 53
    "Xe": 2.16,  # 54
    "Cs": 2.00,  # 55
    "Ba": 2.00,  # 56
    "La": 2.00,  # 57
    "Ce": 2.00,  # 58
    "Pr": 2.00,  # 59
    "Nd": 2.00,  # 60
    "Pm": 2.00,  # 61
    "Sm": 2.00,  # 62
    "Eu": 2.00,  # 63
    "Gd": 2.00,  # 64
    "Tb": 2.00,  # 65
    "Dy": 2.00,  # 66
    "Ho": 2.00,  # 67
    "Er": 2.00,  # 68
    "Tm": 2.00,  # 69
    "Yb": 2.00,  # 70
    "Lu": 2.00,  # 71
    "Hf": 2.00,  # 72
    "Ta": 2.00,  # 73
    "W": 2.00,  # 74
    "Re": 2.00,  # 75
    "Os": 2.00,  # 76
    "Ir": 2.00,  # 77
    "Pt": 1.72,  # 78
    "Au": 1.66,  # 79
    "Hg": 1.55,  # 80
    "Tl": 1.96,  # 81
    "Pb": 2.02,  # 82
    "Bi": 2.00,  # 83
    "Po": 2.00,  # 84
    "At": 2.00,  # 85
    "Rn": 2.00,  # 86
    "Fr": 2.00,  # 87
    "Ra": 2.00,  # 88
    "Ac": 2.00,  # 89
    "Th": 2.00,  # 90
    "Pa": 2.00,  # 91
    "U": 1.86,  # 92
    "Np": 2.00,  # 93
    "Pu": 2.00,  # 94
    "Am": 2.00,  # 95
    "Cm": 2.00,  # 96
    "Bk": 2.00,  # 97
    "Cf": 2.00,  # 98
    "Es": 2.00,  # 99
    "Fm": 2.00,  # 100
    "Md": 2.00,  # 101
    "No": 2.00,  # 102
    "Lr": 2.00,  # 103
    "Rf": 2.00,  # 104
    "Db": 2.00,  # 105
    "Sg": 2.00,  # 106
    "Bh": 2.00,  # 107
    "Hs": 2.00,  # 108
    "Mt": 2.00,  # 109
    "Ds": 2.00,  # 110
}


def apply_bondi_vdw_radii() -> None:
    """Apply Bondi Van der Waals radii to all elements in PyMOL.

    Updates the VDW radii for all elements according to Bondi's values
    and rebuilds the molecular representation.
    """
    print("Updating VDW radii with Bondi values...")
    for element, vdw_radius in BONDI_VDW_RADII.items():
        cmd.alter(f"elem {element}", f"vdw={vdw_radius:.2f}")
    cmd.rebuild()
    print(f"Applied VDW radii for {len(BONDI_VDW_RADII)} elements.")


def apply_custom_style() -> None:
    """Apply custom style settings to PyMOL for enhanced visualization.

    Configures PyMOL with optimized settings for:
    - Color space and background
    - Lighting and reflections
    - Rendering quality
    - Shader usage
    - Display modes
    - Label appearance
    """
    # Display settings
    cmd.space("cmyk")
    cmd.bg_color("white")
    cmd.set("depth_cue", 0)
    cmd.set("orthoscopic", 0)

    # Lighting settings (modified rubber preset)
    lighting_settings = {
        "ambient": 0.3,
        "reflect": 0.4,
        "direct": 0.3,
        "spec_direct": 0,
        "spec_direct_power": 55,
        "light_count": 6,
        "edit_light": 1,
        "spec_count": -1,
        "shininess": 10.0,
        "spec_reflect": -0.01,
        "specular": 1,
        "specular_intensity": 0.5,
        "ambient_occlusion_mode": 0,
        "ambient_occlusion_scale": 25,
        "ambient_occlusion_smooth": 10,
        "power": 1,
        "reflect_power": 1,
        "two_sided_lighting": 1,
    }

    for setting, value in lighting_settings.items():
        cmd.set(setting, value)

    # Rendering settings
    rendering_settings = {
        "antialias": 2,
        "ray_shadow": 0,
        "line_smooth": 1,
        "ray_trace_mode": 1,
        "opaque_background": 1,
    }

    for setting, value in rendering_settings.items():
        cmd.set(setting, value)

    # Enable shaders for all rendering modes
    shader_settings = {
        "use_shaders": 1,
        "cgo_use_shader": 1,
        "dot_use_shader": 1,
        "dash_use_shader": 1,
        "line_use_shader": 1,
        "mesh_use_shader": 1,
        "stick_use_shader": 1,
        "ribbon_use_shader": 1,
        "sphere_use_shader": 1,
        "surface_use_shader": 1,
        "cartoon_use_shader": 1,
        "nonbonded_use_shader": 1,
        "nb_spheres_use_shader": 1,
    }

    for setting, value in shader_settings.items():
        cmd.set(setting, value)

    # Display mode settings
    display_settings = {
        "valence": 0,
        "stick_ball": 1,
        "stick_h_scale": 1,
        "sphere_mode": 5,
        "dot_as_spheres": 1,
        "surface_quality": 2,
        "ribbon_sampling": 20,
        "cartoon_sampling": 20,
        "transparency_mode": 2,
        "dash_as_cylinders": 1,
        "line_as_cylinders": 1,
        "mesh_as_cylinders": 1,
        "stick_as_cylinders": 1,
        "render_as_cylinders": 1,
        "ribbon_as_cylinders": 1,
        "nonbonded_as_cylinders": 1,
        "alignment_as_cylinders": 1,
        "cartoon_nucleic_acid_as_cylinders": 1,
        "cartoon_transparency": 0,
        "cartoon_discrete_colors": 1,
        "cartoon_side_chain_helper": 1,
    }

    for setting, value in display_settings.items():
        cmd.set(setting, value)

    # Label settings
    cmd.set("label_size", 24)
    cmd.set("label_color", 1)
    cmd.set("label_bg_color", 0)
    cmd.set("label_bg_transparency", 0.8)
    cmd.set("label_outline_color", 1)
    cmd.set("label_position", [0, 2.5, 10])

    print("Custom PyMOL style applied successfully.")


def initialize_pymol_environment() -> None:
    """Initialize PyMOL with custom settings and VDW radii.

    This function combines both VDW radii updates and style application
    for a complete PyMOL environment setup.
    """
    apply_bondi_vdw_radii()
    apply_custom_style()


# Register PyMOL commands
cmd.extend("apply_custom_style", apply_custom_style)
cmd.extend("apply_bondi_vdw_radii", apply_bondi_vdw_radii)
cmd.extend("initialize_pymol_environment", initialize_pymol_environment)

if __name__ == "__main__":
    # Auto-initialize when run as a script
    initialize_pymol_environment()
