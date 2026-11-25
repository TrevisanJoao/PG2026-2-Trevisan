from __future__ import annotations

from datetime import datetime
from pathlib import Path

import cv2 as cv

import ImageFilters
import Stickers


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _read_int(prompt: str, default: int, minimum: int, maximum: int) -> int:
    while True:
        value = input(prompt).strip()
        if value == "":
            return default
        try:
            number = int(value)
            if minimum <= number <= maximum:
                return number
        except ValueError:
            pass
        print(f"Digite um número entre {minimum} e {maximum}.")


def _read_float(prompt: str, default: float, minimum: float, maximum: float) -> float:
    while True:
        value = input(prompt).strip().replace(",", ".")
        if value == "":
            return default
        try:
            number = float(value)
            if minimum <= number <= maximum:
                return number
        except ValueError:
            pass
        print(f"Digite um valor entre {minimum} e {maximum}.")


def show_welcome_menu() -> int:
    print("\n========== EDITOR DE IMAGENS E VÍDEOS ==========")
    print("1 - Modo Foto")
    print("2 - Modo Vídeo (webcam)")
    print("3 - Sair")
    print("================================================")
    return _read_int("Escolha uma opção: ", 3, 1, 3)


def show_image_edit_menu():
    """Solicita o caminho e carrega uma imagem do disco."""
    while True:
        print("\n========== MODO FOTO ==========")
        print("Digite o caminho da imagem ou '0' para voltar ao menu inicial.")
        image_path = input("Caminho da imagem: ").strip().strip('"')
        if image_path == "0":
            return None
        image = cv.imread(image_path, cv.IMREAD_COLOR)
        if image is None:
            print("Erro: não foi possível abrir a imagem. Verifique o caminho e o formato.")
            continue
        print(f"Imagem carregada: {image.shape[1]} x {image.shape[0]} pixels.")
        return image


def _choose_filter() -> tuple[str, int] | None:
    print("\n========== FILTROS DISPONÍVEIS ==========")
    for index, key in enumerate(ImageFilters.FILTER_ORDER, start=1):
        info = ImageFilters.FILTERS[key]
        print(f"{index:2} - {info['name']}")
    print("0 - Voltar")
    choice = _read_int("Escolha o filtro: ", 0, 0, len(ImageFilters.FILTER_ORDER))
    if choice == 0:
        return None

    key = ImageFilters.FILTER_ORDER[choice - 1]
    info = ImageFilters.get_filter_info(key)
    print(f"\n{info['name']}")
    print(f"O que faz: {info['description']}")
    print(f"Parâmetros: {info['parameters']}")
    intensity = 3
    if "Nenhum" not in info["parameters"]:
        intensity = _read_int("Intensidade (1 a 15): ", 3, 1, 15)
    return key, intensity


def _choose_channel() -> str:
    print("\nCanal de aplicação:")
    print("A - Todos os canais (RGB/BGR)")
    print("R - Somente vermelho")
    print("G - Somente verde")
    print("B - Somente azul")
    while True:
        channel = input("Escolha o canal [A]: ").strip().upper() or "A"
        if channel in ("A", "R", "G", "B"):
            return "ALL" if channel == "A" else channel
        print("Opção inválida.")


def _apply_filter_menu(current_image):
    selected = _choose_filter()
    if selected is None:
        return current_image
    filter_key, intensity = selected
    channel = _choose_channel()
    try:
        result = ImageFilters.apply_filter_to_channel(
            current_image, filter_key, channel=channel, intensity=intensity
        )
        print("Filtro aplicado.")
        return result
    except ValueError as error:
        print(f"Não foi possível aplicar o filtro: {error}")
        return current_image


def _apply_arithmetic_menu(current_image):
    print("\n========== OPERAÇÕES ENTRE DUAS IMAGENS ==========")
    print("1 - Adição")
    print("2 - Subtração")
    print("3 - Blending (mistura ponderada)")
    print("0 - Voltar")
    operation = _read_int("Escolha a operação: ", 0, 0, 3)
    if operation == 0:
        return current_image

    second_path = input("Caminho da segunda imagem: ").strip().strip('"')
    second_image = cv.imread(second_path, cv.IMREAD_COLOR)
    if second_image is None:
        print("Erro: não foi possível carregar a segunda imagem.")
        return current_image

    if operation == 1:
        result = ImageFilters.add_images(current_image, second_image)
    elif operation == 2:
        result = ImageFilters.subtract_images(current_image, second_image)
    else:
        alpha = _read_float("Peso da imagem atual (0 a 1, padrão 0.5): ", 0.5, 0.0, 1.0)
        result = ImageFilters.blend_images(current_image, second_image, alpha)
    print("Operação concluída. Se necessário, a segunda imagem foi redimensionada para o tamanho da imagem atual.")
    return result


def _run_sticker_editor(current_image):
    stickers = Stickers.get_available_stickers()
    editor = Stickers.StickerEditor(current_image, stickers)
    window_name = "Modo Foto - Stickers"

    print("\n========== STICKERS ==========")
    for index, (name, _) in enumerate(stickers, start=1):
        print(f"{index} - {name}")
    print("Na janela da imagem:")
    print("  Clique com o botão esquerdo para posicionar o sticker ativo.")
    print("  Pressione 1-5 para selecionar um sticker")
    print("  U = desfazer | C = limpar stickers | ENTER ou Q = concluir")

    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    cv.setMouseCallback(window_name, Stickers.mouse_callback, editor)
    try:
        while True:
            preview = editor.render()
            name = editor.active_sticker[0]
            cv.putText(
                preview,
                f"Sticker: {name} | Clique para inserir | U desfaz | C Limpa | Q conclui",
                (10, 28), cv.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2, cv.LINE_AA,
            )
            cv.imshow(window_name, preview)
            key = cv.waitKey(30) & 0xFF
            if key in (ord("q"), ord("Q"), 13, 27):
                break
            elif key in (ord("u"), ord("U")):
                editor.undo()
            elif key in (ord("c"), ord("C")):
                editor.clear()
            elif ord("1") <= key <= ord("9"):
                editor.select_sticker(key - ord("1"))
    finally:
        cv.destroyWindow(window_name)
    print(f"{len(editor.placements)} sticker(s) inserido(s).")
    return editor.render()


def _default_output_path() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return OUTPUT_DIR / f"imagem_editada_{timestamp}.png"


def save_image_or_video(image=None) -> bool:
    """Salva a imagem atual ou um frame capturado do vídeo."""
    if image is None:
        print("Não há imagem/frame para salvar.")
        return False
    default_path = _default_output_path()
    print(f"\nCaminho sugerido: {default_path}")
    path_text = input("Caminho para salvar (ENTER usa o sugerido): ").strip().strip('"')
    output_path = Path(path_text) if path_text else default_path
    if output_path.suffix == "":
        output_path = output_path.with_suffix(".png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    success = cv.imwrite(str(output_path), image)
    if success:
        print(f"Imagem salva em: {output_path.resolve()}")
    else:
        print("Erro: não foi possível salvar a imagem. Tente usar PNG ou JPG.")
    return success


def show_image_edit_options_menu(img):
    """Menu de edição de foto. Os filtros podem ser aplicados em sequência."""
    original = img.copy()
    current = img.copy()
    window_name = "Modo Foto - Resultado"

    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    try:
        while True:
            cv.imshow(window_name, current)
            cv.waitKey(1)
            print("\n========== MENU DE EDIÇÃO DE FOTO ==========")
            print("1 - Aplicar filtro")
            print("2 - Operação matemática com outra imagem")
            print("3 - Adicionar/editar stickers")
            print("4 - Salvar imagem")
            print("5 - Resetar (voltar à imagem original)")
            print("6 - Exibir imagem original")
            print("0 - Voltar ao menu inicial")
            option = _read_int("Escolha uma opção: ", 0, 0, 6)

            if option == 0:
                break
            elif option == 1:
                current = _apply_filter_menu(current)
            elif option == 2:
                current = _apply_arithmetic_menu(current)
            elif option == 3:
                current = _run_sticker_editor(current)
            elif option == 4:
                save_image_or_video(current)
            elif option == 5:
                current = original.copy()
                print("Imagem restaurada ao estado original.")
            elif option == 6:
                cv.imshow("Imagem Original", original)
                cv.waitKey(1)
    finally:
        cv.destroyAllWindows()
    return current


def show_video_edit_menu():
    """Abre a webcam e devolve o objeto VideoCapture."""
    camera_index = _read_int("Índice da webcam [0]: ", 0, 0, 10)
    capture = cv.VideoCapture(camera_index)
    if not capture.isOpened():
        capture.release()
        print("Erro: não foi possível acessar a webcam. Verifique a câmera e as permissões.")
        return None
    return capture


def _print_video_help():
    print("\n========== CONTROLES DO MODO VÍDEO ==========")
    print("1-9: aplicar os filtros 1 a 9 da lista")
    print("0: aplicar o filtro 10 (Canny)")
    print("F: abrir a lista completa de filtros (inclui os filtros 11-14)")
    print("C: escolher o canal (todos, R, G ou B)")
    print("+ / -: aumentar ou diminuir a intensidade")
    print("R: resetar o vídeo para a imagem sem filtro")
    print("S: salvar o frame atual")
    print("H: mostrar esta ajuda")
    print("Q ou ESC: parar a webcam e voltar ao menu inicial")
    print("=============================================")


def show_video_edit_options_menu():
    """Aplica o filtro selecionado em tempo real a todos os frames da webcam."""
    capture = show_video_edit_menu()
    if capture is None:
        return

    active_filter = None
    channel = "ALL"
    intensity = 3
    window_name = "Modo Vídeo - Webcam"
    _print_video_help()

    try:
        while True:
            success, frame = capture.read()
            if not success:
                print("Não foi possível obter um frame da webcam.")
                break

            if active_filter is None:
                output = frame.copy()
                filter_label = "Sem filtro"
            else:
                try:
                    output = ImageFilters.apply_filter_to_channel(
                        frame, active_filter, channel=channel, intensity=intensity
                    )
                    filter_label = ImageFilters.FILTERS[active_filter]["name"]
                except Exception as error:
                    print(f"Erro ao aplicar filtro: {error}")
                    active_filter = None
                    output = frame.copy()
                    filter_label = "Sem filtro"

            status = f"{filter_label} | Canal: {channel} | Intensidade: {intensity}"
            cv.putText(output, status, (10, 28), cv.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2, cv.LINE_AA)
            cv.imshow(window_name, output)

            key = cv.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q"), 27):
                break
            elif key == ord("h") or key == ord("H"):
                _print_video_help()
            elif key in (ord("r"), ord("R")):
                active_filter = None
                channel = "ALL"
                intensity = 3
                print("Filtros e seleção de canal resetados.")
            elif key in (ord("s"), ord("S")):
                save_image_or_video(output)
            elif key in (ord("c"), ord("C")):
                channel = _choose_channel()
            elif key in (ord("+"), ord("=")):
                intensity = min(15, intensity + 1)
            elif key in (ord("-"), ord("_")):
                intensity = max(1, intensity - 1)
            elif key in (ord("f"), ord("F")):
                selected = _choose_filter()
                if selected is not None:
                    active_filter, intensity = selected
            elif ord("1") <= key <= ord("9"):
                active_filter = ImageFilters.FILTER_ORDER[key - ord("1")]
                intensity = 3
            elif key == ord("0"):
                active_filter = ImageFilters.FILTER_ORDER[9]
                intensity = 3
    finally:
        capture.release()
        cv.destroyAllWindows()
        print("Webcam encerrada.")
