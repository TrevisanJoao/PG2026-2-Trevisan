from __future__ import annotations

import cv2 as cv
import numpy as np


def _check_image(img: np.ndarray) -> np.ndarray:
    """Check if the image provided exists and is not empty"""
    if img is None or not isinstance(img, np.ndarray) or img.size == 0:
        raise ValueError("A imagem recebida está vazia ou é inválida.")
    return img


def _as_bgr(img: np.ndarray) -> np.ndarray:
    img = _check_image(img)
    if img.ndim == 2:
        return cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    if img.ndim == 3 and img.shape[2] == 4:
        return cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    if img.ndim == 3 and img.shape[2] == 3:
        return img.copy()
    raise ValueError("Formato de imagem não suportado. Use grayscale, BGR ou BGRA.")


def _odd_kernel(intensity: int, minimum: int = 3, maximum: int = 31) -> int:
    """Increases or lower the intensity of the filter applied"""
    intensity = max(1, min(15, int(intensity)))
    size = max(minimum, intensity * 2 + 1)
    return min(size, maximum if maximum % 2 else maximum - 1)


# =================================================================
# Filtros
# =================================================================

def grayscale_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Turns the image gray by taking away the color but preserving the light"""
    img = _check_image(img)
    if img.ndim == 2:
        gray = img
    elif img.shape[2] == 4:
        gray = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
    else:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return cv.cvtColor(gray, cv.COLOR_GRAY2BGR)


def gaussian_blur(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Aplies Gaussiano filter"""
    img = _check_image(img)
    kernel = _odd_kernel(intensity)
    return cv.GaussianBlur(img, (kernel, kernel), 0)


def median_blur(img: np.ndarray, intensity: int = 2) -> np.ndarray:
    """Reduces noise"""
    img = _check_image(img)
    kernel = _odd_kernel(intensity, maximum=15)
    return cv.medianBlur(img, kernel)


def bilateral_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Smooth the edges"""
    img = _check_image(img)
    intensity = max(1, min(15, int(intensity)))
    diameter = intensity * 2 + 1
    sigma = 20 + intensity * 10
    return cv.bilateralFilter(img, diameter, sigma, sigma)


def sharpening_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Enhances edges and fine details"""
    img = _check_image(img)
    intensity = max(1, min(10, int(intensity)))
    blurred = cv.GaussianBlur(img, (0, 0), 1.0)
    amount = 0.35 + (intensity * 0.15)
    return cv.addWeighted(img, 1.0 + amount, blurred, -amount, 0)


def laplacian_enhancement_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Perform transitions and contouring using the Laplacian operator"""
    img = _check_image(img)
    intensity = max(1, min(10, int(intensity)))
    laplacian = cv.Laplacian(img, cv.CV_16S, ksize=3)
    edges = cv.convertScaleAbs(laplacian)
    return cv.addWeighted(img, 1.0, edges, 0.15 * intensity, 0)


def negative_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Invert the color and intensity of the pixels"""
    img = _check_image(img)
    return cv.bitwise_not(img)


def sepia_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Makes the image look old"""
    img = _as_bgr(img).astype(np.float32)
    matrix = np.array(
        [[0.131, 0.534, 0.272],
         [0.168, 0.686, 0.349],
         [0.189, 0.769, 0.393]],
        dtype=np.float32,
    )
    result = cv.transform(img, matrix)
    return np.clip(result, 0, 255).astype(np.uint8)


def thresholding_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Makes the image exclusively black or white"""
    img = _check_image(img)
    intensity = max(1, min(10, int(intensity)))
    threshold = 40 + intensity * 15
    if img.ndim == 2:
        gray = img
    else:
        gray = cv.cvtColor(_as_bgr(img), cv.COLOR_BGR2GRAY)
    _, result = cv.threshold(gray, threshold, 255, cv.THRESH_BINARY)
    return cv.cvtColor(result, cv.COLOR_GRAY2BGR)


def canny_edge_detection_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Detects edges and marks them. Everything else turns black"""
    img = _check_image(img)
    intensity = max(1, min(10, int(intensity)))
    if img.ndim == 2:
        gray = img
    else:
        gray = cv.cvtColor(_as_bgr(img), cv.COLOR_BGR2GRAY)
    lower = 20 + intensity * 10
    upper = min(255, lower * 3)
    edges = cv.Canny(gray, lower, upper)
    return cv.cvtColor(edges, cv.COLOR_GRAY2BGR)


def cartoon_effect(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Makes the image look like a cartoon"""
    color = _as_bgr(img)
    intensity = max(1, min(10, int(intensity)))
    smooth = cv.bilateralFilter(color, 9, 30 + intensity * 12, 30 + intensity * 12)
    gray = cv.cvtColor(color, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5)
    edges = cv.adaptiveThreshold(
        gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 5 + intensity
    )
    return cv.bitwise_and(smooth, smooth, mask=edges)


def emboss_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Makes the image look like a sculpture"""
    img = _check_image(img)
    kernel = np.array(
        [[-2, -1, 0], [-1, 1, 1], [0, 1, 2]], dtype=np.float32
    )
    result = cv.filter2D(img, -1, kernel)
    return cv.convertScaleAbs(result, alpha=1.0, beta=128)


def brightness_contrast_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Increases brightness and contrast"""
    img = _check_image(img)
    intensity = max(1, min(10, int(intensity)))
    alpha = 1.0 + (intensity * 0.08)
    beta = intensity * 3
    return cv.convertScaleAbs(img, alpha=alpha, beta=beta)


def sobel_edge_filter(img: np.ndarray, intensity: int = 3) -> np.ndarray:
    """Enhances edges """
    img = _check_image(img)
    if img.ndim == 2:
        gray = img
    else:
        gray = cv.cvtColor(_as_bgr(img), cv.COLOR_BGR2GRAY)
    scale = max(1, min(10, int(intensity))) / 3.0
    grad_x = cv.Sobel(gray, cv.CV_16S, 1, 0, ksize=3)
    grad_y = cv.Sobel(gray, cv.CV_16S, 0, 1, ksize=3)
    abs_x = cv.convertScaleAbs(grad_x, alpha=scale)
    abs_y = cv.convertScaleAbs(grad_y, alpha=scale)
    result = cv.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    return cv.cvtColor(result, cv.COLOR_GRAY2BGR)


FILTERS = {
    "grayscale": {
        "name": "Escala de cinza",
        "description": "Remove as cores e preserva a luminosidade da imagem.",
        "parameters": "Nenhum.",
        "function": grayscale_filter,
    },
    "gaussian": {
        "name": "Desfoque Gaussiano",
        "description": "Suaviza a imagem e reduz ruídos; detalhes pequenos ficam menos nítidos.",
        "parameters": "Intensidade de 1 a 15; valores maiores aumentam o desfoque.",
        "function": gaussian_blur,
    },
    "median": {
        "name": "Filtro de mediana",
        "description": "Reduz principalmente ruído do tipo sal e pimenta, preservando algumas bordas.",
        "parameters": "Intensidade de 1 a 7; valores maiores usam uma vizinhança maior.",
        "function": median_blur,
    },
    "bilateral": {
        "name": "Filtro bilateral",
        "description": "Suaviza regiões homogêneas sem borrar tanto as bordas.",
        "parameters": "Intensidade de 1 a 15.",
        "function": bilateral_filter,
    },
    "sharpen": {
        "name": "Sharpen / Realce de nitidez",
        "description": "Aumenta a percepção de nitidez e realça detalhes locais.",
        "parameters": "Intensidade de 1 a 10.",
        "function": sharpening_filter,
    },
    "laplacian": {
        "name": "Realce Laplaciano",
        "description": "Realça transições rápidas de intensidade e contornos da imagem.",
        "parameters": "Intensidade de 1 a 10.",
        "function": laplacian_enhancement_filter,
    },
    "negative": {
        "name": "Negativo",
        "description": "Inverte os valores de intensidade dos canais de cor.",
        "parameters": "Nenhum.",
        "function": negative_filter,
    },
    "sepia": {
        "name": "Sépia",
        "description": "Aplica uma coloração marrom/amarelada semelhante a fotos antigas.",
        "parameters": "Nenhum.",
        "function": sepia_filter,
    },
    "threshold": {
        "name": "Limiarização (Thresholding)",
        "description": "Transforma a imagem em pixels pretos ou brancos conforme um limiar.",
        "parameters": "Intensidade de 1 a 10; altera o limiar entre tons escuros e claros.",
        "function": thresholding_filter,
    },
    "canny": {
        "name": "Detecção de bordas Canny",
        "description": "Mostra principalmente as bordas detectadas na imagem.",
        "parameters": "Intensidade de 1 a 10; controla os limiares de detecção.",
        "function": canny_edge_detection_filter,
    },
    "cartoon": {
        "name": "Efeito desenho animado",
        "description": "Combina suavização de cores com detecção de contornos.",
        "parameters": "Intensidade de 1 a 10.",
        "function": cartoon_effect,
    },
    "emboss": {
        "name": "Relevo (Emboss)",
        "description": "Cria a impressão de relevo, como se os elementos estivessem gravados.",
        "parameters": "Nenhum.",
        "function": emboss_filter,
    },
    "brightness": {
        "name": "Brilho e contraste",
        "description": "Aumenta o brilho e o contraste da imagem.",
        "parameters": "Intensidade de 1 a 10.",
        "function": brightness_contrast_filter,
    },
    "sobel": {
        "name": "Detecção de bordas Sobel",
        "description": "Calcula gradientes horizontais e verticais para realçar bordas.",
        "parameters": "Intensidade de 1 a 10.",
        "function": sobel_edge_filter,
    },
}

FILTER_ORDER = list(FILTERS.keys())


def get_filter_info(filter_key: str) -> dict:
    if filter_key not in FILTERS:
        raise ValueError(f"Filtro desconhecido: {filter_key}")
    return FILTERS[filter_key]


def apply_filter(img: np.ndarray, filter_key: str, intensity: int = 3) -> np.ndarray:
    """Aplica um dos filtros registrados em FILTERS."""
    if filter_key not in FILTERS:
        raise ValueError(f"Filtro desconhecido: {filter_key}")
    _check_image(img)
    return FILTERS[filter_key]["function"](img.copy(), intensity)


def apply_filter_to_channel(
    img: np.ndarray, filter_key: str, channel: str = "ALL", intensity: int = 3
) -> np.ndarray:
    """Aplica o filtro na imagem inteira ou somente em B, G ou R"""
    img = _check_image(img)
    channel = channel.upper()
    if channel in ("ALL", "TODOS", "RGB"):
        return apply_filter(img, filter_key, intensity)

    channel_indices = {"B": 0, "G": 1, "R": 2}
    if channel not in channel_indices:
        raise ValueError("Canal inválido. Escolha ALL, B, G ou R.")

    if img.ndim == 2:
        raise ValueError("A imagem atual está em escala de cinza e não possui canais RGB separados.")
    if img.shape[2] == 4:
        source = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    else:
        source = img

    index = channel_indices[channel]
    filtered = apply_filter(source[:, :, index], filter_key, intensity)
    if filtered.ndim == 3:
        if filtered.shape[2] == 3:
            filtered = cv.cvtColor(filtered, cv.COLOR_BGR2GRAY)
        elif filtered.shape[2] == 4:
            filtered = cv.cvtColor(filtered, cv.COLOR_BGRA2GRAY)
    output = np.zeros_like(source)
    output[:, :, index] = filtered
    return output


# =================================================================-
# Operações aritméticas entre duas imagens
# =================================================================

def _prepare_image_pair(image_a: np.ndarray, image_b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    image_a = _as_bgr(image_a)
    image_b = _as_bgr(image_b)
    if image_a.shape[:2] != image_b.shape[:2]:
        image_b = cv.resize(image_b, (image_a.shape[1], image_a.shape[0]), interpolation=cv.INTER_AREA)
    return image_a, image_b


def add_images(image_a: np.ndarray, image_b: np.ndarray) -> np.ndarray:
    """Add two images, saturating values above 255"""
    a, b = _prepare_image_pair(image_a, image_b)
    return cv.add(a, b)


def subtract_images(image_a: np.ndarray, image_b: np.ndarray) -> np.ndarray:
    """Subtract image_b from image_a; negative results are limited to zero"""
    a, b = _prepare_image_pair(image_a, image_b)
    return cv.subtract(a, b)


def blend_images(image_a: np.ndarray, image_b: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    """Combina duas imagens: A * alpha + B * (1 - alpha)."""
    a, b = _prepare_image_pair(image_a, image_b)
    alpha = max(0.0, min(1.0, float(alpha)))
    return cv.addWeighted(a, alpha, b, 1.0 - alpha, 0)
