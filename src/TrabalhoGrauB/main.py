import Interface


def main():
    running = True
    while running:
        option = Interface.show_welcome_menu()

        if option == 1:
            image = Interface.show_image_edit_menu()
            if image is not None:
                Interface.show_image_edit_options_menu(image)
        elif option == 2:
            Interface.show_video_edit_options_menu()
        elif option == 3:
            running = False
    print("Aplicativo encerrado")


if __name__ == "__main__":
    main()
