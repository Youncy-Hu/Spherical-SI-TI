# Spherical-SI-TI
This python script is for SI and TI measurement in the spherical domain for 360&ordm video.

## __Requirement__
* Python > 3.5
* OpenCV

## __How to Use__

```python main_cal_sph_SI_TI.py video_path save_folder_path```

## __Attention__
This script applies to 360&ordm video of equirectangular projection format. For other projection formats, please change the code of 2D-3D coordinate conversion and weight. The conversion and weight derivation methods for different projection formats are introduced in [JVET F1003].
[JVET-F1003] Y. Ye, E. Alshina, and J. Boyce, “Algorithm descriptions of projection format conversion and video quality metrics in 360Lib,” JVET-F1003,Hobart, AU, March 31-April 7, 2017.