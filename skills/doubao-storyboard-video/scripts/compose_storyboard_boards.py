#!/usr/bin/env python3
"""Compose Chinese storyboard board images from generated cut stills.

Spec format:
{
  "global": {
    "space": "空间与人物位置说明",
    "props": "灯光 / 色彩 / 道具说明",
    "style": "风格 / 禁忌说明",
    "palette": [[222,224,220], [43,47,48]]
  },
  "boards": [
    {
      "filename": "11_分镜故事板_第一段_00-09秒.png",
      "title": "第一段 00:00-00:09｜闯入与投诉",
      "segment_prompt": "本段豆包提示：...",
      "cuts": [
        {
          "num": "1",
          "time": "00:00-00:03",
          "duration": "3秒",
          "image": "03_cut01.png",
          "movement_title": "大全景 / Wide Shot",
          "movement_desc": "手持轻晃\\n快速跟拍",
          "movement_arrow": "push",
          "content": "主体：...\\n动作：...\\n台词：..."
        }
      ]
    }
  ]
}

movement_arrow values: push, lateral, tilt, shake, none.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


BG = (13, 17, 18)
GRID = (112, 118, 111)
TEXT = (232, 229, 220)
MUTED = (185, 181, 170)
ACCENT = (205, 184, 142)
RED = (167, 69, 62)

W = 1800
M = 18
COLS = [170, 850, 320, 424]
TITLE_H = 72
HEADER_H = 82
ROW_H = 390
BOTTOM_H = 450


def find_font() -> str:
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    for item in candidates:
        if Path(item).exists():
            return item
    raise SystemExit("No CJK font found. Install Microsoft YaHei, SimHei, SimSun, PingFang, or Noto Sans CJK.")


FONT_PATH = find_font()


def ft(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size=size)


F_TITLE = ft(42)
F_HEAD = ft(32)
F_SUB = ft(28)
F_BODY = ft(25)
F_SMALL = ft(22)
F_CONT = ft(20)
F_TINY = ft(19)


def column_edges() -> list[int]:
    x = [M]
    for col in COLS[:-1]:
        x.append(x[-1] + col)
    x.append(W - M)
    return x


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int] = TEXT,
    max_width: int = 380,
    line_gap: int = 7,
) -> int:
    x, y = xy
    lines: list[str] = []
    for para in str(text).split("\n"):
        if not para:
            lines.append("")
            continue
        line = ""
        for ch in para:
            test = line + ch
            if draw.textlength(test, font=font) <= max_width or not line:
                line = test
            else:
                lines.append(line)
                line = ch
        if line:
            lines.append(line)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def draw_center(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int] = TEXT,
    spacing: int = 8,
) -> None:
    x0, y0, x1, y1 = box
    lines = str(text).split("\n")
    total = len(lines) * font.size + (len(lines) - 1) * spacing
    y = y0 + (y1 - y0 - total) / 2
    for line in lines:
        width = draw.textlength(line, font=font)
        draw.text((x0 + (x1 - x0 - width) / 2, y), line, font=font, fill=fill)
        y += font.size + spacing


def fit_image(path: Path, size: tuple[int, int]) -> Image.Image:
    img = Image.open(path).convert("RGB")
    return ImageOps.fit(img, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def draw_camera_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1.0) -> None:
    w, h = int(70 * scale), int(42 * scale)
    draw.rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], outline=MUTED, width=2)
    draw.rectangle([cx - w // 2 + 12, cy - h // 2 - 12, cx - w // 2 + 36, cy - h // 2], outline=MUTED, width=2)
    draw.polygon([(cx + w // 2, cy - 14), (cx + w // 2 + 28, cy - 26), (cx + w // 2 + 28, cy + 26), (cx + w // 2, cy + 14)], outline=MUTED)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=MUTED, width=2)


def draw_arrow(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int] = MUTED) -> None:
    draw.line([x0, y0, x1, y1], fill=color, width=3)
    angle = math.atan2(y1 - y0, x1 - x0)
    for delta in [2.55, -2.55]:
        x2 = x1 + 16 * math.cos(angle + delta)
        y2 = y1 + 16 * math.sin(angle + delta)
        draw.line([x1, y1, x2, y2], fill=color, width=3)


def draw_movement(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], cut: dict[str, Any]) -> None:
    x0, y0, x1, y1 = box
    draw_center(draw, (x0 + 8, y0 + 22, x1 - 8, y0 + 128), cut.get("movement_title", ""), F_BODY)
    cx = (x0 + x1) // 2
    draw_camera_icon(draw, cx, y0 + 184, 0.85)
    arrow = cut.get("movement_arrow", "none")
    if arrow == "push":
        draw_arrow(draw, cx, y0 + 255, cx, y0 + 214)
    elif arrow == "lateral":
        draw_arrow(draw, x0 + 70, y0 + 240, x1 - 70, y0 + 240)
    elif arrow == "tilt":
        draw_arrow(draw, x0 + 96, y0 + 255, x1 - 85, y0 + 200)
    elif arrow == "shake":
        draw.line([x0 + 80, y0 + 242, x0 + 115, y0 + 224, x0 + 150, y0 + 252, x0 + 185, y0 + 228, x0 + 220, y0 + 245], fill=MUTED, width=3)
        draw.line([x1 - 80, y0 + 242, x1 - 115, y0 + 224, x1 - 150, y0 + 252, x1 - 185, y0 + 228, x1 - 220, y0 + 245], fill=MUTED, width=3)
    draw_center(draw, (x0 + 12, y0 + 270, x1 - 12, y1 - 18), cut.get("movement_desc", ""), F_SMALL, MUTED)


def draw_palette(draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[Any]) -> None:
    sw = 82
    for raw in colors[:6]:
        color = tuple(raw) if isinstance(raw, list) else raw
        draw.rectangle([x, y, x + sw, y + 58], fill=color, outline=GRID, width=2)
        x += sw + 10


def draw_blocking(draw: ImageDraw.ImageDraw, x0: int, btop: int) -> None:
    dx, dy = x0 + 300, btop + 292
    draw.rectangle([dx - 130, dy - 60, dx + 130, dy + 48], outline=GRID, width=2)
    draw.text((dx - 52, dy - 12), "办公桌", font=F_TINY, fill=MUTED)
    draw.ellipse([dx - 36, dy + 55, dx + 36, dy + 127], fill=(66, 104, 141), outline=GRID)
    draw.text((dx - 44, dy + 133), "老师", font=F_TINY, fill=TEXT)
    draw.ellipse([dx - 210, dy - 12, dx - 150, dy + 48], fill=(146, 74, 64), outline=GRID)
    draw.text((dx - 224, dy + 56), "角色A", font=F_TINY, fill=TEXT)
    draw.ellipse([dx + 150, dy - 12, dx + 210, dy + 48], fill=(72, 82, 82), outline=GRID)
    draw.text((dx + 132, dy + 56), "角色B", font=F_TINY, fill=TEXT)
    draw_arrow(draw, dx - 150, dy + 20, dx - 70, dy + 20, RED)


def compose_board(board: dict[str, Any], global_spec: dict[str, Any], image_dir: Path, out_dir: Path) -> Path:
    cuts = board["cuts"]
    h = M + TITLE_H + HEADER_H + ROW_H * len(cuts) + BOTTOM_H + M
    canvas = Image.new("RGB", (W, h), BG)
    draw = ImageDraw.Draw(canvas)
    x = column_edges()
    top_header = M + TITLE_H
    first_row = top_header + HEADER_H

    draw.rectangle([M, M, W - M, h - M], outline=GRID, width=2)
    draw.rectangle([M, M, W - M, top_header], fill=(14, 20, 22), outline=GRID, width=2)
    draw.text((M + 24, M + 14), board.get("title", ""), font=F_TITLE, fill=ACCENT)
    draw.rectangle([M, top_header, W - M, first_row], fill=(14, 20, 22), outline=GRID, width=2)
    for xline in x[1:-1]:
        draw.line([xline, top_header, xline, h - M], fill=GRID, width=2)
    for idx, label in enumerate(["镜头", "分镜图", "运镜流程 / 景别", "内容与对白"]):
        draw_center(draw, (x[idx], top_header, x[idx + 1], first_row), label, F_HEAD)

    y = first_row
    for cut in cuts:
        draw.line([M, y, W - M, y], fill=GRID, width=2)
        draw_center(draw, (x[0], y, x[1], y + ROW_H), f"Cut {cut.get('num', '')}\n{cut.get('time', '')}\n({cut.get('duration', '')})", F_SUB)
        img = fit_image(image_dir / cut["image"], (COLS[1] - 20, ROW_H - 20))
        canvas.paste(img, (x[1] + 10, y + 10))
        draw.rectangle([x[1] + 10, y + 10, x[2] - 10, y + ROW_H - 10], outline=(34, 39, 38), width=2)
        draw_movement(draw, (x[2], y, x[3], y + ROW_H), cut)
        draw_wrapped(draw, (x[3] + 22, y + 24), cut.get("content", ""), F_CONT, TEXT, max_width=COLS[3] - 44, line_gap=5)
        y += ROW_H

    draw.line([M, y, W - M, y], fill=GRID, width=2)
    btop = y
    draw.rectangle([M, btop, W - M, h - M], fill=(16, 21, 22), outline=GRID, width=2)
    draw.line([M, btop + 80, W - M, btop + 80], fill=GRID, width=2)
    draw.text((M + 24, btop + 24), "制作设定 / 豆包分段提示", font=F_HEAD, fill=ACCENT)
    bx = [M, M + 600, M + 1130, W - M]
    for xline in bx[1:-1]:
        draw.line([xline, btop + 80, xline, h - M], fill=GRID, width=2)

    draw.text((bx[0] + 24, btop + 100), "空间与人物位置", font=F_SUB, fill=TEXT)
    draw_wrapped(draw, (bx[0] + 24, btop + 150), global_spec.get("space", ""), F_SMALL, MUTED, max_width=540, line_gap=6)
    draw_blocking(draw, bx[0], btop)

    draw.text((bx[1] + 24, btop + 100), "灯光 / 色彩 / 道具", font=F_SUB, fill=TEXT)
    draw_wrapped(draw, (bx[1] + 24, btop + 150), global_spec.get("props", ""), F_SMALL, MUTED, max_width=480, line_gap=6)
    palette = global_spec.get("palette", [[222, 224, 220], [43, 47, 48], [176, 160, 135], [134, 55, 50], [80, 105, 113]])
    draw_palette(draw, bx[1] + 24, btop + 322, palette)

    draw.text((bx[2] + 24, btop + 100), "风格 / 禁忌 / 分段提示词", font=F_SUB, fill=TEXT)
    text = f"{global_spec.get('style', '')}\n\n{board.get('segment_prompt', '')}"
    draw_wrapped(draw, (bx[2] + 24, btop + 150), text, F_CONT, MUTED, max_width=590, line_gap=5)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / board["filename"]
    canvas.save(out_path, quality=95)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Compose Doubao-style Chinese storyboard boards from generated cut stills.")
    parser.add_argument("--spec", required=True, type=Path, help="Path to storyboard JSON spec.")
    parser.add_argument("--image-dir", required=True, type=Path, help="Directory containing cut still images referenced by the spec.")
    parser.add_argument("--out-dir", required=True, type=Path, help="Directory for final board PNG files.")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    global_spec = spec.get("global", {})
    for board in spec["boards"]:
        print(compose_board(board, global_spec, args.image_dir, args.out_dir))


if __name__ == "__main__":
    main()
