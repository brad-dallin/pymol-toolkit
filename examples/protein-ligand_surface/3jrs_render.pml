# Fetch CIF
fetch 3jrs, async=0
remove not (alt ''+A)
alter all, alt=''

# Remove unnessary objects
remove chain B or chain C or solvent

# Initialize
hide everything
show spheres

# Split receptor and ligand
extract a8s, resn a8s

# Color receptor
set sphere_color, palegreen, 3jrs and elem C
set sphere_color, tv_green, 3jrs and not elem C

# Color ligand
set sphere_color, lightpink, a8s and elem C
set sphere_color, lightmagenta, a8s and not elem C

# Setup
space cmyk
set bg_rgb, white
set show_alpha_checker, 0
set opaque_background, 1


# Set view
set_view (\
    -0.001774734,   -0.310068041,    0.950711787,\
    -0.848823726,    0.503081799,    0.162493080,\
    -0.528671324,   -0.806700706,   -0.264085263,\
     0.000000000,    0.000000000, -158.014907837,\
    29.527511597,  -11.737289429,   27.301246643,\
   124.580162048,  191.449661255,  -20.000000000 )
