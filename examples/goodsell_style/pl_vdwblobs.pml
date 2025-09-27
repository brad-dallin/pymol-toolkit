# Fetch CIF
fetch 3jrs, async=0
remove not (alt ''+A)
alter all, alt=''



# Color receptor
set sphere_color, palegreen, 3jrs and elem C
set sphere_color, tv_green, 3jrs and not elem C

# Color ligand
set sphere_color, lightpink, a8s and elem C
set sphere_color, lightmagenta, a8s and not elem C

# Set view
set_view (\
    -0.001774734,   -0.310068041,    0.950711787,\
    -0.848823726,    0.503081799,    0.162493080,\
    -0.528671324,   -0.806700706,   -0.264085263,\
     0.000000000,    0.000000000, -202.115402222,\
    29.527511597,  -11.737289429,   27.301246643,\
   168.680648804,  235.550155640,  -20.000000000 )

# Setup scene
util.performance(0)
space cmyk
set bg_rgb, white
set show_alpha_checker, 0
set opaque_background, 1