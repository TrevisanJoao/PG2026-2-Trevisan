import numpy as np
import cv2 as cv


def grayscale_filter(image_path):
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

def gaussian_blur(image_path, intensity, channel_R=True, channel_G=True, channel_B=True):
    # 
    img = cv.imread(image_path)
    # copy() creates a indpendent copy of a image
    imgR = img.copy() 
    imgG = img.copy()
    imgB = img.copy()

    height = img.shape[0]
    lenght = img.shape[1]


    return None

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

def sharpening():
    # increases the image details definition
    return None