#!/usr/bin/env pymol
# -*- coding: utf-8 -*-
"""pymol_toolkit package."""

# ADD CUSTOM PALETTES
cmd.run(f"{PYMOL_TOOLKIT}/load_palette.py")

# ADD GOODSELL STYLE FUNCTIONS
cmd.run(f"{PYMOL_TOOLKIT}/goodsell_style.py")
