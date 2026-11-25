import cv2 as cv
import ImageFilters
import Stickers

# Menus codification
# 1 = welcome menu
# 2 = image edition menu
current_menu = 1

def show_welcome_menu():
    print("===========")
    print("Bem vindo a tela inicial s2")
    print("O que você deseja edita?")
    print("-----------")
    print("Opção 1 - Imagem")
    print("Opção 2 - Vídeo")
    print("Opção 3 - Sair")
    print("-----------")
    print("===========")
    valid_option = False
    while valid_option == False:
        option = int(input("Escolha sua opção (1, 2 ou 3) : "))
        if(option == 1 or option == 2 or option == 3):
            valid_option = True
        else:
            print("Opção Inválida")
    return option

def show_image_edit_menu():
    print("===========")
    print("Bem vindo ao menu de edição de imagem s2")
    print("-----------")
    print("Provenha o path absoluto da imagem ou insira '1' para voltar")
    print("-----------")
    print("===========")
    valid_option = False
    while valid_option == False:
        image_absolute_path = input("Insira o path absoluto da imagem (ex: C:/Users/User1/Imagens/Screenshots/image.png): ")
        image = cv.imread(image_absolute_path)
        if image_absolute_path == 1:
            return image_absolute_path
        elif image is None:
            print("Erro: Imagem não encontrada.")
        else:
            print("Imagem obtida com sucesso")
            return 2, image
    
    return None

def show_image_edit_options_menu(img):
    print("===========")
    print("Bem vindo ao menu de edição de imagem")
    print("Selecione que filtro você deseja aplicar na imagem")
    print("-----------")
    print("1 - GrayScale Filter")
    print("-----------")
    print("===========")
    valid_option = False
    while valid_option == False:
        option = int(input("Escolha sua opção (1, 2 ou 3) : "))
        if(option == 1 or option == 2 or option == 3):
            valid_option = True
        else:
            print("Opção Inválida")
    match option:
        case 1:
            imgOriginal, imgAltered = ImageFilters.grayscale_filter(img)
            cv.imshow('Imagem Original', imgOriginal)
            cv.imshow('Imagem Alterada',imgAltered)
            cv.waitKey(1000)
            cv.destroyAllWindows()
            
    return 1


def show_video_edit_menu():
    return None

def show_video_edit_options_menu():
    return None

def save_image_or_video():
    return None