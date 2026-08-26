---
name: xyb-whitepaper-skills
description: 小胰宝(XYB)患者科普白皮书生成技能。基于指南/共识+病友经验，产出风格统一(配色/字体/logo/组件)的 DOCX 白皮书。稳定覆盖：封面→编者按→目录→前置三页(读者信/范围边界/红黄绿急症卡)→主题章节→术语表→附录(记录表/审核页/耗材/参考资料/出院交接单/复诊提问卡)→页脚；默认补齐 PTCD 白皮书完成度评估中的优先项(P0-1~P0-7、P2)。适用于任意肿瘤/慢病照护主题的科普白皮书生成。
version: 1.0.0
---

# xyb-whitepaper-skills · 小胰宝患者科普白皮书生成技能

把"小胰宝"已验证的两份白皮书（PTCD v0.15、血管通路 v0.2）的**框架、风格、质量门禁**沉淀为一个可复用、可适配、独立部署的技能。新主题只需提供"主题 + 资料源目录"，技能即可生成风格一致、结构完整、安全校准到位的白皮书骨架，再结合指南/共识/病友经验填充内容。

## 何时使用

- 用户要求"生成/做一份 XX 白皮书/科普手册/照护集"，且属于患者家属可读的照护类文档。
- 用户给定了指南/共识/案例资料目录，要求"梳理资料、提取关键内容、丰富白皮书"。
- 用户要求"统一风格/补齐前置页/工具包/安全校准/分页优化"。
- 触发词：白皮书、照护集、科普手册、患者手册、居家护理、指南共识汇编。

## 一、技能开发输入需求（由本技能定义，调用时向用户收集）

> 这部分是技能对外暴露的"必填/选填输入"。缺少必填项时，先向用户确认或给合理默认值并在产物中标注"待补"。

### 必填输入
| 项 | 键 | 说明 | 默认/兜底 |
|---|---|---|---|
| 主题名称 | `topic` | 如"PTCD 居家照护""血管通路(PICC/输液港)" | 无，必须提供 |
| 资料源目录 | `sources_dir` | 含指南解读/护理共识/病友案例的 `*.md` 集合 | 无，必须提供 |
| 输出根目录 | `output_dir` | 产物写入此目录（自动建 `stage2/` `stage3/`） | 当前工作目录下的 `output/<topic>_whitepaper_<date>` |
| 目标文件名 | `target_docx` | 最终 docx 名，默认从 topic 派生为 `{topic_slug}_output.docx`（如 `picc_output.docx`） | `{topic_slug}_output.docx` |

### 选填输入（不提供则用技能默认值）
| 项 | 键 | 默认 |
|---|---|---|
| 副标题 | `subtitle` | "<主题>家属全程照护手册" |
| 通俗名/专业名备注 | `acronym_note` | 空（如 PTCD 为通俗用语，专业称 PTBD） |
| 社区署名 | `community` | "小胰宝社区 · 天工开物基金会" |
| 主色(accent) | `accent` | `#5c4a7a`（紫） |
| 章节大纲 | `chapters` | 见 references/01_framework.md 的标准 11 章（可增减） |
| 对比图配置 | `diagram` | 见 scripts/make_compare_diagram.py；不提供则不放对比图 |
| 病友实证资源 | `patient_resources` | 留"待社区补充"占位 |
| 临床顾问署名 | `advisors` | 留"待合作医护团队审核"占位 |

### 内容源处理方式
- **指南/共识**：作为"权威依据"，引用时标注出处（期刊/机构/年份），列入附录 D 参考资料。
- **护理要点/共识**：作为"操作规范"，转化为可执行的居家观察/维护条目。
- **病友案例/经验**：作为"过来人经验"，以第一人称口吻写入，但涉及处置的必须加【安全提示·个体化医嘱】并归口医护。
- **凡涉及处置的操作**（冲管、回输、补液、拔/换管、出行评估）：一律不以"通用处方"呈现，只写"什么情况要找团队、怎么沟通"，详见 03_assessment_mapping.md。

## 二、工作流（4 阶段）

```
阶段1 采集与抽取   读 sources_dir 的 .md → 提取"权威依据/操作规范/病友经验"三类要点
        ↓
阶段2 HTML 骨架    scaffold_whitepaper.py 生成 stage2/whitepaper.html + finalize.json
                   （含封面/前置三页/标准章节占位/术语表/附录A–G/页脚 + 风格 tokens）
        ↓  agent 填充章节内容、对比图配置
阶段3 图像与转换    make_compare_diagram.py → stage2/compare.png（可选）
                   html_to_docx convert whitepaper.html -o stage3/<target_docx>
        ↓
阶段4 定稿与校验    finalize_docx.py（嵌图 marker + 每章分页 + 0 残留校验）
                   present_files 交付
```

### 命令模板
```bash
# 阶段2：生成骨架（输出 HTML + finalize.json，并拷贝 logo 到 stage2）
python "$SKILL/scripts/scaffold_whitepaper.py" --config config.json

# 阶段3a：生成对比图（可选，参数见脚本 --help）
python "$SKILL/scripts/make_compare_diagram.py" --config cards.json --out stage2/compare.png

# 阶段3b：HTML→DOCX（依赖 tencent-docx 技能内置转换器）
HTML_TO_DOCX_PY="$HOME/.venv-html-to-docx/bin/python"
cd "$HOME/.workbuddy/plugins/cache/workbuddy-builtin/tencent-docx/*/skills/html-to-docx/scripts/"
"$HTML_TO_DOCX_PY" -m html_to_docx convert <stage2/whitepaper.html> -o <stage3/target.docx>

# 阶段4：嵌图+分页+校验
python "$SKILL/scripts/finalize_docx.py" --json <stage2/finalize.json>
```

## 三、稳定框架要素（不可省略，除非主题确实不适用并注明）

1. **封面**：社区 logo + 标题 + 副标题 + "草稿·待医护审核" + 版本号 v0.1 起。
2. **编者按**：预期管理（"会读到/不会读到什么"）+ 怎么用这本子。
3. **目录**：与物理章节顺序一致（含前置三页与附录）。
4. **前置三页（P0-2）**：致读者信 / 范围与边界（负责/不负责对照表 + 统一安全边界）/ 30 秒红黄绿急症卡。各起新页。
5. **主题章节**：标准 11 章认知弧（详见 01_framework.md），按主题映射；可合并/跳过但需注明。
6. **术语快速查询表**：术语/缩写/定义/章节页码。
7. **附录 A 记录表（可打印）** / **B 医护审核页** / **C 耗材清单** / **D 参考资料与版本说明** / **F 出院交接单** / **G 复诊提问卡**（P0-7 工具包）。顺序 A→B→C→D→E(主题专附)→F→G→附件→术语。
8. **页脚**：分隔线 + 浅灰圆角社区卡片 + 社区 logo（或文本署名）。
9. **版本机制**：v0.x 草稿迭代；每次升版在附录 D 写变更说明。

## 四、统一风格（详见 02_style_guide.md，务必遵守）

- **主色**：`#5c4a7a`（紫），h1/h2 用同系深一档。
- **字体**：中文 Hiragino Sans GB（PIL/图用 index 1=粗/0=常规）；docx 由转换器套用默认中文字体。
- **组件**：提示框用**行内样式 `<div>`**（`style="background:#f7f4fb;border-left:4px solid <accent>;..."`）；⚠️ 本转换器会**丢弃 `data-component` 属性**，故不可用该属性承载内容。【安全提示·个体化医嘱】红色标识；表格用 `<table>` 含表头；急症卡三色（🔴🟡🟢）。
- **图片 marker**：所有图用文本占位 `{{INSERT_IMAGE_COVER_LOGO}}` / `{{INSERT_IMAGE_COMPARE}}` / `{{INSERT_IMAGE_COMMUNITY_LOGO}}`（**不要**用 `<img>`，转换器对 `<img>` 内嵌不可靠）。`finalize_docx.py` 在阶段4统一替换为真实图片（Cm：封面 3.2 / 对比图 15.5 / 页脚 6.0）。转换器可能把 `{{X}}` 规范成 `{X}`，finalize 已兼容两种形式。
- **空表格单元格**：转换器会自动转成**可填写表单域**（bookmark 字段），对"记录表/审核页/交接单"恰好是需要的打印可填表单，属预期特性。
- **分页**：每个 H1（除封面标题）`page_break_before=True`。

## 五、质量门禁（PTCD 评估 v1 优先级，默认补齐）

| 优先级 | 要素 | 技能内默认动作 |
|---|---|---|
| P0-1 | 标题统一 | 封面/正文/页脚统一称"白皮书"，注明通俗名↔专业名 |
| P0-2 | 前置三页 | scaffold 直接产出读者信/边界/急症卡 |
| P0-3 | 安全校准 | 处置类语句强制【安全提示·个体化医嘱】+ 范围与边界统一边界 |
| P0-5/6 | 内容合并 | 同源内容只录一处（正文引用+附录要点，附件完整版） |
| P0-7 | 工具包 | scaffold 直接产出出院交接单(F)+复诊提问卡(G) |
| P2 | 占位/分页/版本 | 清理"图片位置待补"类占位；强制分页；版本号管理 |

> P1（图像授权核验、资源出处核验、试读测试）与"公开版/审核版分离"属发布门槛，技能产出仍标记"草稿·待双专业审核"，不自行发布。

## 六、依赖与部署

- **运行时**：Python（需 `Pillow`、`python-docx`；转换器用 `$HOME/.venv-html-to-docx/bin/python`）。
- **转换器依赖**：`tencent-docx` 内置技能（提供 `html_to_docx` 模块）。技能自带 `finalize_docx.py` 会自动 glob 定位该转换器；若该技能未安装则给出明确报错。
- **自包含**：`assets/logo_mascot.png` 随技能分发；`scripts/`、`references/`、`assets/template.html` 均为相对引用，可整体拷贝部署。

## 七、产出检查清单（交付前自检）

- [ ] 封面/目录/正文/附录物理顺序与目录一致
- [ ] 前置三页存在且各起新页
- [ ] 附录 F/G 工具包存在
- [ ] 所有处置类语句有【安全提示·个体化医嘱】
- [ ] 0 个图片 marker 残留（`{{INSERT_IMAGE_xxx}}` / `{INSERT_IMAGE_xxx}` 均不可出现）、0 个"待补"占位（仅合法的"待社区补充"状态注可留）
- [ ] 图片数 = 封面logo + 对比图(可选) + 页脚logo；每章分页生效
- [ ] 指南/共识列入附录 D 并标注出处；病友经验已"归口医护"
- [ ] 版本号已升版并记录变更
