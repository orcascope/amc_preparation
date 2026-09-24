"use strict";

// ---------- small helpers ----------

const $app = document.getElementById("app");
const STUDENT_KEY = "amc.student";
const YEAR_KEY = "amc.year";
const AVATAR_COLORS = ["#5B3DF0", "#178A4C", "#E0457B", "#0E8F82", "#B25E00", "#C9338F"];
const TOPIC_ICONS = {
  algebra: "x²", geometry: "△", number_theory: "#", counting_probability: "n!", arithmetic_logic: "%",
};
const STATUS_TEXT = {
  solved_own: "Solved", solved_hints: "Hints", shown: "Shown", trying: "Trying", new: "",
};

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

// Markdown subset used by the worked solutions: paragraphs, line breaks, **bold**.
// Math ($...$ and $$...$$) is left in place for KaTeX auto-render.
function md(s) {
  return esc(s).split(/\n{2,}/).map((para) =>
    "<p>" + para.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\n/g, "<br>") + "</p>"
  ).join("");
}

function renderMath(el = $app) {
  if (!window.renderMathInElement) return;
  window.renderMathInElement(el, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false },
    ],
    throwOnError: false,
  });
}

function getStudent() {
  try { return JSON.parse(localStorage.getItem(STUDENT_KEY)); } catch { return null; }
}
function setStudent(s) {
  try { s ? localStorage.setItem(STUDENT_KEY, JSON.stringify(s)) : localStorage.removeItem(STUDENT_KEY); } catch { /* private mode */ }
}

// The year filter picked on the topics page. It also scopes problem lists,
// numbering and "Next problem", so it is kept while the student moves around.
function getYear() {
  try { return localStorage.getItem(YEAR_KEY); } catch { return null; }
}
function setYear(y) {
  try { y ? localStorage.setItem(YEAR_KEY, y) : localStorage.removeItem(YEAR_KEY); } catch { /* private mode */ }
}

async function api(path, { method = "GET", body, allYears = false } = {}) {
  const student = getStudent();
  const url = new URL(path, location.origin);
  if (student && method === "GET") url.searchParams.set("student", student.id);
  if (method === "GET" && !allYears && getYear()) url.searchParams.set("year", getYear());
  const res = await fetch(url, {
    method,
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify({ ...body, student: student?.id }) : undefined,
  });
  if (!res.ok) {
    if (res.status === 400 && (await res.text()).includes("unknown student")) {
      setStudent(null);
      location.hash = "#/";
    }
    throw new Error(`${method} ${path} failed: ${res.status}`);
  }
  return res.json();
}

function avatar(s, size = "") {
  const color = AVATAR_COLORS[(s.id - 1) % AVATAR_COLORS.length];
  return `<span class="avatar ${size}" style="background:${color}" aria-hidden="true">${esc(s.name[0].toUpperCase())}</span>`;
}

const ICON_BACK = `<svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M13 4 L7 10 L13 16"/></svg>`;
const ICON_NEXT = `<svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 4 L13 10 L7 16"/></svg>`;
const ICON_LOGO = `<svg width="24" height="24" viewBox="0 0 28 28" fill="none" stroke="#D93A63" stroke-width="2.2" aria-hidden="true"><path d="M4 22 L14 4 L24 22 Z"/><path d="M9 16 H19"/></svg>`;
const ICON_WARN = `<svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="9"/><path d="M11 6 V12"/><path d="M11 15.5 V16"/></svg>`;
const ICON_CHECK = `<svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><circle cx="11" cy="11" r="9"/><path d="M7 11.5 L10 14.5 L15.5 8"/></svg>`;

function topbar(crumbs = "") {
  const s = getStudent();
  return `<header class="topbar">
    ${crumbs ? `<nav class="crumbs" aria-label="Breadcrumb">${crumbs}</nav>`
             : `<a class="brand" href="#/topics">${ICON_LOGO}AMC 10 Practice</a><span style="flex:1"></span>`}
    <a class="who" href="#/" title="Switch student">${avatar(s)}<span class="name">${esc(s.name)} · Switch</span></a>
  </header>`;
}

function outcomeLabel(status, hints) {
  if (status === "solved_own") return "solved on your own";
  if (status === "solved_hints") return `solved with ${hints || "some"} hint${hints === 1 ? "" : "s"}`;
  if (status === "shown") return "answer shown";
  return "";
}

// ---------- screen: choose student ----------

async function showWelcome() {
  const { students, total } = await api("/api/students");
  $app.innerHTML = `<div class="welcome">
    <section class="hero">
      <svg class="shapes" viewBox="0 0 640 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
        <circle cx="560" cy="110" r="70" fill="#FFD84D"/>
        <rect x="470" y="600" width="120" height="120" rx="24" fill="#FF6B8B" transform="rotate(18 530 660)"/>
        <path d="M60 700 L130 580 L200 700 Z" fill="#2FD1B5"/>
        <text x="400" y="330" font-family="Times New Roman, serif" font-size="96" fill="#7E66F5">π</text>
        <text x="300" y="760" font-family="Times New Roman, serif" font-size="72" fill="#7E66F5">√</text>
        <text x="560" y="470" font-family="Times New Roman, serif" font-size="64" fill="#7E66F5">∑</text>
      </svg>
      <div class="brand" style="display:flex;align-items:center;gap:12px;font-weight:700;font-size:17px">${ICON_LOGO.replace("#D93A63", "#FFD84D")}AMC 10 Practice</div>
      <div>
        <h1>Real contest problems.<br><span>Help when you need it.</span></h1>
        <p>${total} real AMC 10 problems, grouped by type. Try each one yourself first. If you get stuck, ask for a hint or see the answer.</p>
      </div>
      <p style="font-size:15px;margin:0">Everyone on this computer can pick their own name, so each student keeps their own progress.</p>
    </section>
    <section class="pick">
      <h2>Who's practicing today?</h2>
      <div class="student-list">
        ${students.map((s) => `<button type="button" class="student" data-id="${s.id}" data-name="${esc(s.name)}">
          ${avatar(s, "lg")}
          <span style="flex:1;display:flex;flex-direction:column">
            <b style="font-size:18px">${esc(s.name)}</b>
            <span class="meta">${s.touched ? `${s.solved} of ${total} solved` : "New · nothing tried yet"}</span>
          </span>${ICON_NEXT}</button>`).join("")}
      </div>
      <form class="new-student">
        <label for="newname">${students.length ? "New here? Type your name" : "Type your name to start"}</label>
        <div class="row">
          <input id="newname" name="name" type="text" maxlength="40" autocomplete="off" placeholder="Your first name" required>
          <button class="btn btn-primary" type="submit">Start</button>
        </div>
        <p class="error" hidden></p>
      </form>
    </section>
  </div>`;

  $app.querySelectorAll(".student").forEach((b) => b.addEventListener("click", () => {
    setStudent({ id: Number(b.dataset.id), name: b.dataset.name });
    location.hash = "#/topics";
  }));
  $app.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = e.target.name.value.trim();
    if (!name) return;
    try {
      const s = await fetch("/api/students", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name }),
      }).then((r) => { if (!r.ok) throw new Error(); return r.json(); });
      setStudent(s);
      location.hash = "#/topics";
    } catch {
      const err = $app.querySelector(".error");
      err.textContent = "That name didn't work. Try 1 to 40 letters.";
      err.hidden = false;
    }
  });
}

// ---------- screen: topics dashboard ----------

async function showTopics() {
  const s = getStudent();
  const { topics, totals, resume, years = [], year = null } = await api("/api/topics");
  if (!year && getYear() && years.length) {  // the saved year has no problems any more
    setYear(null);
    location.replace("#/topics?year=all");
    return;
  }
  const solved = totals.solved_own + totals.solved_hints;
  const pct = (n, t) => `${(100 * n / t).toFixed(1)}%`;
  $app.innerHTML = topbar() + `<main class="page">
    <div class="dash-head">
      <div class="hello">
        <h1>${solved ? "Welcome back" : "Welcome"}, ${esc(s.name)}!</h1>
        <div class="stats">
          <span><b>${solved}</b>of ${totals.total} solved</span>
          <span class="own"><b>${totals.solved_own}</b>solved on your own</span>
          <span class="hints"><b>${totals.solved_hints}</b>solved with hints</span>
          <span><b>${totals.shown}</b>answers shown</span>
        </div>
      </div>
      ${resume ? `<a class="resume" href="#/p/${resume.id}">
        <span class="label">Pick up where you left off</span>
        <span class="title">${esc(resume.topic_name)} · Problem ${resume.number}</span>
        <span class="sub">${esc(resume.subtopic)} · ${resume.attempts} attempt${resume.attempts === 1 ? "" : "s"} so far</span>
      </a>` : ""}
    </div>
    ${years.length > 1 ? `<nav class="year-filter" aria-label="Filter by year">
      <span class="label">Year</span>
      ${[["all", "All years"], ...years.map((y) => [String(y), String(y)])].map(([v, label]) => {
        const on = v === (year ? String(year) : "all");
        return `<a class="chip ${on ? "on" : ""}" href="#/topics?year=${v}" ${on ? 'aria-current="true"' : ""}>${label}</a>`;
      }).join("")}
    </nav>` : ""}
    <h2 class="section-title">Choose a problem type${year ? ` <span class="year-note">· ${year} problems</span>` : ""}</h2>
    <div class="topic-grid">
      ${topics.map((t) => {
        const c = t.counts;
        const done = c.solved_own + c.solved_hints;
        return `<a class="topic t-${t.key}" href="#/topic/${t.key}">
          <div class="head">
            <span class="icon" aria-hidden="true">${TOPIC_ICONS[t.key]}</span>
            <div><div class="name">${esc(t.name)}</div><div class="count">${t.total} problem${t.total === 1 ? "" : "s"}</div></div>
          </div>
          <div class="sub">${t.subtopics.map(esc).join(", ")}</div>
          <div class="bar" role="img" aria-label="${done} solved, ${c.shown} shown, of ${t.total}">
            <span class="own" style="width:${pct(c.solved_own, t.total)}"></span>
            <span class="hints" style="width:${pct(c.solved_hints, t.total)}"></span>
            <span class="shown" style="width:${pct(c.shown, t.total)}"></span>
          </div>
          <div class="progress">${done} solved${c.trying ? ` · ${c.trying} in progress` : ""}</div>
        </a>`;
      }).join("")}
      <div class="legend">
        <div><i style="background:var(--green-bright)"></i>Solved on your own</div>
        <div><i style="background:var(--amber)"></i>Solved with hints</div>
        <div><i style="background:var(--shown)"></i>Answer shown</div>
      </div>
    </div>
  </main>`;
}

async function openTopic(key) {
  const t = await api(`/api/topics/${key}`);
  const next = t.problems.find((p) => p.status === "trying") || t.problems.find((p) => p.status === "new") || t.problems[0];
  location.replace(`#/p/${next.id}`);
}

// ---------- screen: problem ----------

function problemCrumbs(p, extra = "") {
  return `<a href="#/topics">${ICON_BACK}All topics</a><span class="sep">/</span>
    ${extra ? `<a href="#/p/${p.id}">${esc(p.topic_name)} · Problem ${p.number}</a><span class="sep">/</span><span>${extra}</span>`
            : `<span>${esc(p.topic_name)}</span>`}`;
}

function choicesHtml(p, { selected, disabled } = {}) {
  return `<fieldset class="choices">
    <legend>${disabled ? "Answer choices" : "Choose your answer"}</legend>
    ${Object.entries(p.choices).map(([letter, value]) => {
      let cls = "";
      if (p.answer && letter === p.answer.choice) cls = "right";
      else if (p.wrong_tried.includes(letter)) cls = "wrong";
      else if (letter === selected) cls = "selected";
      return `<label class="choice ${cls} ${disabled ? "disabled" : ""}">
        <input type="radio" name="ans" value="${letter}" ${letter === selected ? "checked" : ""} ${disabled ? "disabled" : ""}>
        <b>(${letter})</b><span>${esc(value)}</span></label>`;
    }).join("")}
  </fieldset>`;
}

async function showProblem(id) {
  const p = await api(`/api/problems/${id}`);
  let list = await api(`/api/topics/${p.topic}`);
  if (!list.problems.some((q) => q.id === p.id)) {  // opened from outside the year filter
    list = await api(`/api/topics/${p.topic}`, { allYears: true });
  }
  const state = { selected: null, feedback: null };

  function render() {
    const done = p.status !== "new" && p.status !== "trying";
    let feedback = "";
    if (state.feedback?.correct || (done && p.answer)) {
      const status = state.feedback?.status || p.status;
      feedback = `<div class="banner good">${ICON_CHECK}<div>
        <div class="celebrate">${state.feedback?.correct ? "Correct!" : "Completed"}</div>
        The answer is <b>(${p.answer.choice})</b> ${esc(p.answer.value)}. Saved as <b>${outcomeLabel(status, p.hints_used)}</b>.
      </div></div>
      <div class="actions">
        <a class="btn btn-outline" href="#/p/${p.id}/solution">See the full solution</a>
        ${p.next ? `<a class="btn btn-primary" href="#/p/${p.next}">Next problem ${ICON_NEXT}</a>`
                 : `<a class="btn btn-primary" href="#/topics">Back to all topics</a>`}
      </div>`;
    } else if (state.feedback) {
      feedback = `<div class="banner warn">${ICON_WARN}<div>
        <b>(${state.selected}) isn't right.</b><br>
        ${state.feedback.explanation ? esc(state.feedback.explanation) : "Try again, or pick a way to get help below."}
      </div></div>`;
    }
    const help = (state.feedback?.correct || done) ? "" : `<section>
      <h2 style="font-family:var(--body);font-size:16px;font-weight:700;margin-bottom:12px">${p.attempts ? "Stuck? Pick how much help you want:" : "Not sure where to start?"}</h2>
      <div class="help-grid">
        ${p.attempts ? `<button type="button" class="help" data-act="retry"><b>Try again</b><small>Choose another answer</small></button>` : ""}
        <a class="help primary" href="#/p/${p.id}/guide"><b>${p.hints_used ? "Back to my hints" : "Guide me step by step"}</b><small>${p.hints_used ? `${p.hints_used} of ${p.steps_total - 1} hints shown` : "Show one hint at a time"}</small></a>
        <a class="help" href="#/p/${p.id}/solution"><b>Show me the answer</b><small>Answer and full solution</small></a>
      </div></section>`;

    $app.innerHTML = topbar(problemCrumbs(p)) + `<div class="problem-layout">
      <nav class="plist" aria-label="Problems in ${esc(p.topic_name)}">
        <div class="cap">${list.problems.length} problems</div>
        ${list.problems.map((q) => `<a href="#/p/${q.id}" class="${q.id === p.id ? "current" : ""}" ${q.id === p.id ? 'aria-current="page"' : ""}>
          <span class="dot ${q.status}" aria-hidden="true"></span>
          <span class="lbl">${q.number} · ${esc(q.subtopic)}</span>
          <span class="st">${STATUS_TEXT[q.status]}</span></a>`).join("")}
      </nav>
      <main class="pmain">
        <div class="meta-row">
          <span class="topic-tag t-${p.topic}">${esc(p.topic_name)}</span>
          <span>Problem ${p.number} of ${p.of}</span><span>·</span><span>${esc(p.subtopic)}</span><span>·</span><span>${p.year}</span>
          ${p.attempts ? `<span>·</span><span>${p.attempts} attempt${p.attempts === 1 ? "" : "s"}</span>` : ""}
        </div>
        <div class="statement"><img src="${p.image}" alt="Problem statement: ${esc(p.text.replace(/\$/g, ""))}"></div>
        <form class="answer-form">
          ${choicesHtml(p, { selected: state.selected, disabled: state.feedback?.correct || done })}
          ${(state.feedback?.correct || done) ? "" : `<div class="actions" style="margin-top:16px">
            <button class="btn btn-primary" type="submit" ${state.selected ? "" : "disabled"}>Check my answer</button></div>`}
        </form>
        ${feedback}
        ${help}
      </main>
    </div>`;
    renderMath();
    wire();
  }

  function wire() {
    const form = $app.querySelector(".answer-form");
    form.querySelectorAll("input[name=ans]").forEach((r) => r.addEventListener("change", () => {
      state.selected = r.value;
      state.feedback = null;
      render();
      $app.querySelector(`input[value=${r.value}]`).focus();
    }));
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!state.selected) return;
      const res = await api(`/api/problems/${p.id}/attempt`, { method: "POST", body: { choice: state.selected } });
      p.attempts += 1;
      state.feedback = res;
      if (res.correct) {
        p.answer = res.answer;
        p.status = res.status;
      } else if (!p.wrong_tried.includes(state.selected)) {
        p.wrong_tried.push(state.selected);
      }
      render();
      $app.querySelector(".banner")?.scrollIntoView({ behavior: "smooth", block: "center" });
    });
    $app.querySelector("[data-act=retry]")?.addEventListener("click", () => {
      state.selected = null;
      state.feedback = null;
      render();
      $app.querySelector(".choices input:not(:disabled)")?.focus();
    });
  }

  render();
}

// ---------- screen: guided steps ----------

function stepHtml(step, i, { current, showTurnAnswer } = {}) {
  const turn = step.your_turn;
  return `<section class="step ${current ? "current" : ""}">
    <span class="num" aria-hidden="true">${i}</span>
    <div class="content">
      <h2><span class="sr-only">Step ${i}: </span>${esc(step.title)}</h2>
      <div class="body">${md(step.body)}</div>
      ${turn ? `<div class="yourturn">
        <div><b>Your turn:</b> ${esc(turn.prompt)}</div>
        ${showTurnAnswer ? `<div class="answer"><b>Answer:</b> ${esc(turn.answer)}</div>` : `<div class="row">
          <label class="sr-only" for="yt${i}">Your idea for step ${i}</label>
          <textarea id="yt${i}" rows="1" placeholder="Work it out, then type your idea (optional)"></textarea>
          <button type="button" class="reveal" data-step="${i}">Show answer</button>
        </div>
        <div class="answer" data-answer="${i}" hidden><b>Answer:</b> ${esc(turn.answer)}</div>`}
      </div>` : ""}
    </div>
  </section>`;
}

function problemAside(p, tip) {
  return `<aside>
    <div class="card problem-card"><div class="cap">The problem</div><img src="${p.image}" alt="Problem statement: ${esc(p.text.replace(/\$/g, ""))}"></div>
    ${tip ? `<div class="tip">${tip}</div>` : ""}
  </aside>`;
}

async function showGuide(id) {
  const p = await api(`/api/problems/${id}`);
  let data = await api(`/api/problems/${id}/steps?upto=${Math.max(1, p.hints_used)}`);

  function render() {
    const shown = data.steps.length;
    const total = data.total;
    const lockedFrom = shown + 1;
    $app.innerHTML = topbar(problemCrumbs(p, "Guided solution")) + `<div class="two-col">
      ${problemAside(p, "Each step shows one idea. Stop whenever you see what to do next, then go back and choose your answer.")}
      <main>
        <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
          <h1 style="font-size:26px;flex:1">Let's work through it</h1>
          <span style="color:var(--muted);font-size:14px">Step ${shown} of ${total}</span>
          <div class="progress-pips" aria-hidden="true">${Array.from({ length: total }, (_, i) => `<span class="${i < shown ? "on" : ""}"></span>`).join("")}</div>
        </div>
        ${data.steps.map((s, i) => stepHtml(s, i + 1, { current: i === shown - 1 })).join("")}
        ${Array.from({ length: total - shown }, (_, k) => {
          const n = lockedFrom + k;
          return `<div class="locked"><span class="num" aria-hidden="true">${n}</span>${n === total ? "Final step: the answer · hidden until you ask" : `Step ${n} · hidden until you ask`}</div>`;
        }).join("")}
        <div class="bottom-bar">
          ${shown < total - 1
            ? `<button type="button" class="btn btn-primary" data-act="next">Show step ${shown + 1}</button>`
            : `<a class="btn btn-primary" href="#/p/${p.id}/solution">Show the final step</a>`}
          <a class="btn btn-outline-green" href="#/p/${p.id}">I can finish it myself</a>
          <span class="spacer"></span>
          <a class="btn-link" href="#/p/${p.id}/solution">Show the full solution</a>
        </div>
      </main>
    </div>`;
    renderMath();
    $app.querySelectorAll(".reveal").forEach((b) => b.addEventListener("click", () => {
      const ans = $app.querySelector(`[data-answer="${b.dataset.step}"]`);
      ans.hidden = false;
      b.remove();
    }));
    $app.querySelector("[data-act=next]")?.addEventListener("click", async () => {
      data = await api(`/api/problems/${id}/steps?upto=${shown + 1}`);
      p.hints_used = Math.max(p.hints_used, shown + 1);
      render();
      $app.querySelector(".step.current")?.scrollIntoView({ behavior: "smooth", block: "start" });
      $app.querySelector(".step.current h2")?.setAttribute("tabindex", "-1");
      $app.querySelector(".step.current h2")?.focus({ preventScroll: true });
    });
  }

  render();
}

// ---------- screen: full solution + progress ----------

async function showSolution(id) {
  const p = await api(`/api/problems/${id}`);
  const data = await api(`/api/problems/${id}/steps?upto=all`);
  const done = p.status !== "new" && p.status !== "trying";
  let chosen = done ? p.status : "shown";

  function render(saved = false) {
    const outcomes = [
      ["solved_own", "I solved it on my own", "var(--green-bright)"],
      ["solved_hints", `I solved it after ${p.hints_used || "some"} hint${p.hints_used === 1 ? "" : "s"}`, "var(--amber)"],
      ["shown", "I needed the full solution", "var(--shown)"],
    ];
    $app.innerHTML = topbar(problemCrumbs(p, "Full solution")) + `<div class="two-col">
      <main>
        <div class="answer-card">
          <span class="label">Answer</span>
          <span class="value">(${data.answer.choice}) ${esc(data.answer.value)}</span>
        </div>
        ${data.steps.map((s, i) => stepHtml(s, i + 1, { showTurnAnswer: true })).join("")}
        <p class="done-note">These steps were worked out ahead of time with the math-olympiad solver and checked against the official answer key.</p>
      </main>
      <aside>
        <div class="card" style="display:flex;flex-direction:column;gap:16px">
          <h2 style="font-size:22px">Save your progress</h2>
          <fieldset class="outcomes">
            <legend>How did this one go?</legend>
            ${outcomes.map(([v, label, color]) => `<label class="outcome">
              <input type="radio" name="outcome" value="${v}" ${v === chosen ? "checked" : ""}>
              <i style="background:${color}" aria-hidden="true"></i>${label}</label>`).join("")}
          </fieldset>
          ${saved ? `<div class="banner good" style="padding:10px 14px">${ICON_CHECK}<span>Saved as <b>${outcomeLabel(chosen, p.hints_used)}</b>.</span></div>` : ""}
          <button type="button" class="btn btn-success" data-act="complete">${done || saved ? "Update" : "Mark as completed"}</button>
          <a class="btn btn-outline" href="#/topics">Save for later</a>
        </div>
        ${p.next ? `<a class="next-link" href="#/p/${p.next}"><span class="label">Up next in ${esc(p.topic_name)}</span>
          <b style="font-size:16px">Problem ${p.number + 1}</b></a>` : ""}
        <div class="card problem-card"><div class="cap">The problem</div><img src="${p.image}" alt="Problem statement: ${esc(p.text.replace(/\$/g, ""))}"></div>
      </aside>
    </div>`;
    renderMath();
    $app.querySelectorAll("input[name=outcome]").forEach((r) => r.addEventListener("change", () => { chosen = r.value; }));
    $app.querySelector("[data-act=complete]").addEventListener("click", async () => {
      await api(`/api/problems/${id}/complete`, { method: "POST", body: { outcome: chosen } });
      p.status = chosen;
      render(true);
    });
  }

  render();
}

// ---------- router ----------

async function route() {
  const hash = location.hash || "#/";
  const student = getStudent();
  if (!student && hash !== "#/") {
    location.replace("#/");
    return;
  }
  const [path, query = ""] = hash.slice(2).split("?");
  const parts = path.split("/");
  if (parts[0] === "topics") {
    const year = new URLSearchParams(query).get("year");
    if (year) setYear(year === "all" ? null : year);
    else if (getYear()) {  // keep the link in step with the saved filter
      location.replace(`#/topics?year=${getYear()}`);
      return;
    }
  }
  try {
    if (hash === "#/") await showWelcome();
    else if (parts[0] === "topics") await showTopics();
    else if (parts[0] === "topic") await openTopic(parts[1]);
    else if (parts[0] === "p" && parts[2] === "guide") await showGuide(parts[1]);
    else if (parts[0] === "p" && parts[2] === "solution") await showSolution(parts[1]);
    else if (parts[0] === "p") await showProblem(parts[1]);
    else location.replace("#/topics");
    window.scrollTo(0, 0);
  } catch (err) {
    console.error(err);
    $app.innerHTML = `<main class="page"><h1>Something went wrong</h1><p>${esc(err.message)}</p><p><a href="#/topics">Back to topics</a></p></main>`;
  }
}

window.addEventListener("hashchange", route);
window.addEventListener("DOMContentLoaded", route);
