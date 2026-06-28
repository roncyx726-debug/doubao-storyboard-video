---
name: doubao-storyboard-video
description: "Create Doubao-ready storyboard packages from a finished video prompt or script: split into ten-second-or-shorter segments, plan cuts, generate character reference sheets and storyboard frames, compose Chinese storyboard board images, and write matching segment prompts. Use when asked for 分镜故事板, 人物参考图, 豆包视频提示词, storyboards, or reusable video-generation packs."
---

# Doubao Storyboard Video

## Output Contract

Create a single output folder containing:

- Character reference images for recurring adult main characters. For realistic Seedance/Doubao short dramas, default to one image per role: left side realistic colored faceless full-body figure, right side black-and-white face sketch, with only a simple role label.
- Storyboard frame stills for each cut.
- One final storyboard board image per Doubao segment.
- A Markdown file with one complete video-generation prompt per segment.

Default to Doubao's maximum duration rule: every segment must be `<=10` seconds. If the source video is longer, split it into consecutive segments such as `00:00-00:09`, `00:09-00:17`, `00:17-00:25`.

For realistic short dramas, estimate duration from spoken dialogue plus action and reaction beats, not from written scene count. A 10-second segment usually works best with 2-3 storyboard frames on the board; one frame is often too sparse, and more than three frames is usually too dense. Split into more segments when dialogue needs breathing room.

## Workflow

1. Parse the source prompt or script.
   - Preserve exact dialogue.
   - Extract hard constraints, especially banned subjects, logos, subtitles, watermarks, music, and real names.
   - Identify adult characters, scene, props, tone, camera style, and total duration.

2. Split into Doubao segments.
   - Keep each segment at or below 10 seconds.
   - Keep dramatic units intact when possible: setup, escalation, reversal, ending.
   - Make segment titles useful for production, not decorative.
   - Estimate timing by reading dialogue aloud and adding room for actions, reactions, pauses, and evidence inserts.
   - Do not squeeze multiple long dialogue exchanges into one 8-10 second segment. Prefer more segments with fewer lines per segment.
   - Inside each segment prompt, make cut timings relative to that segment, starting at `00:00`, even when the segment title uses the full-film timecode.

3. Plan deliverables.
   - Create a dedicated output folder near the user's source materials or in the current workspace.
   - Use stable numbered filenames:
     - `01_角色名_人物参考图.png`
     - `03_cut01_镜头摘要.png`
     - `11_分镜故事板_第一段_00-09秒.png`
     - `14_三段豆包视频提示词.md`
   - Adjust numbering for more or fewer characters, cuts, or boards.

4. Generate image assets with the `imagegen` skill.
   - Use one image-generation call per distinct character reference sheet or frame still.
   - For realistic Seedance/Doubao short-drama role references: generate one separate image per role. Use a two-half layout: left side realistic colored faceless full-body figure; right side black-and-white face sketch; add only the role name as a simple label.
   - For young adult characters or review-sensitive face references, make the right-side face sketch visibly sketch-like: lower contrast, weaker line weight, less portrait-like detail. Keep the colored faceless full-body side unchanged.
   - If a platform rejects a role reference for portrait or likeness protection, first weaken, blur, or lighten the face-sketch half; if needed, use only the colored faceless full-body figure and describe the face in text.
   - If the user explicitly requests a turnaround instead of the default role-reference layout, ask for exactly three full-body views of the same adult character: front, side, back.
   - For cut stills: generate 16:9 horizontal storyboard references even if the final video is 9:16; include the final video ratio inside the segment prompts.
   - Repeat critical prohibitions in every prompt, for example no minors, no real logos, no readable school names, no subtitles, no watermark.
   - If the user provided example storyboards, treat them as layout/style references, not edit targets, unless explicitly asked.
   - Copy final generated images into the output folder; do not leave project-bound assets only under `$CODEX_HOME/generated_images`.

5. Compose final storyboard boards.
   - Prefer `scripts/compose_storyboard_boards.py` for deterministic Chinese table layout.
   - For each `<=10` second Doubao segment, include 2-3 storyboard frames when the segment has more than one action, reaction, or evidence beat. Use one frame only for very simple beats; avoid more than three frames unless the board remains readable.
   - The board should have these columns: `镜头`, `分镜图`, `运镜流程 / 景别`, `内容与对白`.
   - Use the detailed approval-oriented board format by default for short dramas and any user-facing storyboard package. See `references/detailed-storyboard-board.md`.
   - In the `内容与对白` column, do not write a short summary only. For every cut, include `主体`, `动作`, `描述`, `台词`, and `音效` so reviewers can understand exactly what is on screen and what happens.
   - In the `运镜流程 / 景别` column, include a bilingual or clear shot label, a camera icon/arrow when composing visually, and a short movement note such as `从证据转到表情` or `从手机页面扫到现实后门`.
   - Add a bottom production strip titled `制作设定 / 豆包分段提示` with three blocks: `空间与人物位置`, `灯光 / 色彩 / 道具`, and `风格 / 禁忌 / 分段提示词`.
   - Include a simple space/blocking diagram and color swatches in the bottom strip when the board is an image, especially for realistic short dramas.
   - If the bundled script cannot fit the detailed layout cleanly, create a custom composer for that package, but keep the same information architecture.

6. Write segment prompts.
   - Use `references/segment-prompt-template.md` as the shape.
   - Use `references/doubao-generation-fallbacks.md` when a segment may fail generation or has already failed in Doubao.
   - Each prompt must be independently usable in Doubao: include style, aspect ratio, scene, character continuity, cuts, dialogue, audio, and prohibitions.
   - Before the video prompt body, list the role reference images used in that segment, for example `角色参考图：考生参考：assets/...；妈妈参考：assets/...`.
   - Keep each prompt aligned to its storyboard board and exact segment timing.
   - Use segment-relative cut timings that start at `00:00`; keep the full-film timecode only in the segment heading.
   - Also create generation-compatible fallback prompts when the story contains conflict, complaints, food issues, enforcement, scams, insults, or other review-sensitive material. Preserve the plot function, but soften loaded wording and avoid terms that can cause video generation failure.
   - For sensitive segments, provide three prompt tiers: full production prompt, softened prompt, and ultra-short neutral action prompt. The ultra-short version should be safe to pair with a storyboard reference image.
   - For video generation, default to text-only or clean single-frame stills first. If that fails, try the ultra-short neutral prompt together with the storyboard board image as visual guidance; avoid pairing a dense storyboard board with a long conflict-heavy prompt.

7. Validate before final response.
   - Confirm every segment is `<=10` seconds.
   - Confirm the output folder contains all promised files.
   - Inspect at least one final storyboard board visually with `view_image`; inspect all boards if time or layout risk is high.
   - Check for common failures: text overflowing, missing cut images, accidental minors, real logos/school names, readable fake UI text where none was requested, inconsistent role names, or missing dialogue.

## Compose Script

Resolve the bundled script relative to this `SKILL.md`, then run it like this:

```powershell
python "<skill-directory>/scripts/compose_storyboard_boards.py" `
  --spec "<project-directory>/storyboard_spec.json" `
  --image-dir "<project-directory>/assets" `
  --out-dir "<project-directory>/boards"
```

The JSON spec format is documented in the script help:

```powershell
python "<skill-directory>/scripts/compose_storyboard_boards.py" --help
```

The composer requires Python 3, Pillow, and an installed CJK font such as Microsoft YaHei, SimHei, PingFang, or Noto Sans CJK.

## Prompt Notes

For sensitive source scripts, carry constraints forward aggressively. A prohibition only stated once in the source prompt should still appear in every image-generation prompt and every Doubao segment prompt if violating it would break the project.

For real-life short dramas, prefer:

- Realistic office or home texture over glossy cinematic exaggeration.
- Handheld camera language when the source calls for realism.
- Cold/warm lighting notes tied to the actual scene.
- Direct behavioral acting notes: who pressures, who restrains, who reverses the scene.
- Review-tested role reference style over overly realistic portrait references: separate role images, colored faceless full-body on the left, softened face sketch on the right, role label only.

Do not invent extra characters, brands, students, school names, or platform UI unless the user asked for them.

## Generation Compatibility Notes

Before handing prompts to Doubao or another video generator, make a final compatibility pass:

- If using Seedance/Doubao with uploaded role references, avoid highly realistic young face references. If a later segment fails while earlier segments pass, test by removing the young-character face reference first, then weakening the face sketch, then using full-body-only reference plus text description.

- Replace direct accusation or insult words with neutral action descriptions when possible. Examples: use `页面展示偏差`, `现场核验`, `合规沟通`, `尴尬停顿` instead of harsher fraud, humiliation, or abuse framing.
- For food-related stories, avoid disgusting or unsafe close-up language. Use `包装碎屑`, `焦糊碎屑`, `卖相差距` instead of graphic contamination wording unless the user explicitly needs a non-generation script.
- Avoid real-world enforcement framing unless necessary. Use `合规工作人员` or `现场工作人员` instead of real agency names, and keep the behavior calm.
- Keep exact dramatic beats, but remove unnecessary provocation from dialogue if generation fails.
- If a generation attempt fails, use this ladder:
  1. Softened text-only segment prompt.
  2. Softened prompt with one clean cut still from `assets/`.
  3. Ultra-short neutral action prompt, optionally with the composed storyboard board as visual guidance.
- Do not pair a text-heavy storyboard board with a long conflict-heavy prompt. This combination is more likely to fail than the board itself.
- If a segment fails twice, create an ultra-safe neutral action prompt for that segment. Remove accusation, complaint, customer-service confrontation, platform review, enforcement, scam/fraud framing, "AI-generated" claims, humiliation, and insults. Preserve only visible actions and continuity, for example `查看页面图片 -> 对比现场 -> 出门核对地址`.
- When using a storyboard board after failures, keep the text prompt very short and neutral, such as `参考故事板，生成这一段现实短剧视频：成人男主查看手机页面、对比桌上餐盒、拿外套出门核对地址。不要字幕、水印、旁白、真实平台和真实品牌。`
- If the ultra-short prompt generates video but loses dialogue, add back only 1-3 neutral spoken lines. Keep the lines short, practical, and non-accusatory, such as `地址显示是在这儿？`, `你平时从这里取餐吗？`, `我只想确认实际情况。` Avoid adding back long arguments or judgment-heavy lines.
- If softened prompts feel too flat, restore conflict through performance and pacing instead of sensitive claims. Use quick interruptions, short neutral challenges, silence, eye contact, stepping closer, phone evidence held in frame, and contrast cuts. Example lines: `这差得也太多了吧？`, `那我去地址那边看一下。`, `那页面上的店在哪？`, `页面信息和现场情况，需要对应一下。`
