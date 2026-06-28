# Review-Safe Sketch Storyboards

Use this reference whenever human faces appear in storyboard images intended for Doubao or Seedance upload.

## Default Frame Style

- 16:9 horizontal, full-bleed single frame.
- Black-and-white graphite pencil on slightly warm off-white paper.
- Visible construction lines, cross-hatching, and hand-drawn imperfections.
- Preserve blocking, gesture, prop placement, clothing silhouette, gaze, and dramatic beat.
- Render generic adult faces with approximate emotion only.
- Do not preserve exact identity, pores, skin texture, eye catchlights, precise anatomy, portrait likeness, celebrity likeness, or photographic depth-of-field.
- Do not treat grayscale or edge-filtered photography as a finished storyboard frame.

Use `../assets/graphite-storyboard-frame-reference.png` as the default style anchor.

## Image-Generation Prompt Shape

```text
Use case: style-transfer
Asset type: review-safe 16:9 storyboard frame for Doubao/Seedance
Input images: Image 1 is the content/composition reference when available. Image 2 is the bundled graphite style reference.
Primary request: redraw the scene as a hand-drawn black-and-white graphite pencil storyboard sketch matching the style reference's warm paper, loose construction lines, cross-hatching, and monochrome tonal hierarchy.
Preserve: camera angle, adult figure count and positions, gestures, props, clothing silhouettes, gaze directions, and dramatic beat.
Change: simplify every face into a generic adult sketch face with approximate expression only. Remove exact identity, pores, skin rendering, eye catchlights, precise likeness, portrait rendering, and photographic depth-of-field.
Composition: single full-bleed 16:9 horizontal frame, no collage.
Constraints: adults only; no minors; no text; no logos; no watermark; no color; no photorealism; no celebrity likeness.
```

When generating from text only, omit `Image 1` and describe the complete scene. Still attach the bundled style reference.

## Default Board Layout

Use `../assets/light-three-panel-board-reference.png` as the visual target and `../scripts/compose_sketch_storyboard_boards.py` for deterministic layout.

Required structure:

1. Large segment title and one-line three-beat subtitle.
2. Two or three large graphite panels across the top, each with a short action label.
3. `画面 / 动作` and `运镜 / 节奏` boxes.
4. `台词` and `声音 / 禁止项` boxes.
5. Bottom `豆包提示摘要` strip.

## JSON Schema

```json
{
  "boards": [
    {
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
      "summary": "供豆包使用的短摘要。"
    }
  ]
}
```

## Acceptance Checklist

- Every panel is visibly drawn, not photo-derived in appearance.
- Faces communicate only age range and emotion, not identity.
- No realistic skin, eyes, pores, bokeh, or camera grain remains.
- No minors, logos, watermarks, subtitles, or unintended readable UI.
- Two or three panels cover setup, reversal/action, and reaction/ending.
- Exact dialogue fits without clipping.
- The prohibition box states that the sketch is for composition only and concrete facial features must not be copied.
