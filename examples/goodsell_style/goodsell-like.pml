# Fetch CIF
fetch 3jrs, async=0
remove not (alt ''+A)
alter all, alt=''

# Remove unnessary objects
remove chain B or chain C or solvent

# Initialize
hide everything

# Split receptor and ligand
extract a8s, resn a8s

# show it as blue/magenta spheres
as spheres
color lightblue, a8s
color lightmagenta, 3jrs
set sphere_transparency, 0.4, 3jrs

# Set view
set_view (\
    -0.001774734,   -0.310068041,    0.950711787,\
    -0.848823726,    0.503081799,    0.162493080,\
    -0.528671324,   -0.806700706,   -0.264085263,\
     0.000000000,    0.000000000, -202.115402222,\
    29.527511597,  -11.737289429,   27.301246643,\
  -1811.998535156, 2216.229736328,  -20.000000000 )

# Set to max performance view
util.performance(0)

# set the lights, ray tracing setttings
# to get the Goodsell-like rendering
space cmyk
bg_color white
#set opaque_background, 1
#set show_alpha_checker, 0
set specular, 0
set antialias, 2
set ray_trace_mode, 1
set ray_trace_color, black
set ray_trace_disco_factor, 1
#set ray_trace_trans_cutoff, 0.5
set ray_opaque_background, 1
set ray_transparency_oblique
set ray_transparency_oblique_power, 0
set ray_transparency_contrast, 3
set ambient, 0.5
unset depth_cue
