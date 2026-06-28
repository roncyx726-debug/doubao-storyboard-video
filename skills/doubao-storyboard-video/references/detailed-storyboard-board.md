# Detailed Storyboard Board Format

Use this format by default for Doubao storyboard board images, especially Chinese realistic short dramas and any package that may be reviewed or approved by a platform/client.

## Board Structure

Use a horizontal board image with these columns:

- `镜头`
- `分镜图`
- `运镜流程 / 景别`
- `内容与对白`

Add a full-width strip under the cuts titled:

`制作设定 / 豆包分段提示`

The bottom strip should contain three blocks:

- `空间与人物位置`
- `灯光 / 色彩 / 道具`
- `风格 / 禁忌 / 分段提示词`

When composing an image board, include a simple blocking diagram in the space block and color swatches in the lighting/color/props block.

## Per-Cut Content

The `内容与对白` column must be detailed. Do not use a short plot summary only.

For each cut, write these labels in order:

```text
主体：<who/what is visually central>
动作：<specific physical action and blocking>
描述：<visual details reviewers must see on screen>
台词：<exact dialogue, preserving the source>
音效：<diegetic sound, room tone, phone sound, paper friction, etc.>
```

Keep the text compact enough to fit, but include the full production intent. If a line is too long, shorten descriptions before removing labels.

## Camera Column

The `运镜流程 / 景别` column should include:

- A clear shot label, optionally bilingual, such as `桌面中近景 / Desk MCU`, `证据特写 / Insert Shot`, `表情定格 / Freeze Close Up`.
- A visual movement cue when possible: camera icon, push arrow, lateral arrow, tilt arrow, or shake line.
- A short movement note, for example `从登记表推到家长面前`, `从手机门店图转到现实后门`, `快速推近定格老板僵脸`.

## Bottom Strip Details

`空间与人物位置`:
- Describe the physical location and the relative positions of all important characters and props.
- Include a simple diagram if producing an image board. Circles are enough for characters; rectangles are enough for desks, doors, phones, evidence, or props.

`灯光 / 色彩 / 道具`:
- List practical props required by the segment.
- Describe lighting and color temperature.
- Include 4-6 color swatches in the image board.

`风格 / 禁忌 / 分段提示词`:
- Repeat the core style, aspect ratio, camera texture, and hard prohibitions.
- Include a compact segment prompt summary, not just generic style notes.
- Carry forward banned items such as subtitles, watermarks, real platform logos, real brands, real school names, minors, gore, or background music whenever relevant.

## Quality Bar

A board is not complete if:

- `内容与对白` only summarizes the plot and does not include `主体 / 动作 / 描述 / 台词 / 音效`.
- The bottom strip lacks concrete space, prop, lighting, and negative-constraint information.
- The storyboard stills are present but the reviewer cannot infer what should happen in the generated video.
- The board omits exact dialogue that exists in the source script.
- Hard prohibitions appear only in the Markdown prompt but not on the board image.

Before final delivery, visually inspect all final board images when time allows. Check that text fits, cut images are not missing, and the bottom strip is readable.
