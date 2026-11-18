import cv2 as cv
import ImageFilters

def main():
    image_path = "src/TrabalhoGrauB/baboon.png"
    #imgOriginal, imgAltered = ImageFilters.gaussian_blur(image_path, 10)
    imgOriginal, imgAltered = ImageFilters.sharpening_filter(image_path, 1)

    cv.imshow('Imagem Original', imgOriginal)
    cv.imshow('Imagem Alterada',imgAltered)
    k = cv.waitKey(0)


if 1 == 1:
    main()


