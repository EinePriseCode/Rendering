#Overview
You can find several Python modules *sceneX.py* in */scene* defining scene objects used 
for rendering the images in */images* as *imageX.ppm* files. 
Those images are converted to .png files with */base/image_converter.py* and saved in */images_report*.
The documentation *report.pdf* is located in */report* directory.

#Starting examples
Open a terminal in the */Rendering* directory. Make sure your Python environment is set up and started properly.\
Following Python libraries have to be installed:
 - NumPy
 - OpenCV (for image_converter.py only)

Start rendering a *sceneX* by following command (-m to run a Python module):
```console
python -m scenes.sceneX
```
For custom usage the implementation of the base package may be different and must be adjusted.

:warning: **WARNING**: Pulling the repository includes all rendered example images (*/images* itself has as size of 860mb)