#!/usr/bin/env python3
"""Compose light three-panel Chinese storyboard boards from graphite frames.

Spec format:
{
  "boards": [{
    "filename": "14_storyboard_segment_01_00-10.png",
    "title": "第一段｜00:00-00:10｜剧情功能",
    "subtitle": "3张草图分镜：动作A -> 动作B -> 反应C。",
    "images": [
      {"file": "02_cut01.png", "label": "动作A"},
      {"file": "03_cut02.png", "label": "动作B"},
      {"file": "04_cut03.png", "label": "反应C"}
    ],
    "action": "画面和表演说明。",
    "camera": "景别、运镜和节奏说明。",
    "dialogue": "角色：台词",
    "audio": "同期声和禁止项。",
    "summary": "豆包提示摘要。"
  }]
}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


WIDTH, HEIGHT = 2400, 1580
MARGIN = 54
BG = (247, 244, 237)
PANEL_BG = (238, 235, 227)
BOX_BG = (252, 250, 246)
FOOT_BG = (235, 232, 224)
TEXT = (35, 35, 35)
MUTED = (85, 85, 85)
ACCENT = (115, 67, 54)
GRID = (176, 166, 152)
PANEL_GRID = (75, 75, 75)


def find_font(bold: bool = False) -> str:
    regular = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    bold_candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    ]
    for item in (bold_candidates if bold else regular):
        if Path(item).exists():
            return item
    if bold:
        return find_font(False)
    raise SystemExit("No CJK font found. Install Microsoft YaHei, SimHei, PingFang, or Noto Sans CJK.")


FONT = find_font(False)
FONT_BOLD = find_font(True)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size=size)


def wrap_cjk(text: str, max_chars: int) -> list[str]:
    lines: list[str] = []
    for paragraph in str(text).splitlines() or [""]:
        while len(paragraph) > max_chars:
            lines.append(paragraph[:max_chars])
            paragraph = paragraph[max_chars:]
        lines.append(paragraph)
    return lines


def paste_panel(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    image_path: Path,
    box: tuple[int, int, int, int],
    label: str,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=14, fill=PANEL_BG, outline=PANEL_GRID, width=3)
    draw.text((x1 + 16, y1 + 10), label, fill=ACCENT, font=font(26, True))
    if not image_path.exists():
        raise SystemExit(f"Missing storyboard frame: {image_path}")
    image = Image.open(image_path).convert("RGB")
    fitted = ImageOps.fit(image, (x2 - x1 - 30, y2 - y1 - 64), method=Image.Resampling.LANCZOS)
    canvas.paste(fitted, (x1 + 15, y1 + 54))


def draw_text_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    heading: str,
    body: str,
    max_lines: int,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=14, fill=BOX_BG, outline=GRID, width=2)
    draw.text((x1 + 22, y1 + 18), heading, fill=ACCENT, font=font(31, True))
    y = y1 + 68
    lines = wrap_cjk(body, 38)
    if len(lines) > max_lines:
        raise SystemExit(f"Text overflow in {heading}: {len(lines)} lines, max {max_lines}")
    for line in lines:
        draw.text((x1 + 22, y), line, fill=TEXT, font=font(26))
        y += 38


def compose_board(board: dict[str, Any], image_dir: Path, out_dir: Path) -> Path:
    images = board.get("images", [])
    if not 1 <= len(images) <= 3:
        raise SystemExit("Each sketch board must contain 1-3 images; prefer 2-3.")

    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(canvas)

    draw.text((MARGIN, 36), board["title"], fill=TEXT, font=font(50, True))
    draw.text((MARGIN, 102), board["subtitle"], fill=MUTED, font=font(27))
    draw.line((MARGIN, 150, WIDTH - MARGIN, 150), fill=GRID, width=3)

    top, panel_h, gap = 185, 470, 28
    panel_w = (WIDTH - 2 * MARGIN - gap * (len(images) - 1)) // len(images)
    for index, item in enumerate(images):
        x1 = MARGIN + index * (panel_w + gap)
        paste_panel(
            canvas,
            draw,
            image_dir / item["file"],
            (x1, top, x1 + panel_w, top + panel_h),
            item["label"],
        )

    y = 700
    col_w = (WIDTH - 2 * MARGIN - 30) // 2
    draw_text_box(draw, (MARGIN, y, MARGIN + col_w, y + 270), "画面 / 动作", board["action"], 5)
    draw_text_box(draw, (MARGIN + col_w + 30, y, WIDTH - MARGIN, y + 270), "运镜 / 节奏", board["camera"], 5)
    draw_text_box(draw, (MARGIN, y + 305, MARGIN + col_w, y + 650), "台词", board["dialogue"], 8)
    draw_text_box(draw, (MARGIN + col_w + 30, y + 305, WIDTH - MARGIN, y + 650), "声音 / 禁止项", board["audio"], 8)

    footer_y = HEIGHT - 135
    draw.rounded_rectangle(
        (MARGIN, footer_y, WIDTH - MARGIN, HEIGHT - 46),
        radius=14,
        fill=FOOT_BG,
        outline=GRID,
        width=2,
    )
    draw.text((MARGIN + 22, footer_y + 20), "豆包提示摘要", fill=ACCENT, font=font(29, True))
    summary = wrap_cjk(board["summary"], 72)
    if len(summary) > 2:
        raise SystemExit("Summary is too long for the footer.")
    for index, line in enumerate(summary):
        draw.text((MARGIN + 245, footer_y + 22 + 34 * index), line, fill=TEXT, font=font(26))

    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / board["filename"]
    canvas.save(output, quality=95)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Compose light review-safe storyboard boards from graphite frames.")
    parser.add_argument("--spec", required=True, type=Path, help="JSON storyboard specification.")
    parser.add_argument("--image-dir", required=True, type=Path, help="Directory containing graphite frame PNGs.")
    parser.add_argument("--out-dir", required=True, type=Path, help="Output directory for board PNGs.")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    for board in spec["boards"]:
        print(compose_board(board, args.image_dir, args.out_dir))


if __name__ == "__main__":
    main()
