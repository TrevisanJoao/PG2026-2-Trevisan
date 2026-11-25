import numpy as np
import cv2 as cv

posicoes_stickers = []

def apply_sticker(fundo, sticker_path, x, y):
    sticker = cv.imread(sticker_path)
    h_fundo, w_fundo = fundo.shape[:2]
    h_sticker, w_sticker = sticker.shape[:2]

    if y + h_sticker > h_fundo or x + w_sticker > w_fundo:
            return fundo
    b, g, r, a = cv.split(sticker)
    sticker_bgr = cv.merge([b, g, r])

    alpha = a / 255.0
    alpha_3c = cv.merge([alpha, alpha, alpha])

    roi = fundo[y:y+h_sticker, x:x+w_sticker]

    fundo_suavizado = roi * (1 - alpha_3c)
    sticker_suavizado = sticker_bgr * alpha_3c

    resultado = cv.add(fundo_suavizado, sticker_suavizado).astype(np.uint8)

    fundo[y:y+h_sticker, x:x+w_sticker] = resultado
    return None

def mouse_callback(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        posicoes_stickers.append((x, y))
    return None

