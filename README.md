# xyb-whitepaper-writer

> 小胰宝（XYB）患者科普白皮书生成技能 —— 基于指南/共识 + 病友经验，产出风格统一的 DOCX 白皮书。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/WorkBuddy-Skill-%235c4a7a)](https://www.workbuddy.cn)

## 简介

`xyb-whitepaper-writer` 是一个面向 WorkBuddy 的 AI 技能（Skill），把**小胰宝社区**已验证的两份白皮书（PTCD 居家照护 v0.15、血管通路 v0.3）的框架、风格、质量门禁沉淀为可复用、可适配的流水线。新主题只需提供「主题 + 资料源目录」，即可生成：

- 封面（社区 logo + 标题 + 版本号）
- 编者按 + 目录
- 前置三页（致读者信 / 范围与边界 / 30 秒红黄绿急症卡）
- 按主题映射的标准章节（认知弧：基础认知 → 术前 → 术后 → 日常维护 → 异常识别 → 急症应急 → 心理支持 → 医疗资源）
- 术语快速查询表
- 可打印工具包（维护记录表 / 医护审核页 / 耗材清单 / 出院交接单 / 复诊提问卡）
- 参考资料与版本说明
- 页脚（社区署名 + logo）

## 目录结构

```
xyb-whitepaper-writer/
├── SKILL.md                    # 技能入口（用途、触发、输入、流水线、质量门禁）
├── README.md                   # 本文件
├── assets/
│   ├── logo_mascot.png         # 小胰宝社区吉祥物 logo（自包含）
│   └── template.html           # 参考用 HTML 模板
├── references/
│   ├── 01_framework.md         # 标准 11 章框架 + 前置页/附录映射
│   ├── 02_style_guide.md       # 配色/字体/组件/logo/marker 规范
│   ├── 03_assessment_mapping.md # PTCD 评估 P0–P2 自动补齐映射
│   ├── 04_pipeline.md          # 4 阶段命令模板 + 常见坑
│   └── 05_input_requirements.md # 必填/选填输入 + 缺省策略
└── scripts/
    ├── scaffold_whitepaper.py   # 生成 HTML 骨架 + finalize.json
    ├── make_compare_diagram.py  # 参数化对比图（PIL，PICC/PORT/CVC 等）
    └── finalize_docx.py         # 嵌图 + 分页 + 校验
```

## 快速开始

### 前置依赖

- Python 3.10+（需 `Pillow`、`python-docx`）
- WorkBuddy 内置 `tencent-docx` 技能（提供 `html_to_docx` 转换器）

### 1. 准备配置

```json
{
  "topic": "血管通路(PICC/输液港)",
  "subtitle": "肿瘤患者中心静脉通路家属全程照护手册",
  "community": "小胰宝社区 · 天工开物基金会",
  "date": "2026-08-27",
  "accent": "#5c4a7a",
  "sources_dir": "/path/to/guide_collection",
  "output_dir": "/path/to/output",
  "diagram": {"enabled": true}
}
```

### 2. 生成骨架

```bash
python scripts/scaffold_whitepaper.py --config config.json
```

产出 `stage2/whitepaper.html` + `stage2/finalize.json`。

### 3. 填充内容

由 AI Agent 读取 `sources_dir` 中的指南/共识/案例 `.md`，提取关键内容填充到 HTML 骨架的各章节。

### 4. 生成对比图（可选）

```bash
python scripts/make_compare_diagram.py --config cards.json --out stage2/compare.png
```

### 5. 转换 + 定稿

```bash
# HTML → DOCX
html_to_docx convert stage2/whitepaper.html -o stage3/output.docx

# 嵌图 + 分页 + 校验
python scripts/finalize_docx.py --json stage2/finalize.json
```

## 核心特性

| 特性 | 说明 |
|---|---|
| 🎨 **统一风格** | 主色 `#5c4a7a`（紫）、Hiragino Sans GB 字体、行内样式提示框、三色急症卡 |
| 🏗️ **稳定框架** | 封面 → 编者按 → 目录 → 前置三页 → 主题章节 → 术语表 → 附录 A–G → 页脚 |
| 🛡️ **安全校准** | 处置类语句强制 `【安全提示·个体化医嘱】`，统一归口医护 |
| 📋 **工具包** | 出院交接单、复诊提问卡、维护记录表、耗材清单，均可打印 |
| 🔄 **主题适配** | 标准 11 章可增减/合并，对比图、主色、章节均可配置 |
| ✅ **质量门禁** | 0 残留 marker、0 占位、每章分页、图片嵌入校验 |

## 设计原则

本技能严格遵循以下原则（来自《PTCD 白皮书完成度评估与后续任务 v1.0》）：

1. **基于指南和共识**：所有操作建议以权威指南/共识为依据，引用标注出处
2. **结合病友经验**：以过来人口吻补充实操细节，但涉及处置的强制归口医护
3. **不替代医嘱**：每篇白皮书统一声明"不替代面诊与主治医生的个体化决策"
4. **可打印可携带**：关键表格（记录表/交接单/急症卡）设计为 A4 打印版式
5. **草稿待审核**：正式发布前留医护团队审核签字位

## 命名规范

- 最终 docx 文件名自动从 `topic` 派生：`{topic_slug}_output.docx`
- 如 `topic="血管通路(PICC/输液港)"` → `picc_output.docx`
- 如 `topic="PTCD 居家照护"` → `ptcd_output.docx`
- 也支持手动指定 `target_docx`

## 感谢 ❤️

本技能的核心框架、内容素材与社区 logo 来自**小胰宝（XYB）患者社区**。

感谢每一位小胰宝开发者、病友志愿者、合作医护团队的无私奉献。是你们在一线积累的经验、整理的指南、分享的案例，让这些白皮书有了真实的温度，让后来的病友和家属在照护路上少走弯路。

**用爱发电，以知识照亮前路。**

---

*xyb-whitepaper-writer is released under the MIT License. The community mascot logo is an asset of 小胰宝社区 and is bundled with this skill for the sole purpose of generating community-branded whitepapers.*