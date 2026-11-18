import numpy as np
import cv2 as cv


def grayscale_filter(image_path: str):
    # removes the image colors and preserves the luminosity, turning it gray
    img = cv.imread(image_path)
    if img is None:
        print("Error: Could not load image!")
        return None, None
    imgGrayScale = img.copy()

    height = img.shape[0]
    lenght = img.shape[1]

    for i in range (height):
        for j in range (lenght):
            # obtain the values of R, G, and B channels of each pixel i and j
            b = img.item(i,j,0) # Blue Channel - B
            g = img.item(i,j,1) # Green Channel - G
            r = img.item(i,j,2) # Red Channel - R

            weightedAverage = r * 0.2125 + g * 0.7154 + b * 0.0721
            imgGrayScale[i,j,0] = weightedAverage 
            imgGrayScale[i,j,1] = weightedAverage
            imgGrayScale[i,j,2] = weightedAverage

    return img, imgGrayScale

def gaussian_blur(image_path: str, intensity: int):
    # reduce sharpness and detail making an image appear smoother
    ratio = 3  + (intensity * 2)
    img = cv.imread(image_path)
    gaussian = cv.GaussianBlur(img, (ratio, ratio), 0)
    return img, gaussian

def sharpening_filter(image_path: str, intensity: int):
    # increases the image details definition
    img = cv.imread(image_path)
    adjacent_pixel = -(intensity / 2)
    central_pixel = (intensity * 3)
    first_array = [0, adjacent_pixel, 0]
    second_array = [adjacent_pixel, central_pixel, adjacent_pixel]
    third_array = first_array
    kernel = np.array([first_array, second_array, third_array])
    sharpened_image = cv.filter2D(img, -1, kernel)
    return img, sharpened_image

def enhancement_filter():
    #
    return None 

def negative_filter():
    # inver the colors
    return None

def sepia_filter():
    # make is looks old
    return None

def thresholding_filter():
    # make it pure black and white
    return None

def canny_edge_detection_filter():
    # shows only the image edges
    return None

def cartoon_effec():
    # makes the image look like a cartoon
    return None

