#!/usr/bin/env python3
"""
Agent-interview diagrams — editorial clean style (v2).

Improvements vs v1:
- No notebook ruled lines (looked dated)
- Soft pastel fills + dark ink text (not solid PPT headers)
- Hiragino Sans GB W3/W6 type hierarchy
- Render @2x then downscale (sharper on retina)
- Clear loop topology (sequential, not parallel+serial mash)
- Module map rows left-aligned under a shared rail
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"

# Editorial tokens
BG = "#FAFAF8"
CARD = "#FFFFFF"
INK = "#1C1917"
MUTED = "#78716C"
LINE = "#D6D3D1"
RAIL = "#A8A29E"

BLUE = "#2563EB"
BLUE_SOFT = "#EFF6FF"
TEAL = "#0F766E"
TEAL_SOFT = "#F0FDFA"
ORANGE = "#C2410C"
ORANGE_SOFT = "#FFF7ED"
SLATE = "#57534E"
SLATE_SOFT = "#F5F5F4"
INDIGO = "#4338CA"
INDIGO_SOFT = "#EEF2FF"
RED = "#B91C1C"
RED_SOFT = "#FEF2F2"
AMBER = "#B45309"
AMBER_SOFT = "#FFFBEB"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=2 if bold else 0)


def new_canvas(w: int, h: int, scale: int = 2) -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
    img = Image.new("RGB", (w * scale, h * scale), BG)
    return img, ImageDraw.Draw(img), scale


def finish(img: Image.Image, path: Path, scale: int) -> None:
    if scale != 1:
        img = img.resize((img.width // scale, img.height // scale), Image.Resampling.LANCZOS)
    img.save(path, optimize=True)
    print("wrote", path)


def S(v: float, scale: int) -> int:
    return int(round(v * scale))


def card(
    d: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    scale: int,
    *,
    fill: str = CARD,
    outline: str = LINE,
    radius: float = 12,
    width: float = 1.5,
    accent: str | None = None,
    accent_w: float = 5,
) -> None:
    x0, y0, x1, y1 = (S(v, scale) for v in box)
    r = S(radius, scale)
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline, width=max(1, S(width, scale)))
    if accent:
        # left accent inset
        aw = S(accent_w, scale)
        d.rounded_rectangle([x0 + S(2, scale), y0 + S(10, scale), x0 + aw, y1 - S(10, scale)], radius=S(2, scale), fill=accent)


def arrow_v(d, x, y0, y1, scale, color=RAIL) -> None:
    x, y0, y1 = S(x, scale), S(y0, scale), S(y1, scale)
    head = S(6, scale)
    d.line([(x, y0), (x, y1 - head)], fill=color, width=max(1, S(1.5, scale)))
    d.polygon([(x - head // 2, y1 - head), (x + head // 2, y1 - head), (x, y1)], fill=color)


def arrow_h(d, x0, y, x1, scale, color=RAIL) -> None:
    x0, y, x1 = S(x0, scale), S(y, scale), S(x1, scale)
    head = S(6, scale)
    d.line([(x0, y), (x1 - head, y)], fill=color, width=max(1, S(1.5, scale)))
    d.polygon([(x1 - head, y - head // 2), (x1 - head, y + head // 2), (x1, y)], fill=color)


def txt(d, xy, text, f, scale, fill=INK, anchor="lt") -> None:
    d.text((S(xy[0], scale), S(xy[1], scale)), text, font=f, fill=fill, anchor=anchor)


# ─── 00 module map ───────────────────────────────────────────
def draw_00() -> None:
    w, h = 1000, 580
    img, d, s = new_canvas(w, h)
    ft, f, fs, fxs = font(S(24, s), True), font(S(13, s), True), font(S(12, s)), font(S(11, s))

    txt(d, (w / 2, 28), "Agent 工程师面试 · 12 模块地图", ft, s, anchor="mt")
    txt(d, (w / 2, 58), "边界 → 工具 → 架构 → 生产 → 系统设计", fs, s, MUTED, "mt")

    modules = [
        [("M1 基础边界", "6 题", BLUE, BLUE_SOFT), ("M2 Context", "5 题", BLUE, BLUE_SOFT),
         ("M3 Tool / MCP", "6 题", BLUE, BLUE_SOFT), ("M4 RAG", "5 题", BLUE, BLUE_SOFT),
         ("M5 单 Agent", "5 题", BLUE, BLUE_SOFT), ("M6 多 Agent", "5 题", BLUE, BLUE_SOFT)],
        [("M7 Memory", "4 题", TEAL, TEAL_SOFT), ("M8 Eval", "5 题", TEAL, TEAL_SOFT),
         ("M9 安全", "4 题", TEAL, TEAL_SOFT), ("M10 生产", "5 题", TEAL, TEAL_SOFT)],
        [("M11 系统设计", "4 题", ORANGE, ORANGE_SOFT), ("M12 行为面", "3 题", ORANGE, ORANGE_SOFT)],
    ]

    bw, bh, gap, left, tops = 140, 64, 16, 40, [100, 220, 340]
    centers: list[list[tuple[float, float]]] = []

    for ri, (row, top) in enumerate(zip(modules, tops)):
        row_c = []
        for i, (title, sub, color, soft) in enumerate(row):
            x = left + i * (bw + gap)
            card(d, (x, top, x + bw, top + bh), s, fill=soft, outline=color, width=1.5, accent=color)
            txt(d, (x + bw / 2 + 2, top + 18), title, f, s, color, "mt")
            txt(d, (x + bw / 2 + 2, top + 42), sub, fs, s, MUTED, "mt")
            row_c.append((x + bw / 2, top + bh / 2))
        centers.append(row_c)
        # horizontal arrows
        for i in range(len(row) - 1):
            x0 = left + i * (bw + gap) + bw
            x1 = left + (i + 1) * (bw + gap)
            arrow_h(d, x0 + 2, top + bh / 2, x1 - 2, s)

    # snake drops: end of row → start of next (aligned to left rail)
    for ri in range(2):
        sx, sy = centers[ri][-1]
        dx, dy = centers[ri + 1][0]
        top_a = tops[ri] + bh
        top_b = tops[ri + 1]
        mid = (top_a + top_b) / 2
        # down from last
        d.line([(S(sx, s), S(top_a, s)), (S(sx, s), S(mid, s))], fill=RAIL, width=max(1, S(1.5, s)))
        d.line([(S(sx, s), S(mid, s)), (S(dx, s), S(mid, s))], fill=RAIL, width=max(1, S(1.5, s)))
        arrow_v(d, dx, mid, top_b - 2, s)

    # legend
    chips = [("蓝区 · 打底", BLUE, BLUE_SOFT), ("青区 · 生产", TEAL, TEAL_SOFT), ("橙区 · 综合", ORANGE, ORANGE_SOFT)]
    cy, cw = 440, 150
    lx = (w - (3 * cw + 40)) / 2
    for i, (lab, c, soft) in enumerate(chips):
        x = lx + i * (cw + 20)
        card(d, (x, cy, x + cw, cy + 40), s, fill=soft, outline=c, accent=c)
        txt(d, (x + cw / 2 + 2, cy + 20), lab, fs, s, c, "mm")

    txt(d, (w / 2, 510), "合计 57 题 · 博客园每周三更（一 / 三 / 五）", fs, s, MUTED, "mt")
    txt(d, (w / 2, 536), "建议：蓝区打底 → 青区上生产 → 橙区综合", fxs, s, MUTED, "mt")
    finish(img, OUT / "00-module-map.png", s)


# ─── 01 boundary ─────────────────────────────────────────────
def draw_01_boundary() -> None:
    w, h = 1000, 480
    img, d, s = new_canvas(w, h)
    ft, f, fs, fxs = font(S(24, s), True), font(S(16, s), True), font(S(13, s)), font(S(11, s))
    txt(d, (w / 2, 24), "Chatbot · Workflow · Agent 边界", ft, s, anchor="mt")
    txt(d, (w / 2, 54), "先问控制权在谁手里，再决定叫什么名字", fs, s, MUTED, "mt")

    cols = [
        (SLATE, SLATE_SOFT, "Chatbot", "人持续提问", [
            "单轮 / 多轮对话",
            "主要产出：文本",
            "无自主选工具循环",
            "下一步由人驱动",
        ], "线性问答"),
        (BLUE, BLUE_SOFT, "Workflow", "规则定路径", [
            "预定义步骤图",
            "LLM 是节点之一",
            "分支由规则决定",
            "可预测、可回放",
        ], "固定流水线"),
        (TEAL, TEAL_SOFT, "Agent", "模型做决策", [
            "目标驱动循环",
            "模型选工具与顺序",
            "观察结果再规划",
            "需终止条件 / 人审",
        ], "目标 + 循环"),
    ]
    margin, gap = 40, 28
    cw = (w - 2 * margin - 2 * gap) // 3
    top, ch = 88, 300

    for i, (color, soft, title, who, lines, tag) in enumerate(cols):
        x = margin + i * (cw + gap)
        card(d, (x, top, x + cw, top + ch), s, fill=CARD, outline=LINE, accent=color, accent_w=6)
        # soft header strip
        d.rounded_rectangle(
            [S(x + 14, s), S(top + 14, s), S(x + cw - 14, s), S(top + 78, s)],
            radius=S(8, s),
            fill=soft,
        )
        txt(d, (x + cw / 2, top + 28), title, f, s, color, "mt")
        txt(d, (x + cw / 2, top + 54), who, fs, s, MUTED, "mt")

        # mini motif
        my = top + 100
        if i == 0:  # linear dots
            for k in range(3):
                cx = x + 50 + k * 70
                d.ellipse([S(cx - 5, s), S(my - 5, s), S(cx + 5, s), S(my + 5, s)], fill=color)
                if k < 2:
                    arrow_h(d, cx + 8, my, cx + 62, s, color)
        elif i == 1:  # stacked steps
            for k in range(3):
                yy = my - 8 + k * 14
                d.rounded_rectangle([S(x + 70, s), S(yy, s), S(x + cw - 70, s), S(yy + 10, s)], radius=S(3, s), fill=color)
        else:  # loop
            box = [S(x + cw / 2 - 28, s), S(my - 16, s), S(x + cw / 2 + 28, s), S(my + 20, s)]
            d.arc(box, 40, 320, fill=color, width=max(2, S(2, s)))
            # arrow tip
            d.polygon(
                [
                    (S(x + cw / 2 + 22, s), S(my + 14, s)),
                    (S(x + cw / 2 + 34, s), S(my + 8, s)),
                    (S(x + cw / 2 + 20, s), S(my + 2, s)),
                ],
                fill=color,
            )

        txt(d, (x + cw / 2, top + 130), tag, fxs, s, color, "mt")
        y = top + 158
        for line in lines:
            d.ellipse([S(x + 28, s), S(y + 5, s), S(x + 36, s), S(y + 13, s)], fill=color)
            txt(d, (x + 46, y), line, fs, s, INK, "lt")
            y += 32

    txt(d, (w / 2, 416), "面试加分：先画控制权（人 / 规则图 / 模型）", fs, s, MUTED, "mt")
    txt(d, (w / 2, 442), "可组合：Workflow 嵌 Agent · Agent 某步可回落 Chat", fxs, s, MUTED, "mt")
    finish(img, OUT / "01-boundary.png", s)


# ─── 01 agent loop ───────────────────────────────────────────
def draw_01_loop() -> None:
    w, h = 760, 520
    img, d, s = new_canvas(w, h)
    ft, f, fs, fxs = font(S(22, s), True), font(S(14, s), True), font(S(12, s)), font(S(11, s))
    txt(d, (w / 2, 22), "Agent 最小控制回路", ft, s, anchor="mt")
    txt(d, (w / 2, 52), "白板 30 秒可画完 · 缺「观察」或「终止」通常说明没落地", fs, s, MUTED, "mt")

    # vertical sequential chain (clear topology)
    nodes = [
        (BLUE, BLUE_SOFT, "目标 / 用户请求"),
        (INDIGO, INDIGO_SOFT, "思考 / 规划"),
        (TEAL, TEAL_SOFT, "选工具"),
        (TEAL, TEAL_SOFT, "执行"),
        (TEAL, TEAL_SOFT, "观察结果"),
        (ORANGE, ORANGE_SOFT, "完成？"),
    ]
    bw, bh = 200, 44
    cx = w / 2
    top0 = 90
    gap = 18
    ys = []
    for i, (color, soft, label) in enumerate(nodes):
        y = top0 + i * (bh + gap)
        ys.append(y)
        x0 = cx - bw / 2
        card(d, (x0, y, x0 + bw, y + bh), s, fill=soft, outline=color, accent=color, accent_w=5)
        txt(d, (cx + 2, y + bh / 2), label, f, s, color, "mm")
        if i < len(nodes) - 1:
            arrow_v(d, cx, y + bh, y + bh + gap, s)

    # loop back from 完成 to 思考
    think_y = ys[1] + bh / 2
    done_y = ys[-1] + bh / 2
    left_x = cx - bw / 2 - 70
    d.line(
        [
            (S(cx - bw / 2, s), S(done_y, s)),
            (S(left_x, s), S(done_y, s)),
            (S(left_x, s), S(think_y, s)),
            (S(cx - bw / 2, s), S(think_y, s)),
        ],
        fill=ORANGE,
        width=max(2, S(2, s)),
    )
    # arrow into think
    head = S(7, s)
    d.polygon(
        [
            (S(cx - bw / 2, s), S(think_y, s)),
            (S(cx - bw / 2 - head, s), S(think_y - head / 2, s)),
            (S(cx - bw / 2 - head, s), S(think_y + head / 2, s)),
        ],
        fill=ORANGE,
    )
    txt(d, (left_x - 8, (think_y + done_y) / 2), "未完成", fxs, s, ORANGE, "rm")

    # exit
    last_y = ys[-1] + bh
    arrow_v(d, cx, last_y, last_y + 28, s)
    txt(d, (cx, last_y + 40), "输出 / 升级人工", fs, s, MUTED, "mt")

    # constraint chips
    chips = ["步数上限", "Token / 钱预算", "人工确认点"]
    cy = 470
    total = sum(80 + len(c) * 6 for c in chips) + 40
    # simpler fixed chips
    chip_w = 140
    lx = (w - 3 * chip_w - 40) / 2
    for i, lab in enumerate(chips):
        x = lx + i * (chip_w + 20)
        card(d, (x, cy, x + chip_w, cy + 32), s, fill=SLATE_SOFT, outline=LINE)
        txt(d, (x + chip_w / 2, cy + 16), lab, fxs, s, MUTED, "mm")

    finish(img, OUT / "01-agent-loop.png", s)


# ─── 02 when not ─────────────────────────────────────────────
def draw_02() -> None:
    w, h = 1000, 540
    img, d, s = new_canvas(w, h)
    ft, f, fs, fxs = font(S(22, s), True), font(S(14, s), True), font(S(12, s)), font(S(11, s))
    txt(d, (w / 2, 22), "何时不上 Agent：快速否决清单", ft, s, anchor="mt")
    txt(d, (w / 2, 52), "否决的核心不是模型够不够聪明，而是控制权该不该交给它", fs, s, MUTED, "mt")

    cards = [
        (RED, RED_SOFT, "路径写得清", "步骤固定、分支少", "改用 Workflow / 规则"),
        (RED, RED_SOFT, "失败不可回滚", "付款、删库、合规", "改用人工 / 强审批流"),
        (RED, RED_SOFT, "必须可复现", "审计、对账、法务", "改用确定性编排"),
        (AMBER, AMBER_SOFT, "延迟 / 成本极敏感", "毫秒级或极省钱", "改用缓存 / 单次调用"),
        (AMBER, AMBER_SOFT, "工具面太窄", "几乎只有聊天", "Chatbot 即可"),
        (AMBER, AMBER_SOFT, "开放目标但无护栏", "无步数 / 预算 / 权限", "先补约束再谈 Agent"),
    ]
    margin, gap_x, gap_y = 40, 22, 22
    cw = (w - 2 * margin - 2 * gap_x) // 3
    ch = 150
    for i, (color, soft, title, sub, alt) in enumerate(cards):
        row, col = divmod(i, 3)
        x = margin + col * (cw + gap_x)
        y = 90 + row * (ch + gap_y)
        card(d, (x, y, x + cw, y + ch), s, fill=CARD, outline=LINE, accent=color, accent_w=6)
        # soft title pill
        d.rounded_rectangle(
            [S(x + 18, s), S(y + 16, s), S(x + cw - 18, s), S(y + 48, s)],
            radius=S(8, s),
            fill=soft,
        )
        txt(d, (x + cw / 2, y + 32), title, f, s, color, "mm")
        txt(d, (x + cw / 2, y + 72), sub, fs, s, MUTED, "mt")
        d.line([(S(x + 28, s), S(y + 100, s)), (S(x + cw - 28, s), S(y + 100, s))], fill=LINE, width=max(1, S(1, s)))
        txt(d, (x + cw / 2, y + 118), alt, fs, s, INK, "mt")

    txt(d, (w / 2, 490), "面试加分：举你亲手否决过的真实场景，而不是背清单", fs, s, MUTED, "mt")
    finish(img, OUT / "02-when-not.png", s)


# ─── 03 react vs plan ────────────────────────────────────────
def draw_03() -> None:
    w, h = 1000, 520
    img, d, s = new_canvas(w, h)
    ft, f, fs, fxs = font(S(22, s), True), font(S(15, s), True), font(S(13, s)), font(S(11, s))
    txt(d, (w / 2, 22), "ReAct vs Plan-and-Execute", ft, s, anchor="mt")
    txt(d, (w / 2, 52), "选型看三件事：反馈密度 · 计划稳定性 · 是否要人审计划", fs, s, MUTED, "mt")

    panels = [
        (
            BLUE,
            BLUE_SOFT,
            "ReAct",
            "边想边做",
            [
                "Thought 思考",
                "Action 调工具",
                "Observation 看结果",
                "循环直到终止",
            ],
            "适合：反馈密、计划易变",
        ),
        (
            TEAL,
            TEAL_SOFT,
            "Plan-and-Execute",
            "先计划再执行",
            [
                "先产出完整计划（可审）",
                "再逐步执行子步骤",
                "偏差大则重规划",
                "规划 / 执行可换模型",
            ],
            "适合：步骤长、要审计、可并行",
        ),
    ]
    margin, gap = 44, 36
    pw = (w - 2 * margin - gap) // 2
    top, ph = 84, 360

    for i, (color, soft, title, sub, steps, fit) in enumerate(panels):
        x = margin + i * (pw + gap)
        card(d, (x, top, x + pw, top + ph), s, fill=CARD, outline=LINE, accent=color, accent_w=6)
        d.rounded_rectangle(
            [S(x + 16, s), S(top + 16, s), S(x + pw - 16, s), S(top + 78, s)],
            radius=S(10, s),
            fill=soft,
        )
        txt(d, (x + pw / 2, top + 34), title, f, s, color, "mt")
        txt(d, (x + pw / 2, top + 58), sub, fs, s, MUTED, "mt")

        y = top + 100
        for idx, lab in enumerate(steps):
            bx0, by0 = x + 36, y
            bx1, by1 = x + pw - 36, y + 44
            card(d, (bx0, by0, bx1, by1), s, fill=soft, outline=color, width=1.25, accent=None)
            # number badge
            d.ellipse([S(bx0 + 14, s), S(by0 + 10, s), S(bx0 + 38, s), S(by0 + 34, s)], fill=color)
            txt(d, (bx0 + 26, by0 + 22), str(idx + 1), fs, s, "#fff", "mm")
            txt(d, (bx0 + 50, by0 + 22), lab, fs, s, INK, "lm")
            if idx < len(steps) - 1:
                arrow_v(d, x + pw / 2, by1, y + 52, s)
            y += 56

        txt(d, (x + pw / 2, top + ph - 28), fit, fxs, s, color, "mt")

    finish(img, OUT / "03-react-vs-plan.png", s)


if __name__ == "__main__":
    draw_00()
    draw_01_boundary()
    draw_01_loop()
    draw_02()
    draw_03()
    print("done v2")
