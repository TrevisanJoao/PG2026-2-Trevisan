import cv2 as cv
import ImageFilters

def main():
    image_path = "src/TrabalhoGrauB/baboon.png"
    imgOriginal, imgAltered = ImageFilters.grayscale_filter(image_path)

    cv.imshow('Imagem Original', imgOriginal)
    cv.imshow('Canal Grayscale',imgAltered)
    k = cv.waitKey(0)


if 1 == 1:
    main()


