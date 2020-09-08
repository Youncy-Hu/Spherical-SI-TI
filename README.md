# Spherical-SI-TI
This python script is for SI and TI measurement for 360&deg; video in the spherical domain.

Considering planar representations (equirectangular, cube-map, etc.) change the characterization of the 360o content because of warping, discontinuities, etc., the spatial and temporal information measurement on 2D planar cannot represent the information subjects perceived using HMD. This algorithem calculates the spatial information (SI) and temporal information (TI) defined in [ITU-T P.910] in the spherical domain. The methodology please refer to [coming soon] and [Chen, 2018].

## __Requirement__
* python > 3.5
* opencv-python >= 3.4.2

## __How to Use__

```python main_cal_sph_SI_TI.py video_path save_folder_path```

## __Notes__
This script applies to 360&deg; video of equirectangular projection format. For other projection formats, please change the code of 2D-3D coordinate conversion and weight. The conversion and weight derivation methods for different projection formats are introduced in [JVET F1003].

## __Reference__
[Coming soon]...

[Chen, 2018] S. Chen, Y. Zhang, Y. Li, Z. Chen, and Z. Wang, "Spherical Structural Similarity Index for Objective Omnidirectional Video Quality Assessment," IEEE International Conference on Multimedia and Expo (ICME), July, 2018.

[JVET-F1003] Y. Ye, E. Alshina, and J. Boyce, "Algorithm descriptions of projection format conversion and video quality metrics in 360Lib," JVET-F1003, Hobart, AU, March 31-April 7, 2017.