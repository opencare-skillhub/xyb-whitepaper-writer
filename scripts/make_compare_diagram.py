#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_compare_diagram.py — 通用多方案对比图示生成器（PIL，中文 Hiragino Sans GB）

cards.json 结构：
{
  "title": "三种血管通路对比图示",
  "subtitle": "PICC · 输液港（PORT）· CVC —— 置入位置、留置时长、维护与风险一览",
  "bottom_tip": "怎么选？短期住院用 CVC；长期化疗首选输液港……",
  "cards": [
    {
      "name": "PICC", "en": "经外周静脉置入中心静脉导管",
      "accent": [232,116,59],
      "placement": "上臂浅静脉", "duration": "数月至 1 年",
      "maint": "每周 1 次", "look": "手臂留一截导管", "risk": "感染/血栓/堵管较高",
      "who": "化疗 < 1 年", "mlabel": "上臂静脉置入", "mtype": "arm"
    }
  ]
}
mtype ∈ {arm, chest, neck}  决定人体剪影上的置入位置标注。

用法：
  python make_compare_diagram.py --config cards.json --out compare.png
"""
import os, sys, json, argparse
from PIL import Image, ImageDraw, ImageFont

FP = "/System/Library/Fonts/Hiragino Sans GB.ttc"
def F(size, bold=False):
    try:
        return ImageFont.truetype(FP, size, index=1 if bold else 0)
    except Exception:
        return ImageFont.load_default()

W, H = 1800, 1440
M = 48
BG = (255, 255, 255)
CARD_BG = (247, 250, 252)
BORDER = (214, 224, 232)
DARK = (43, 58, 66)
MUTED = (107, 123, 133)
TITLE = (31, 61, 77)
HEART = (214, 69, 79)


def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def tlabel(d, text, box, font, color, anchor="mm"):
    d.text((box[0], box[1]), text, font=font, fill=color, anchor=anchor)

def text_wrap(d, text, font, max_w):
    lines, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=font) <= max_w:
            cur += ch
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines


def draw_silhouette(d, cx, sy, accent):
    hr = 40
    head_cy = sy + hr + 6
    d.ellipse([cx-hr, head_cy-hr, cx+hr, head_cy+hr], fill=(233,239,243), outline=(176,190,201), width=3)
    sh_y = head_cy + hr + 14
    hip_y = sy + 360
    torso = [cx-70, sh_y, cx+70, sh_y, cx+58, hip_y, cx-58, hip_y]
    d.polygon(torso, fill=(233,239,243), outline=(176,190,201))
    d.line([(cx-70, sh_y), (cx+70, sh_y)], fill=(176,190,201), width=3)
    d.line([(cx-66, sh_y+10), (cx-150, sh_y+120)], fill=(176,190,201), width=14)
    d.line([(cx+66, sh_y+10), (cx+150, sh_y+120)], fill=(176,190,201), width=14)
    d.line([(cx-30, hip_y), (cx-44, hip_y+150)], fill=(176,190,201), width=16)
    d.line([(cx+30, hip_y), (cx+44, hip_y+150)], fill=(176,190,201), width=16)
    hx, hy = cx, sh_y + 70
    d.polygon([(hx, hy+18), (hx-22, hy-6), (hx-10, hy-20), (hx, hy-10), (hx+10, hy-20), (hx+22, hy-6)], fill=HEART)
    return head_cy, sh_y, hip_y


def build(cfg):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cards = cfg.get("cards", [])
    n = max(1, len(cards))

    tlabel(d, cfg.get("title", "方案对比图示"), (W/2, 70), F(46, True), TITLE, anchor="mm")
    sub = cfg.get("subtitle", "")
    if sub:
        tlabel(d, sub, (W/2, 122), F(24), MUTED, anchor="mm")
    for x in range(M, W-M, 16):
        d.line([(x, 152), (x+9, 152)], fill=BORDER, width=2)

    gap = 28
    colW = (W - 2*M - (n-1)*gap) / float(n)
    col_x = [M + i*(colW+gap) for i in range(n)]
    HEAD_Y0, HEAD_Y1 = 178, 300
    SIL_Y0, SIL_Y1 = 318, 838
    DIV_Y = 852
    BADGE_Y0, BADGE_Y1 = 872, 1302
    N_BADGE = 5
    badgeH = (BADGE_Y1 - BADGE_Y0 - (N_BADGE-1)*10) / N_BADGE

    for i, c in enumerate(cards):
        x = col_x[i]
        acc = tuple(c.get("accent", [120,120,160]))
        rr(d, [x, HEAD_Y0, x+colW, BADGE_Y1+8], 16, fill=CARD_BG, outline=BORDER, width=2)
        rr(d, [x, HEAD_Y0, x+colW, HEAD_Y1], 16, fill=acc)
        d.rectangle([x, HEAD_Y1-30, x+colW, HEAD_Y1], fill=acc)
        tlabel(d, c["name"], (x+colW/2, HEAD_Y0+44), F(40, True), (255,255,255), anchor="mm")
        for k, ln in enumerate(text_wrap(d, c.get("en",""), F(19), colW-40)):
            tlabel(d, ln, (x+colW/2, HEAD_Y0+92 + k*24), F(19), (255,255,255), anchor="mm")

        cx = x + colW/2
        head_cy, sh_y, hip_y = draw_silhouette(d, cx, SIL_Y0, acc)
        mt = c.get("mtype", "arm")
        if mt == "arm":
            mx, my = cx-150, sh_y+120
            d.ellipse([mx-15, my-15, mx+15, my+15], fill=acc, outline=(255,255,255), width=3)
            d.line([(mx, my), (cx-30, sh_y+60)], fill=acc, width=5)
        elif mt == "chest":
            pbx, pby = cx, sh_y+150
            d.rounded_rectangle([pbx-26, pby-18, pbx+26, pby+18], radius=8, outline=acc, width=2)
            d.rounded_rectangle([pbx-22, pby-14, pbx+22, pby+14], radius=6, fill=acc)
            d.line([(pbx, pby-18), (cx, sh_y+78)], fill=acc, width=4)
            d.line([(pbx, pby-44), (pbx, pby-20)], fill=(120,120,120), width=4)
            d.ellipse([pbx-6, pby-48, pbx+6, pby-38], fill=(120,120,120))
        else:
            mx, my = cx, head_cy + 30
            d.ellipse([mx-15, my-15, mx+15, my+15], fill=acc, outline=(255,255,255), width=3)
            d.line([(mx, my), (cx, sh_y+44)], fill=acc, width=5)
        tlabel(d, c.get("mlabel", c["name"]), (cx, SIL_Y1-6), F(20, True), acc, anchor="mm")

        d.line([(x+20, DIV_Y), (x+colW-20, DIV_Y)], fill=BORDER, width=2)
        badges = [("置入位置", c.get("placement","")), ("留置时长", c.get("duration","")),
                  ("维护频率", c.get("maint","")), ("体表外观", c.get("look","")), ("主要风险", c.get("risk",""))]
        y = BADGE_Y0
        for label, val in badges:
            rr(d, [x+14, y, x+colW-14, y+badgeH], 10, fill=(255,255,255), outline=BORDER, width=1)
            d.rectangle([x+14, y+10, x+22, y+badgeH-10], fill=acc)
            tlabel(d, label, (x+34, y+20), F(21, True), acc, anchor="lm")
            for k, ln in enumerate(text_wrap(d, val, F(23), colW-70)[:2]):
                tlabel(d, ln, (x+34, y+48 + k*27), F(23), DARK, anchor="lm")
            y += badgeH + 10

    tip = cfg.get("bottom_tip")
    if tip:
        ty0, ty1 = 1320, 1412
        rr(d, [M, ty0, W-M, ty1], 14, fill=TITLE)
        for k, ln in enumerate(text_wrap(d, tip, F(23), W-2*M-60)[:2]):
            tlabel(d, ln, (W/2, ty0+34 + k*30), F(23), (255,255,255), anchor="mm")
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    with open(args.config, encoding="utf-8") as f:
        cfg = json.load(f)
    img = build(cfg)
    parent = os.path.dirname(args.out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    img.save(args.out)
    print("saved", args.out, img.size)


if __name__ == "__main__":
    main()
