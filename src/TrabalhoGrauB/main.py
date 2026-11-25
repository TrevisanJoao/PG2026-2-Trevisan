import cv2 as cv
import ImageFilters
import Stickers
import Interface

def main():
    #image_path = "src/TrabalhoGrauB/baboon.png"
    #sticker_image_path = "src/TrabalhoGrauB/sticker.png"
    #imgOriginal, imgAltered = ImageFilters.gaussian_blur(image_path, 10)
    #imgOriginal, imgAltered = ImageFilters.sharpening_filter(image_path, 1)

    #cv.imshow('Imagem Original', imgOriginal)
    #cv.imshow('Imagem Alterada',imgAltered)

    #nome_janela = 'Modo Foto - Aplicacao de Stickers'
    #cv.namedWindow(nome_janela)
    #cv.setMouseCallback(nome_janela, Stickers.mouse_callback)
    img = None
    video = None

    current_menu = 0
    running = True
    while running == True:

        match current_menu:
            case 0:
                #shows the main menu
                current_menu = Interface.show_welcome_menu()
            case 1:
                #show the edit image menu
                current_menu, img = Interface.show_image_edit_menu()
            case 2:
                current_menu = Interface.show_image_edit_options_menu(img)
            case 3:
                current_menu, video = Interface.show_video_edit_menu()
            case 4:
                current_menu = Interface.show_video_edit_options_menu()
            case 5:
                current_menu = Interface.save_image_or_video()
            case 3:
                running = False

    return None


if 1 == 1:
    main()


