# 04 · 工作流详解（Pipeline）

端到端命令与注意事项。变量：`$SKILL` = 技能目录；`$OUT` = 输出根目录。

## 阶段 1 · 采集与抽取
```
读 $sources_dir/*.md → 按"权威依据 / 操作规范 / 病友经验"三类摘录
```
- 指南/共识 → 权威依据（记出处：机构·期刊·年份·DOI）
- 护理要点 → 操作规范（转居家可执行条目）
- 病友案例 → 过来人经验（第一人称，处置类归口医护）

## 阶段 2 · 生成骨架
```bash
python "$SKILL/scripts/scaffold_whitepaper.py" --config config.json
```
产出：
- `$OUT/stage2/whitepaper.html` —— 完整风格化骨架（封面/前置三页/11章占位/术语表/附录A–G/页脚 + 风格 tokens + `{{INSERT_IMAGE_COVER_LOGO}}`/`{{INSERT_IMAGE_COMPARE}}`/`{{INSERT_IMAGE_COMMUNITY_LOGO}}` marker）
- `$OUT/stage2/finalize.json` —— 嵌图映射 + 输出路径（供阶段4读取）
- `$OUT/stage2/logo_mascot.png` —— 自技能资产复制

## 阶段 3a · 对比图（可选）
```bash
python "$SKILL/scripts/make_compare_diagram.py" --config cards.json --out "$OUT/stage2/compare.png"
```
`cards.json` 描述每种方案的卡片（名称/英文/主色/置入位置/留置时长/维护频率/外观/风险/适用/人体标记类型）。不提供则不放对比图（HTML 中删除该 marker 行即可）。

## 阶段 3b · HTML→DOCX
```bash
HTML_TO_DOCX_PY="$HOME/.venv-html-to-docx/bin/python"
CONV=$(ls -d "$HOME/.workbuddy/plugins/cache/workbuddy-builtin/tencent-docx/"*/skills/html-to-docx/scripts)
cd "$CONV"
"$HTML_TO_DOCX_PY" -m html_to_docx convert "$OUT/stage2/whitepaper.html" -o "$OUT/stage3/<target>.docx"
```
- 转换器**不会可靠内嵌 `<img>`**，因此封面/页脚/对比图统一用 `{{INSERT_IMAGE_xxx}}` 文本 marker，留作 finalize 阶段替换。
- 经验：转换器可能把 `{{X}}` 规范成 `{X}`，`finalize_docx.py` 已兼容两种形式（同时尝试 `{{X}}`/`{X}`/`X` 匹配）。

## 阶段 4 · 定稿与校验
```bash
python "$SKILL/scripts/finalize_docx.py" --json "$OUT/stage2/finalize.json"
```
动作：
1. 读取 finalize.json 的 `markers` 映射，把 docx 中的 `{{INSERT_IMAGE_x}}`（或 `{INSERT_IMAGE_x}`）文本替换为真实图片（指定 Cm 宽度、居中）。
2. 每个 H1 设 `page_break_before`（默认跳过**首个** H1＝封面标题，避免空白页；由 finalize.json 的 `skip_first_h1:true` 控制）。
3. 校验并打印：图片数、marker 残留数、章节数、分页数、关键字命中。

## 常见坑
- **重转会清空已嵌图**：每次 convert 都会新建 docx，必须重跑 finalize 嵌图。流程上 convert→finalize 成对执行。
- **提示框 content 丢失**：转换器会**丢弃 `data-component` 属性**，callout 必须用行内样式 `<div>` 承载内容，不可写 `data-component="callout"`。
- **marker 落在表格内**：若把 marker 放进表格单元格，finalize 同样扫描 table cell 文本并替换；但建议让 `{{INSERT_IMAGE_x}}` 单独成 `<p>` 最稳妥。
- **中文图字体**：PIL 必须用 Hiragino Sans GB.ttc；缺字体时图内中文变方块。
- **封面空白页**：务必让首个 H1（封面标题）跳过 `page_break_before`。
- **转换器偶发陈旧文本**：转后立刻读 docx 校验关键字，发现不符即重转。
- **空表格单元格变表单域**：转换器会把空单元格自动转成可填写字段（bookmark），对"记录表/审核页/交接单"是预期的可打印表单特性。
