# Doubao Generation Fallbacks

Use these fallbacks when a storyboard package is good for review but Doubao video generation fails.

## Prompt Tiers

For sensitive short-drama segments, write three versions:

1. **Full production prompt**: complete plot, dialogue, character continuity, style, and prohibitions.
2. **Softened prompt**: same visible beats, but neutral wording for complaints, food issues, enforcement, scams, insults, or humiliation.
3. **Ultra-short neutral action prompt**: only visible actions and continuity. Remove conflict explanation and sensitive claims.

The third version can be paired with the composed storyboard board image. This can work better than pairing the storyboard board with a long conflict-heavy prompt.

## Successful Pattern

When the long or softened prompt fails, try:

```text
如果仍然失败，使用这个更短版本

中国现实短剧，竖屏9:16，<地点>，真实生活质感，手持镜头。成年<主角>在<地点>做<动作1>；<时间2>，他/她做<动作2>；<时间3>，他/她做<动作3>。不要背景音乐，不要字幕，不要水印，不要旁白，不出现真实平台名称和真实品牌。
```

Example:

```text
中国现实短剧，竖屏9:16，出租屋餐桌旁，真实生活质感，手持镜头。成年男主角坐在餐桌旁查看手机里的虚构店铺页面，桌上有外卖餐盒和一次性筷子。0-3秒，他认真查看手机里的菜品图片；3-6秒，他滑到店铺环境图片，看见明亮整洁的小餐厅照片；6-10秒，他拿起外套和手机走向门口，低声说：“我去地址那边看一下。” 不要背景音乐，不要字幕，不要水印，不要旁白，不出现真实平台名称和真实品牌。
```

## Reference Image Guidance

- First try text only.
- If text only fails, try a single clean frame still from `assets/`.
- If a storyboard board is needed, pair it with the ultra-short neutral prompt, not the full prompt.
- Avoid asking the model to read small board text. Treat the board as visual composition guidance only.

## Wording Rules

Avoid these in generation prompts after failures:

- `诈骗`, `骗局`, `骗你下单`
- `讹`, `吃不起`, direct insults
- `监管执法`, real agency names
- graphic food-safety wording such as `异物`, `发黑`, `恶心`
- explicit claims like `AI生成的假图` when a neutral phrase can work

Prefer:

- `页面展示偏差`
- `现场核验`
- `页面图片和现实不一致`
- `包装碎屑`
- `合规工作人员`
- `尴尬停顿`
- `查看页面 -> 对比现场 -> 出门核对`
