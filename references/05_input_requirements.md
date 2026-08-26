# 05 · 技能开发输入需求（Input Requirements）

> 用户要求"自行完善技能开发输入需求部分"。本文件把"调用本技能时需要什么输入、由谁提供、缺了怎么办"显式定义，作为技能对外的契约。

## 一、输入来源分层

| 层 | 提供方 | 内容 |
|---|---|---|
| 技能内置（随技能分发） | 开发者 | 框架、风格、脚本、logo、参考文档 |
| 调用时用户提供 | 用户/agent | 主题、资料源、输出路径、目标文件名、可选定制 |
| 运行时生成 | 技能脚本 | HTML 骨架、对比图、finalize.json、docx |

## 二、必填输入（缺则无法启动）

1. **`topic`（主题）** —— 决定标题、章节主题词。例："PTCD 居家照护"。
2. **`sources_dir`（资料源目录）** —— 含指南/共识/案例 `*.md`。技能只读取，不修改。
3. **`output_dir`（输出根）** —— 写入 `stage2/` `stage3/`。
4. **`target_docx`（目标文件名）** —— 最终 docx 名，默认从 topic 自动派生为 `{topic_slug}_output.docx`（例：topic="血管通路(PICC/输液港)" → `picc_output.docx`）。也可手动指定。

## 三、选填输入（缺则用默认值，产物中标注）

5. `subtitle` 副标题
6. `acronym_note` 通俗名↔专业名备注
7. `community` 社区署名（默认"小胰宝社区 · 天工开物基金会"）
8. `accent` 主色（默认 `#5c4a7a`）
9. `chapters` 章节大纲（默认标准 11 章，可增减）
10. `diagram` 对比图配置（默认无图）
11. `patient_resources` 病友实证资源（默认留"待社区补充"）
12. `advisors` 临床顾问署名（默认"待合作医护团队审核"）

## 四、输入交付形态

推荐用一份 `config.json` 一次性提供：
```json
{
  "topic": "PTCD 居家照护",
  "subtitle": "经皮肝穿刺胆道引流（PTCD）家属全程照护手册",
  "acronym_note": "PTCD 为通俗用语，专业称 PTBD",
  "community": "小胰宝社区 · 天工开物基金会",
  "date": "2026-08-26",
  "accent": "#5c4a7a",
  "sources_dir": "/path/to/collection",
  "output_dir": "/path/to/output/ptcd_whitepaper_2026-08-26",
  "target_docx": "ptcd_output.docx",
  "chapters": "default",
  "diagram": {"enabled": true, "config": "cards.json"},
  "patient_resources": "待社区补充",
  "advisors": "待合作医护团队审核"
}
```
scaffold 读取后生成骨架；后续内容填充由 agent 基于 `sources_dir` 完成。

## 五、缺省与降级策略

- 无 `sources_dir`：**拒绝启动**（白皮书必须基于指南/共识/病友经验，不能无源编造）。
- 无 `diagram`：生成无对比图版本（删除 HTML 中 marker 行）。
- 无 `patient_resources`：附录/资源章保留"待社区补充"占位（合法状态注，允许保留）。
- `accent` 异常：回退紫 `#5c4a7a`。

## 六、输出契约（技能保证）

- 产出 `stage3/<target_docx>` 一个 docx。
- 0 个 `INSERT_IMAGE` 残留、0 个"待补"占位（仅合法状态注可留）。
- 封面 logo + （可选）对比图 + 页脚 logo 均嵌入。
- 每 H1 分页；前置三页与工具包附录齐备。
- 标记"草稿 · 待双专业审核后发布"。
