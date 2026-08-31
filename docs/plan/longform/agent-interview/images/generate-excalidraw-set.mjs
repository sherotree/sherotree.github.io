#!/usr/bin/env node
/**
 * Regenerate agent-interview diagrams via excalidraw-diagram-generator conventions.
 * fontFamily: 5 (Excalifont) on all text; hachure fills; roughness 1.
 *
 * Usage:
 *   node generate-excalidraw-set.mjs
 *   node ../.agents/.../export.mjs <file> -o <png>
 */

import { writeFileSync, mkdirSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import { spawnSync } from "child_process";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = __dirname;
const EXPORT = join(
  __dirname,
  "../../../../../../../.agents/skills/tech-diagram/scripts/excalidraw/export.mjs",
);

let seq = 0;
const uid = (p = "e") => `${p}_${(++seq).toString(36)}_${Math.floor(Math.random() * 1e6)}`;
const seed = () => Math.floor(Math.random() * 2 ** 31);
const now = Date.now();

const C = {
  ink: "#1e1e1e",
  muted: "#868e96",
  blue: "#a5d8ff",
  blueStroke: "#1971c2",
  green: "#b2f2bb",
  greenStroke: "#2f9e44",
  teal: "#99e9f2",
  tealStroke: "#0c8599",
  yellow: "#ffec99",
  yellowStroke: "#f59f00",
  red: "#ffc9c9",
  redStroke: "#e03131",
  violet: "#d0bfff",
  violetStroke: "#7048e8",
  orange: "#ffd8a8",
  orangeStroke: "#e8590c",
  gray: "#e9ecef",
  grayStroke: "#495057",
};

function base(partial) {
  return {
    angle: 0,
    strokeWidth: 2,
    strokeStyle: "solid",
    roughness: 1,
    opacity: 100,
    groupIds: [],
    frameId: null,
    index: `a${seq}`,
    roundness: null,
    seed: seed(),
    version: 1,
    versionNonce: seed(),
    isDeleted: false,
    boundElements: null,
    updated: now,
    link: null,
    locked: false,
    ...partial,
  };
}

/** Labeled rounded rectangle (rect + bound text), fontFamily 5 */
function labeledBox({ id, x, y, w, h, text, fill, stroke, fontSize = 18 }) {
  const rid = id || uid("box");
  const tid = uid("txt");
  const rect = base({
    id: rid,
    type: "rectangle",
    x,
    y,
    width: w,
    height: h,
    strokeColor: stroke || C.ink,
    backgroundColor: fill || C.blue,
    fillStyle: "hachure",
    roundness: { type: 3 },
    boundElements: [{ id: tid, type: "text" }],
  });
  const te = base({
    id: tid,
    type: "text",
    x: x + 8,
    y: y + (h - fontSize * 1.25) / 2,
    width: w - 16,
    height: fontSize * 1.25,
    strokeColor: C.ink,
    backgroundColor: "transparent",
    fillStyle: "solid",
    strokeWidth: 1,
    roughness: 0,
    roundness: null,
    text,
    fontSize,
    fontFamily: 5,
    textAlign: "center",
    verticalAlign: "middle",
    containerId: rid,
    originalText: text,
    lineHeight: 1.25,
    autoResize: true,
  });
  return { elements: [rect, te], box: { id: rid, x, y, w, h } };
}

function titleText(x, y, text, fontSize = 28) {
  return base({
    id: uid("title"),
    type: "text",
    x,
    y,
    width: Math.max(200, text.length * fontSize * 0.7),
    height: fontSize * 1.4,
    strokeColor: C.ink,
    backgroundColor: "transparent",
    fillStyle: "solid",
    strokeWidth: 1,
    roughness: 0,
    text,
    originalText: text,
    fontSize,
    fontFamily: 5,
    textAlign: "left",
    verticalAlign: "top",
    containerId: null,
    lineHeight: 1.25,
    autoResize: true,
  });
}

function noteText(x, y, text, fontSize = 16, color = C.muted) {
  return base({
    id: uid("note"),
    type: "text",
    x,
    y,
    width: Math.max(120, text.length * fontSize * 0.65),
    height: fontSize * 1.4,
    strokeColor: color,
    backgroundColor: "transparent",
    fillStyle: "solid",
    strokeWidth: 1,
    roughness: 0,
    text,
    originalText: text,
    fontSize,
    fontFamily: 5,
    textAlign: "left",
    verticalAlign: "top",
    containerId: null,
    lineHeight: 1.25,
    autoResize: true,
  });
}

function arrow(x, y, points, stroke = C.muted, endArrowhead = "arrow") {
  const xs = points.map((p) => p[0]);
  const ys = points.map((p) => p[1]);
  return base({
    id: uid("arr"),
    type: "arrow",
    x,
    y,
    width: Math.max(...xs) - Math.min(...xs) || 1,
    height: Math.max(...ys) - Math.min(...ys) || 1,
    strokeColor: stroke,
    backgroundColor: "transparent",
    fillStyle: "solid",
    roundness: { type: 2 },
    points,
    startBinding: null,
    endBinding: null,
    startArrowhead: null,
    endArrowhead,
    lastCommittedPoint: null,
  });
}

function doc(elements, bg = "#ffffff") {
  return {
    type: "excalidraw",
    version: 2,
    source: "https://excalidraw.com",
    elements,
    appState: { viewBackgroundColor: bg, gridSize: 20 },
    files: {},
  };
}

function save(name, elements) {
  const path = join(OUT, `${name}.excalidraw`);
  writeFileSync(path, JSON.stringify(doc(elements), null, 2));
  console.log("wrote", path, elements.length, "elements");
  return path;
}

function exportPng(excalPath, pngName) {
  const png = join(OUT, pngName);
  const r = spawnSync(process.execPath, [EXPORT, excalPath, "-o", png, "--scale", "2"], {
    stdio: "inherit",
  });
  if (r.status !== 0) process.exit(r.status ?? 1);
}

// ─── 00 module map ───────────────────────────────────────────
function gen00() {
  const els = [];
  els.push(titleText(280, 30, "Agent 工程师面试 · 12 模块地图", 28));
  els.push(noteText(260, 70, "边界 → 工具 → 架构 → 生产 → 系统设计", 16));

  const rows = [
    {
      y: 120,
      color: C.blue,
      stroke: C.blueStroke,
      items: [
        ["M1 基础边界", "6 题"],
        ["M2 Context", "5 题"],
        ["M3 Tool/MCP", "6 题"],
        ["M4 RAG", "5 题"],
        ["M5 单 Agent", "5 题"],
        ["M6 多 Agent", "5 题"],
      ],
    },
    {
      y: 260,
      color: C.teal,
      stroke: C.tealStroke,
      items: [
        ["M7 Memory", "4 题"],
        ["M8 Eval", "5 题"],
        ["M9 安全", "4 题"],
        ["M10 生产", "5 题"],
      ],
    },
    {
      y: 400,
      color: C.orange,
      stroke: C.orangeStroke,
      items: [
        ["M11 系统设计", "4 题"],
        ["M12 行为面", "3 题"],
      ],
    },
  ];

  const bw = 140;
  const bh = 70;
  const gap = 18;
  const left = 40;
  const boxes = [];

  for (const row of rows) {
    row.items.forEach(([title, sub], i) => {
      const x = left + i * (bw + gap);
      const { elements, box } = labeledBox({
        x,
        y: row.y,
        w: bw,
        h: bh,
        text: `${title}\n${sub}`,
        fill: row.color,
        stroke: row.stroke,
        fontSize: 15,
      });
      // two-line text needs taller text box — rebuild text height
      const te = elements[1];
      te.height = 40;
      te.y = row.y + 15;
      te.fontSize = 15;
      els.push(...elements);
      boxes.push(box);
    });
  }

  // horizontal arrows within rows
  const connectRow = (startIdx, count, y) => {
    for (let i = 0; i < count - 1; i++) {
      const a = boxes[startIdx + i];
      const b = boxes[startIdx + i + 1];
      els.push(
        arrow(a.x + a.w, y + bh / 2, [
          [0, 0],
          [gap, 0],
        ]),
      );
    }
  };
  connectRow(0, 6, 120);
  connectRow(6, 4, 260);
  connectRow(10, 2, 400);

  // snake drops
  const drop = (from, to) => {
    const a = boxes[from];
    const b = boxes[to];
    const x1 = a.x + a.w / 2;
    const y1 = a.y + a.h;
    const x2 = b.x + b.w / 2;
    const y2 = b.y;
    const mid = (y1 + y2) / 2;
    els.push(
      arrow(x1, y1, [
        [0, 0],
        [0, mid - y1],
        [x2 - x1, mid - y1],
        [x2 - x1, y2 - y1],
      ]),
    );
  };
  drop(5, 6);
  drop(9, 10);

  // legend
  const legends = [
    [40, 520, "蓝区 · 打底", C.blue, C.blueStroke],
    [220, 520, "青区 · 生产", C.teal, C.tealStroke],
    [400, 520, "橙区 · 综合", C.orange, C.orangeStroke],
  ];
  for (const [x, y, t, fill, stroke] of legends) {
    els.push(...labeledBox({ x, y, w: 150, h: 44, text: t, fill, stroke, fontSize: 16 }).elements);
  }
  els.push(noteText(200, 590, "合计 57 题 · 博客园每周三更（一 / 三 / 五）", 16));
  els.push(noteText(220, 620, "建议：蓝区打底 → 青区上生产 → 橙区综合", 15));

  return save("00-module-map", els);
}

// ─── 01 boundary ─────────────────────────────────────────────
function gen01Boundary() {
  const els = [];
  els.push(titleText(220, 24, "Chatbot · Workflow · Agent 边界", 28));
  els.push(noteText(240, 64, "先问控制权在谁手里，再决定叫什么名字", 16));

  const cols = [
    {
      title: "Chatbot",
      who: "人持续提问",
      fill: C.gray,
      stroke: C.grayStroke,
      lines: ["单轮 / 多轮对话", "主要产出：文本", "无自主选工具循环", "下一步由人驱动"],
      tag: "线性问答",
    },
    {
      title: "Workflow",
      who: "规则定路径",
      fill: C.blue,
      stroke: C.blueStroke,
      lines: ["预定义步骤图", "LLM 是节点之一", "分支由规则决定", "可预测、可回放"],
      tag: "固定流水线",
    },
    {
      title: "Agent",
      who: "模型做决策",
      fill: C.teal,
      stroke: C.tealStroke,
      lines: ["目标驱动循环", "模型选工具与顺序", "观察结果再规划", "需终止条件 / 人审"],
      tag: "目标 + 循环",
    },
  ];

  const cw = 260;
  const gap = 36;
  const left = 50;
  const top = 110;

  cols.forEach((col, i) => {
    const x = left + i * (cw + gap);
    els.push(...labeledBox({ x, y: top, w: cw, h: 70, text: `${col.title}\n${col.who}`, fill: col.fill, stroke: col.stroke, fontSize: 18 }).elements);
    els[els.length - 1].height = 48;
    els[els.length - 1].y = top + 12;

    els.push(...labeledBox({ x: x + 40, y: top + 90, w: cw - 80, h: 36, text: col.tag, fill: "#fff", stroke: col.stroke, fontSize: 15 }).elements);

    col.lines.forEach((line, j) => {
      els.push(noteText(x + 20, top + 150 + j * 36, `•  ${line}`, 16, C.ink));
    });
  });

  els.push(noteText(180, 360, "面试加分：先画控制权（人 / 规则图 / 模型）", 16));
  els.push(noteText(160, 395, "可组合：Workflow 嵌 Agent · Agent 某步可回落 Chat", 15));
  return save("01-boundary", els);
}

// ─── 01 agent loop ───────────────────────────────────────────
function gen01Loop() {
  const els = [];
  els.push(titleText(200, 24, "Agent 最小控制回路", 28));
  els.push(noteText(120, 64, "缺「观察」或「终止」——通常说明还没落地", 16));

  const nodes = [
    [C.blue, C.blueStroke, "1  目标 / 用户请求"],
    [C.violet, C.violetStroke, "2  思考 / 规划"],
    [C.teal, C.tealStroke, "3  选工具 → 执行 → 观察"],
    [C.orange, C.orangeStroke, "4  完成？"],
  ];
  const bw = 300;
  const bh = 56;
  const cx = 200;
  const top0 = 110;
  const gap = 40;
  const boxes = [];

  nodes.forEach(([fill, stroke, text], i) => {
    const y = top0 + i * (bh + gap);
    const { elements, box } = labeledBox({ x: cx, y, w: bw, h: bh, text, fill, stroke, fontSize: 18 });
    els.push(...elements);
    boxes.push(box);
    if (i < nodes.length - 1) {
      els.push(
        arrow(cx + bw / 2, y + bh, [
          [0, 0],
          [0, gap],
        ]),
      );
    }
  });

  // loop left
  const think = boxes[1];
  const done = boxes[3];
  const lx = cx - 70;
  els.push(
    arrow(
      done.x,
      done.y + done.h / 2,
      [
        [0, 0],
        [lx - done.x, 0],
        [lx - done.x, think.y + think.h / 2 - (done.y + done.h / 2)],
        [0, think.y + think.h / 2 - (done.y + done.h / 2)],
      ],
      C.orangeStroke,
    ),
  );
  els.push(noteText(lx - 70, (think.y + done.y) / 2 + 20, "未完成", 16, C.orangeStroke));

  // exit right
  const outX = cx + bw + 40;
  els.push(
    arrow(done.x + done.w, done.y + done.h / 2, [
      [0, 0],
      [40, 0],
    ], C.greenStroke),
  );
  els.push(
    ...labeledBox({
      x: outX,
      y: done.y,
      w: 180,
      h: bh,
      text: "输出 / 升级人工",
      fill: C.green,
      stroke: C.greenStroke,
      fontSize: 16,
    }).elements,
  );

  els.push(noteText(140, 520, "旁注：步数上限 · Token / 钱预算 · 人工确认点", 16));
  return save("01-agent-loop", els);
}

// ─── 02 when not ─────────────────────────────────────────────
function gen02() {
  const els = [];
  els.push(titleText(240, 24, "何时不上 Agent：快速否决清单", 26));
  els.push(noteText(160, 64, "否决核心不是模型够不够聪明，而是控制权该不该交给它", 16));

  const cards = [
    [C.red, C.redStroke, "路径写得清", "步骤固定、分支少", "→ Workflow / 规则"],
    [C.red, C.redStroke, "失败不可回滚", "付款、删库、合规", "→ 人工 / 强审批流"],
    [C.red, C.redStroke, "必须可复现", "审计、对账、法务", "→ 确定性编排"],
    [C.orange, C.orangeStroke, "延迟 / 成本极敏感", "毫秒级或极省钱", "→ 缓存 / 单次调用"],
    [C.orange, C.orangeStroke, "工具面太窄", "几乎只有聊天", "→ Chatbot 即可"],
    [C.orange, C.orangeStroke, "开放目标但无护栏", "无步数 / 预算 / 权限", "→ 先补约束再谈 Agent"],
  ];

  const cw = 280;
  const ch = 140;
  const gapX = 28;
  const gapY = 28;
  const left = 40;
  const top = 110;

  cards.forEach(([fill, stroke, title, sub, alt], i) => {
    const row = Math.floor(i / 3);
    const col = i % 3;
    const x = left + col * (cw + gapX);
    const y = top + row * (ch + gapY);
    els.push(...labeledBox({ x, y, w: cw, h: ch, text: `${title}\n${sub}\n${alt}`, fill, stroke, fontSize: 16 }).elements);
    const te = els[els.length - 1];
    te.height = 90;
    te.y = y + 25;
    te.fontSize = 16;
  });

  els.push(noteText(180, 480, "面试加分：举你亲手否决过的真实场景，而不是背清单", 16));
  return save("02-when-not", els);
}

// ─── 03 react vs plan ────────────────────────────────────────
function gen03() {
  const els = [];
  els.push(titleText(280, 24, "ReAct vs Plan-and-Execute", 28));
  els.push(noteText(200, 64, "一边是环，一边是两段式——别用同一张列表硬套", 16));

  // Left panel ReAct
  els.push(...labeledBox({ x: 40, y: 100, w: 420, h: 60, text: "ReAct · 边想边做 · 交错决策", fill: C.blue, stroke: C.blueStroke, fontSize: 18 }).elements);

  const cx = 250;
  const cy = 320;
  const R = 100;
  const nodes = [
    [cx, cy - R, "Thought 思考", C.blue, C.blueStroke],
    [cx + R, cy, "Action 调工具", C.teal, C.tealStroke],
    [cx, cy + R, "Observation", C.teal, C.tealStroke],
    [cx - R, cy, "继续 / 停止", C.violet, C.violetStroke],
  ];
  // ellipse ring
  els.push(
    base({
      id: uid("ring"),
      type: "ellipse",
      x: cx - R - 40,
      y: cy - R - 40,
      width: (R + 40) * 2,
      height: (R + 40) * 2,
      strokeColor: C.blueStroke,
      backgroundColor: "transparent",
      fillStyle: "solid",
      roundness: null,
    }),
  );
  for (const [x, y, t, fill, stroke] of nodes) {
    els.push(...labeledBox({ x: x - 70, y: y - 24, w: 140, h: 48, text: t, fill, stroke, fontSize: 14 }).elements);
  }
  els.push(noteText(cx - 20, cy - 8, "循环", 16, C.muted));
  els.push(noteText(100, 500, "适合：反馈密、计划易变", 16, C.blueStroke));

  // Right panel Plan
  const rx = 520;
  els.push(...labeledBox({ x: rx, y: 100, w: 420, h: 60, text: "Plan-and-Execute · 先计划再执行", fill: C.teal, stroke: C.tealStroke, fontSize: 18 }).elements);
  els.push(
    ...labeledBox({
      x: rx + 40,
      y: 190,
      w: 340,
      h: 100,
      text: "阶段 A · Plan\n产出完整计划（可人审）\n可用更强模型",
      fill: C.blue,
      stroke: C.blueStroke,
      fontSize: 16,
    }).elements,
  );
  els[els.length - 1].height = 70;
  els[els.length - 1].y = 205;

  els.push(
    arrow(rx + 210, 290, [
      [0, 0],
      [0, 30],
    ]),
  );

  els.push(
    ...labeledBox({
      x: rx + 40,
      y: 330,
      w: 340,
      h: 100,
      text: "阶段 B · Execute\n逐步执行 · 可换小模型\n偏差大 → 重规划",
      fill: C.teal,
      stroke: C.tealStroke,
      fontSize: 16,
    }).elements,
  );
  els[els.length - 1].height = 70;
  els[els.length - 1].y = 345;

  // replan
  els.push(
    arrow(
      rx + 380,
      380,
      [
        [0, 0],
        [40, 0],
        [40, -140],
        [0, -140],
      ],
      C.orangeStroke,
    ),
  );
  els.push(noteText(rx + 390, 300, "re-plan", 14, C.orangeStroke));
  els.push(noteText(rx + 60, 500, "适合：步骤长、要审计、可并行", 16, C.tealStroke));

  return save("03-react-vs-plan", els);
}

// ─── main ────────────────────────────────────────────────────
const files = [gen00(), gen01Boundary(), gen01Loop(), gen02(), gen03()];
const pngMap = {
  "00-module-map.excalidraw": "00-module-map.png",
  "01-boundary.excalidraw": "01-boundary.png",
  "01-agent-loop.excalidraw": "01-agent-loop.png",
  "02-when-not.excalidraw": "02-when-not.png",
  "03-react-vs-plan.excalidraw": "03-react-vs-plan.png",
};

for (const f of files) {
  const baseName = f.split("/").pop();
  exportPng(f, pngMap[baseName]);
}

console.log("\nDone. Open .excalidraw on https://excalidraw.com to edit.");
console.log("Summary:");
console.log("  00-module-map — architecture map, 12 modules");
console.log("  01-boundary — relationship/compare, 3 columns");
console.log("  01-agent-loop — flowchart with feedback loop");
console.log("  02-when-not — checklist cards, 6 veto cases");
console.log("  03-react-vs-plan — dual topology compare");
