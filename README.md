# BME547 Final Project-Image Processor

## Image Processing 
The image processing codes were done mainly utilizing the package `scikit-image`.
### Histogram Equalization
The function used from `scikit-image` is `skimage.exposure.equalize_hist()`. For grayscale images, the histogram equalization is done through calling the function once. For color images, the histogram equalizaion is performed in each color channel. The 3 color channels after equalization are used to form a new color image with `numpy.dstack`.
### Contrast Stretching
The function used from `scikit-image` is `skimage.exposure.rescale_intensity()`. What this function do is to make sure that the image has utilized the full range of the graylevel. Say, we have a 8-bit image, so the full range would be [0, 255]. If the original image sent in already has pixels with value of 0 and 255, which means the full range of graylevel has already been fully used, this function would actually do no change to the pixel values of the image. This might account for some processed images after contrast stretching look the same as the original ones.
### Log Compression
The function used from `scikit-image` is `skimage.exposure.adjust_log()`. For some images, no obvious differences appear between the original and processed images happens as the problem addressed above with contrast stretching. But if you check the pixel values, you can see the difference. What accounts for this problem might be the input images are already in good contrast. Because both contrast stretching and log compression are contrast adjustment functions, if the contrast is already good, no great changes can be generated through these functions.
### Reverse Video
The function used from `scikit-image` is `skimage.util.invert()`. This might be the function that can generate the most obvious change. What it's doing is something like turn white into black or turn black into white.

*More details about the functions used from `scikit-image` can be found on their official webpage: https://scikit-image.org/*

## Sphinx docstring
All the docstrings of functions can be found in folder `html`. Feel free to check them.
![pic1](https://github.com/SylviaCHS/BME547_Final_Project/blob/zl187/update_readme/images/pic1.PNG)