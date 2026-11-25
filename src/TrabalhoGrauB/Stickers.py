from __future__ import annotations

from pathlib import Path

import cv2 as cv
import numpy as np


STICKER_DIR = Path(__file__).resolve().parent / "stickers"


def _new_canvas(size: int = 180) -> np.ndarray:
    return np.zeros((size, size, 4), dtype=np.uint8)


def _save_default_stickers() -> list[tuple[str, str]]:
    """Gera cinco stickers PNG BGRA caso ainda não existam na pasta stickers."""
    STICKER_DIR.mkdir(parents=True, exist_ok=True)
    size = 180
    items: list[tuple[str, str]] = []

    # 1. Coração
    path = STICKER_DIR / "coracao.png"
    if not path.exists():
        image = _new_canvas(size)
        heart = np.array(
            [[90, 150], [22, 88], [20, 58], [35, 32], [60, 25], [90, 52],
             [120, 25], [145, 32], [160, 58], [158, 88]],
            dtype=np.int32,
        )
        cv.fillPoly(image, [heart], (45, 55, 245, 255), lineType=cv.LINE_AA)
        cv.polylines(image, [heart], True, (255, 255, 255, 255), 5, cv.LINE_AA)
        cv.imwrite(str(path), image)
    items.append(("Coração", str(path)))

    # 2. Estrela
    path = STICKER_DIR / "estrela.png"
    if not path.exists():
        image = _new_canvas(size)
        points = []
        center = (90, 90)
        for i in range(10):
            angle = -np.pi / 2 + i * np.pi / 5
            radius = 75 if i % 2 == 0 else 33
            points.append((int(center[0] + radius * np.cos(angle)), int(center[1] + radius * np.sin(angle))))
        polygon = np.array(points, dtype=np.int32)
        cv.fillPoly(image, [polygon], (0, 205, 255, 255), lineType=cv.LINE_AA)
        cv.polylines(image, [polygon], True, (255, 255, 255, 255), 5, cv.LINE_AA)
        cv.imwrite(str(path), image)
    items.append(("Estrela", str(path)))

    # 3. Carinha sorridente
    path = STICKER_DIR / "carinha.png"
    if not path.exists():
        image = _new_canvas(size)
        cv.circle(image, (90, 90), 75, (0, 220, 255, 255), -1, cv.LINE_AA)
        cv.circle(image, (90, 90), 75, (255, 255, 255, 255), 6, cv.LINE_AA)
        cv.circle(image, (63, 72), 8, (40, 40, 40, 255), -1, cv.LINE_AA)
        cv.circle(image, (117, 72), 8, (40, 40, 40, 255), -1, cv.LINE_AA)
        cv.ellipse(image, (90, 98), (38, 25), 0, 10, 170, (40, 40, 40, 255), 6, cv.LINE_AA)
        cv.imwrite(str(path), image)
    items.append(("Carinha", str(path)))

    # 4. Óculos
    path = STICKER_DIR / "oculos.png"
    if not path.exists():
        image = _new_canvas(size)
        cv.rectangle(image, (12, 57), (168, 70), (35, 35, 35, 255), -1, cv.LINE_AA)
        cv.ellipse(image, (52, 88), (38, 34), 0, 0, 360, (25, 25, 25, 255), -1, cv.LINE_AA)
        cv.ellipse(image, (128, 88), (38, 34), 0, 0, 360, (25, 25, 25, 255), -1, cv.LINE_AA)
        cv.ellipse(image, (52, 88), (32, 28), 0, 0, 360, (150, 90, 35, 255), 3, cv.LINE_AA)
        cv.ellipse(image, (128, 88), (32, 28), 0, 0, 360, (150, 90, 35, 255), 3, cv.LINE_AA)
        cv.imwrite(str(path), image)
    items.append(("Óculos", str(path)))

    # 5. Balão de fala
    path = STICKER_DIR / "balao.png"
    if not path.exists():
        image = _new_canvas(size)
        cv.rectangle(image, (15, 25), (165, 125), (245, 245, 245, 255), -1, cv.LINE_AA)
        cv.rectangle(image, (15, 25), (165, 125), (30, 30, 30, 255), 5, cv.LINE_AA)
        tail = np.array([[48, 123], [38, 155], [82, 123]], dtype=np.int32)
        cv.fillPoly(image, [tail], (245, 245, 245, 255), lineType=cv.LINE_AA)
        cv.polylines(image, [tail], True, (30, 30, 30, 255), 5, cv.LINE_AA)
        cv.line(image, (45, 65), (135, 65), (60, 60, 60, 255), 6, cv.LINE_AA)
        cv.line(image, (45, 90), (115, 90), (60, 60, 60, 255), 6, cv.LINE_AA)
        cv.imwrite(str(path), image)
    items.append(("Balão de fala", str(path)))

    return items


def get_available_stickers() -> list[tuple[str, str]]:
    defaults = _save_default_stickers()
    known_paths = {Path(path).resolve() for _, path in defaults}
    for path in sorted(STICKER_DIR.glob("*.png")):
        if path.resolve() not in known_paths:
            defaults.append((path.stem.replace("_", " ").title(), str(path)))
    return defaults


def load_sticker(sticker_path: str) -> np.ndarray:
    sticker = cv.imread(str(sticker_path), cv.IMREAD_UNCHANGED)
    if sticker is None:
        raise FileNotFoundError(f"Não foi possível abrir o sticker: {sticker_path}")
    if sticker.ndim == 2:
        sticker = cv.cvtColor(sticker, cv.COLOR_GRAY2BGRA)
    elif sticker.shape[2] == 3:
        alpha = np.full(sticker.shape[:2], 255, dtype=np.uint8)
        sticker = cv.merge((sticker[:, :, 0], sticker[:, :, 1], sticker[:, :, 2], alpha))
    elif sticker.shape[2] != 4:
        raise ValueError("O sticker precisa ter 3 canais (BGR) ou 4 canais (BGRA).")
    return sticker


def apply_sticker(
    background: np.ndarray, sticker_path: str, x: int, y: int, center: bool = True
) -> np.ndarray:
    if background is None or background.size == 0:
        raise ValueError("A imagem de fundo está vazia.")
    if background.ndim == 2:
        result = cv.cvtColor(background, cv.COLOR_GRAY2BGR)
    elif background.ndim == 3 and background.shape[2] == 4:
        result = cv.cvtColor(background, cv.COLOR_BGRA2BGR)
    else:
        result = background.copy()

    sticker = load_sticker(sticker_path)
    h_bg, w_bg = result.shape[:2]
    h_sticker, w_sticker = sticker.shape[:2]

    if center:
        left = int(x) - w_sticker // 2
        top = int(y) - h_sticker // 2
    else:
        left, top = int(x), int(y)

    right = left + w_sticker
    bottom = top + h_sticker

    x1, y1 = max(0, left), max(0, top)
    x2, y2 = min(w_bg, right), min(h_bg, bottom)
    if x1 >= x2 or y1 >= y2:
        return result

    sx1, sy1 = x1 - left, y1 - top
    sx2, sy2 = sx1 + (x2 - x1), sy1 + (y2 - y1)

    sticker_crop = sticker[sy1:sy2, sx1:sx2]
    foreground = sticker_crop[:, :, :3].astype(np.float32)
    alpha = sticker_crop[:, :, 3].astype(np.float32) / 255.0
    alpha = alpha[:, :, np.newaxis]

    roi = result[y1:y2, x1:x2].astype(np.float32)
    blended = roi * (1.0 - alpha) + foreground * alpha
    result[y1:y2, x1:x2] = np.clip(blended, 0, 255).astype(np.uint8)
    return result


class StickerEditor:

    def __init__(self, image: np.ndarray, stickers: list[tuple[str, str]]):
        if image is None or image.size == 0:
            raise ValueError("A imagem para edição está vazia.")
        self.original = image.copy()
        self.stickers = stickers
        self.active_index = 0
        self.placements: list[tuple[str, int, int]] = []

    @property
    def active_sticker(self) -> tuple[str, str]:
        return self.stickers[self.active_index]

    def select_sticker(self, index: int) -> None:
        if 0 <= index < len(self.stickers):
            self.active_index = index

    def place(self, x: int, y: int) -> None:
        self.placements.append((self.active_sticker[1], int(x), int(y)))

    def undo(self) -> None:
        if self.placements:
            self.placements.pop()

    def clear(self) -> None:
        self.placements.clear()

    def render(self) -> np.ndarray:
        result = self.original.copy()
        for path, x, y in self.placements:
            result = apply_sticker(result, path, x, y, center=True)
        return result


def mouse_callback(event: int, x: int, y: int, flags: int, param) -> None:
    if event == cv.EVENT_LBUTTONDOWN and isinstance(param, StickerEditor):
        param.place(x, y)
