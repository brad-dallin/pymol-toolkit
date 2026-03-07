# Fetch CIF
fetch 3jrs, async=0
remove not (alt ''+A)
alter all, alt=''

# Remove unnessary objects
remove chain B or chain C or solvent
