# Doubao Storyboard Video

一个面向 Codex 的豆包 / Seedance 短剧制作 Skill。输入已经确认的短剧脚本，默认输出人脸审核更友好的石墨铅笔分镜、浅色三联故事板、人物参考图和逐段视频提示词。

## 能做什么

- 根据对白、动作和反应节奏拆分视频，每段不超过 10 秒。
- 为主要成年角色生成独立人物参考图。
- 为每段规划 2—3 个关键分镜，并生成不保留精确真人五官的黑白石墨草图。
- 将分镜自动排成浅色三联画中文故事板，避免把照片级人脸放进最终上传素材。
- 输出与故事板、人物和时间轴一致的豆包 / Seedance 视频提示词。
- 对冲突、投诉、食品、执法、欺诈和羞辱类题材提供完整、降敏、极简三档提示词。
- 检查人物一致性、台词遗漏、真实品牌、未成年人、字幕、水印和故事板文字溢出。

## 仓库结构

```text
doubao-storyboard-video/
├─ .codex-plugin/plugin.json
├─ skills/doubao-storyboard-video/
│  ├─ SKILL.md
│  ├─ agents/openai.yaml
│  ├─ assets/                         # 已验证的草图与版式参考
│  ├─ references/
│  └─ scripts/
│     ├─ compose_sketch_storyboard_boards.py
│     └─ compose_storyboard_boards.py
├─ docs/完整工作流规划.md
└─ requirements.txt
```

## 安装

克隆本仓库：

```bash
git clone https://github.com/roncyx726-debug/doubao-storyboard-video.git
```

然后把 `skills/doubao-storyboard-video` 整个目录复制到 Codex Skills 目录：

- Windows：`C:\Users\<用户名>\.codex\skills\doubao-storyboard-video`
- macOS / Linux：`~/.codex/skills/doubao-storyboard-video`

安装故事板合成脚本依赖：

```bash
python -m pip install -r requirements.txt
```

系统还需要一个中文字体，例如微软雅黑、黑体、苹方或 Noto Sans CJK。人物图与分镜图生成需要当前 Codex 环境提供图像生成能力。

## 使用方式

准备一份已经确认的剧本，然后在 Codex 中输入：

```text
使用 $doubao-storyboard-video，把这份剧本制作成豆包故事板包。

要求：
- 竖屏 9:16
- 每段不超过 10 秒
- 每段 2—3 张分镜
- 所有最终分镜使用黑白石墨铅笔草图，不使用照片级真人画面
- 每个主要角色单独生成人物参考图
- 保留原始对白
- 不要字幕、水印和真实品牌
- 输出到当前项目下的独立文件夹
```

建议同时提供：完整剧本、目标时长、画幅、视觉风格、禁止项和输出目录。

## 默认人物参考图

每个角色单独一张：左侧为写实彩色无脸全身形象，右侧为弱线条、低对比度的黑白脸部素描，只保留简单角色标签。若平台对肖像或年轻面孔较敏感，优先弱化或移除右侧脸部素描。

## 默认故事板风格

最终分镜参考仓库内置的已验证结果：暖白纸张、黑白石墨线条、明显交叉排线和手绘构造线。保留镜位、动作、服装轮廓和人物位置，但不保留精确真人身份、皮肤纹理、眼睛高光或照片景深。

默认故事板为 2400×1580 的浅色三联画：顶部 2—3 张草图，下方依次为画面动作、运镜节奏、完整台词、声音与禁止项，底部附豆包提示摘要。深色详细制作表格仅在用户明确要求时使用。

## 适用边界

这个 Skill 从“已经确定的脚本”开始工作，不负责搜索热点或决定选题。完整的热点选题到成片流程见 [完整工作流规划](docs/完整工作流规划.md)。

## 注意

- 热点事件应提炼情绪和冲突原型，不要包装成真实事件复刻。
- 平台规则会变化，敏感题材和人物参考图策略需要结合当前平台重新验证。
- 本仓库暂未附带开源许可证；未经许可，不代表自动获得复制、修改或再发布授权。
