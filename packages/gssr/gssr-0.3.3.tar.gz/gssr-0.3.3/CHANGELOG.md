# Change Log

All notable changes to this project will be documented in this file.

## [v0.3.3] - 2025-12-05
- Remove --wrap / -w option and replace it with positional argument. Now user's command just have to be at the end of gssr command.
- Fix bug when -o flag is used. One folder level is not created and caused issue when analyzing the results. 
- Improve readability of plots by 
   (1) Include units for all plots

   (2) Update y axis so that the values are more readable

## [gssr-v0.3] - 2025-08-13
### New
- Change name to gssr for (Gpu Saturation ScoreR) as gss is already reserved at pypi


## [v0.2] - 2025-08-12

### New
- Installation directly from GitHub and pypi
- Added License file and Change Log
- Simplify usage (-l and -o flags are no longer mandatory)

### Changed
- Fixed font issue due to Latin-1 encoding
- Tool failed when a single GPU is used now returns a warning message instead of an error while generating heatmaps
- Improved tool verbosity
- Update name from agi to gss (GPU Saturation Scorer)
- Removed the restriction to not print heatmap when `np.abs(y).max() > 1e-3` (until motivation is understood)
- Fix bug when command is too long and cause a the table to overflow to the next page (not supported). Only the first 500 characters will now be shared to prevent the overflow.

