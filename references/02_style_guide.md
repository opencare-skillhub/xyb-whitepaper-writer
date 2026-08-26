# 02 · 统一设计系统（Style Guide）

所有主题共用同一视觉语言，保证"小胰宝"品牌一致性。

## 一、配色（CSS 变量，写进 HTML `<style>`）

| 角色 | 值 | 用法 |
|---|---|---|
| 主色 accent | `#5c4a7a` | 封面标题带、H1/H2 文字、卡片标题、急症卡底 |
| accent 深 | `#4a3d63` | H2 文字 |
| accent 浅 | `#9480b0` | 副标题、letter-spacing 标签 |
| 正文 dark | `#333` / `#444` | 段落 |
| 弱化 muted | `#666` / `#888` / `#999` | 说明、页码、脚注 |
| 卡片底 | `#f7f4fb` 或 `#f7fafc` | callout / 区块背景 |
| 边框 border | `#e3dcec` / `#d6e0e8` | 卡片、表格线 |
| 红(急症) | `#d64545` | 🔴 立即急诊 |
| 黄(急症) | `#e0a800` | 🟡 当天联系 |
| 绿(急症) | `#2e9e6b` | 🟢 正常观察 |

> 新主题如需换色，只改 `accent` 一个变量（及同系深/浅推导），其余保持不变。scaffold 通过 config 注入。

## 二、字体

- **中文正文/标题**：转换器默认中文字体（docx）；HTML 不强行指定，交由转换器套用。
- **图内文字（PIL 生成对比图/示意图）**：`/System/Library/Fonts/Hiragino Sans GB.ttc`，`index=1` 粗、`index=0` 常规。脚本已硬编码此路径并做 fallback。
- 数字/英文可用系统字体，中文必须走上述 CJK 字体，避免豆腐块。

## 三、组件（HTML 写法，转换器可识别）

### 1) 提示框 callout（⚠️ 必须用行内样式 div，不可用 `data-component`）
> 经验：本转换器会**丢弃 `data-component` 属性及其内容**，用 `data-component="callout"` 会导致整段提示文字丢失。改用行内样式 `<div>`：
```html
<div style="background:#f7f4fb;border-left:4px solid #5c4a7a;border-radius:6px;padding:10px 14px;margin:12px 0;">
  <p style="margin:0;font-size:13px;"><strong>小标题：</strong>内容……</p>
</div>
```

### 2) 安全提示（强制，处置类必接）
```html
<div style="background:#f7f4fb;border-left:4px solid #5c4a7a;border-radius:6px;padding:10px 14px;margin:12px 0;">
  <p style="margin:0;font-size:13px;"><strong>【安全提示·个体化医嘱】</strong>本操作必须经<strong>置管/主治团队授权</strong>后执行；居家严禁自行套用他人方案。下文只讲"什么情况要找团队"，不提供可照抄处方。</p>
</div>
```

### 3) 表格（含表头、可设列宽）
```html
<table>
  <tr><th style="width:30%;">项目</th><th>内容</th></tr>
  <tr><td>…</td><td>…</td></tr>
</table>
```

### 4) 急症卡（三色表）
表头：`颜色 | 出现这些情况 | 立刻做什么（找谁）`；行：🔴红·立即急诊 / 🟡黄·当天联系 / 🟢绿·正常观察。

### 5) 对比图（marker 方式，finalize 嵌图）
```html
<p style="text-align:center;margin:14px 0 4px;">{{INSERT_IMAGE_COMPARE}}</p>
<p style="text-align:center;font-size:12px;color:#888;margin:0 0 10px;">图 1-1　三种…对比图</p>
```

### 6) 封面 / 页脚 logo（**均用 marker，不要 `<img>`**）
> 经验：本转换器对 `<img>` 内嵌不可靠（仅首图、且行为不稳），所有图统一用 `{{INSERT_IMAGE_xxx}}` 文本 marker，留待 finalize 阶段嵌入。
```html
<!-- 封面 -->
<p style="text-align:center;">{{INSERT_IMAGE_COVER_LOGO}}</p>
<!-- 页脚 -->
<p style="text-align:center;">{{INSERT_IMAGE_COMMUNITY_LOGO}}</p>
```

## 四、logo 用法

| 位置 | 形式 | 尺寸 |
|---|---|---|
| 封面 | `{{INSERT_IMAGE_COVER_LOGO}}` → finalize 嵌图 | Cm 3.2 |
| 页脚 | `{{INSERT_IMAGE_COMMUNITY_LOGO}}` → finalize 嵌图 | Cm 6 |
| 对比图 | 由 make_compare_diagram.py 生成 | Cm 15.5 |

> logo 文件随技能分发于 `assets/logo_mascot.png`；scaffold 会复制到 `stage2/`，finalize 在阶段4相对 `images_dir` 解析并嵌入。

## 五、分页

- 每个 H1（章节/附录）`page_break_before = True`。
- 封面标题（含"白皮书"三字）跳过分页，避免空白页。
- 前置三页、术语表、各附录均因是 H1 而自动分页。
