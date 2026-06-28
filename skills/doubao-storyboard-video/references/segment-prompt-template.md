# Segment Prompt Template

Use this shape when writing each Doubao video prompt. Keep the prompt self-contained; do not rely on the previous segment being visible.

```text
【段落】<第几段｜时间码｜剧情功能>

<整体风格>。竖屏9:16。<镜头质感>。<声音要求>。

【硬性限制】
<逐条写清禁止项，例如：画面中不要出现孩子、学生、未成年人；不要出现真实学校名称、真实校徽、真实平台logo；不要字幕、不要水印、不要旁白。>

【人物一致性】
<角色1：年龄、发型、服装、气质、表演要求。>
<角色2：年龄、发型、服装、气质、表演要求。>
<必要时加入角色3。>

【场景】
<地点、桌面/背景道具、灯光、生活质感。>

【镜头】
镜头1，<时间>：<画面、动作、景别、运镜、对白、音效。>
镜头2，<时间>：<画面、动作、景别、运镜、对白、音效。>
镜头3，<时间>：<画面、动作、景别、运镜、对白、音效。>

【表演重点】
<本段最重要的情绪变化、冲突节奏、反转或结尾落点。>
```

Checklist:

- Every segment duration is at most 10 seconds.
- Dialogue is copied exactly from the source unless the user asks for rewriting.
- Each segment repeats character continuity and hard prohibitions.
- Any evidence shown on phones/tablets/screens describes only allowed objects or blurred records.
- Do not request subtitles if the source says no subtitles.
