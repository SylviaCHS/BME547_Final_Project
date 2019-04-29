# BME547_Final_Project

Huis Cai, Kimberly Lennox, Zhen Lin

last update: 04/28/2019

## Overview
For the image processor project, our team designed and implemented a software system to upload image(s) or an archive of images to a web-server, perform image-processing tasks on the web-server, and then display / download the processed image(s). 

The following image processing methods can be implemented to the images: 
  + Histogram Equalization __default__
  + Contrast Stretching
  + Log Compression
  + Reverse Video  
The results will be stored in the database.

Image(s) can be retrieved by selecting one or multiple files in the listbox. If one image is selected, results will be also displayed in the GUI so that user can compare the original and processed images, as well as the corresponding histograms. Some useful metadata are also available in a pop-up window. When multiple files are selected, a zip archive of the processed image of a specified image type will be stored in a designated folder.

## Instruction Manual
### Deploy to Virtual Machine
The server has been deployed to VCM. The hostname and port is:
```
vcm-9030.vm.duke.edu:5000
```
Note: If want to run it locally, please refer to the other release from branch `local_server`

### View Our Instruction Video!!

For instruction, please watch our instruction video under the git repo master branch called "FinalInstructionVideo.mp4".
It seems slow but we promise it is faster now!

### Upload Image(s) or A Zipfile to Run Analysis on Server
- First, user needs to type a user name. If a new user, please check the box `New User`. If the user name already exists, you would get an error on the right of the `run analysis`, so please choose another name. If a new user forget to check the box, an error message will also be displayed.
- Then, user needs to click import file. User can choose one or more image file(s) or one zip archive to import. The program accepts most image types. While other types of file or more than one zip files are chosen, an error will be displayed.
- User can also choose one proessing method. The default method is histogram equalization.
- Now, click the `run analysis` and let the it run! When finished, `Imaged saved successfully` should be displayed on the right of the button. All the processed images will be save to the database.

### Select and Download Processed Image(s) from Server
On the bottom half of the GUI, it allows users to choose, display, and download images.
- Load File(s): first please make sure the user name is correct, then click the `Load File(s)` button. All the processed images should be listed with the processing method append to it.
- Select File(s): Select one or more files in the listbox under `Load File(s)` by clicking them. The selected files will be hightlighted in blue. 
- Optional: Choose the desired image type by selecting in the dropdown menu. Default is JPEG.
- Download File(s): Click `Download File(s)`. A window will pop up to let user to choose the folder he/she wants to save the iamge(s) in. For single file, original and processed image, as well as the matching histogram will be automatically display in the GUI. For multiple files, no images will be displayed, but images will be save as a zip file called `processed_images.zip`.
A message will be displayed to indicated iamge(s) saved successfully.
- Metrics: User metrics and image metrics will be displayed in pop-up windows. The metrics includes:
    - Timestamp when uploaded
    - Time to process the image(s)
    - Image size   
    - User metrics: 
        - how many times has a user run each processing method
        - latency for running the method
## Database Structure
The software uses MongoDB as the database. The follow fields existed in MongoDB:
    - UserID (str): user name as the primary key
    - timestamp (list): Timestamp when the image is saved to database
    - ImageFile (list): A list of dictionaries for each image containing all the necessary information (more details shown below)
    - filenames (list): A list string of all the filenames existed in the database
    - raw_image (list): A list of boolen values of whether the image is original or processed image.
    
 The ImageFile dictionary contains the following keys:
     ```
     Image_Dict = {
                    "File": filename, # filename (str)
                    "Image": image_tif, # image array in tiff format (nparray)
                    "Process": process, # process method (str)
                    "Timestamp": time, # timestamp (str)
                    "Latency": latency, # time to process the image (float)
                    "Size": size, # size of image (list)
                    "Histogram": hist, # image array of histogram (nparray)
                 }
     ```
### Warnings
Occasionally, the MongoDB could be really slow when the size of the stored data is too large or when the server is overload. If the GUI is not responding for a long time, please contact one of our team member to request to change database/ clear the history.

### Status Code
  `400` : There is an error and data is not processed. Error could include: Missing keys, wrong file type, user ID is not in the database, new user ID already exist, cannot find image in databse, etc.
  `200` : Requests has been processed sucessfully.

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

## MIT License

Copyright (c) [2019] [Huisi Cai]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
