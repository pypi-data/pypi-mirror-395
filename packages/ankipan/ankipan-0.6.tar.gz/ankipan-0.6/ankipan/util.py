from pathlib import Path
import json
from wcwidth import wcswidth

from typing import Any
from typing import Callable, List, Tuple, Optional, Dict, Iterable

from ankipan import DEFAULT_SERVER

def load_json(path: Path) -> dict[str, Any]:
    if path.exists():
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    else:
        return {}

def save_json(path: Path, obj: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)

def pad_clip(s, width):
    s = "" if s is None else str(s)
    if wcswidth(s) <= width:
        return s + " " * (width - wcswidth(s))
    ell = "…"; keep=[]; acc=0; tgt=max(1, width - wcswidth(ell))
    for ch in s:
        cw = wcswidth(ch)
        if acc + cw > tgt: break
        keep.append(ch); acc += cw
    return "".join(keep) + ell

def estimate_known_words(
    available_example_sentence_sources,
    known_words,
    source_path: Optional[str] = None,
    max_questions: int = 10,
    conservatism: float = 0.95,
    top_n: int = 300,
    host: str = "127.0.0.1",
    port: int = 8762,
    open_browser: bool = True,
):
    import threading, time, webbrowser
    from collections import Counter
    import numpy as np
    from flask import Flask, jsonify, render_template_string, request
    from werkzeug.serving import make_server

    lemma_counts = Counter()

    def accumulate_root(root_name: str):
        root = available_example_sentence_sources(root_name)
        for child in getattr(root, "children", {}).keys():
            node = available_example_sentence_sources(f"{root_name}/{child}")
            if getattr(node, "lemma_counts", None):
                lemma_counts.update(node.lemma_counts or {})

    if not source_path:
        roots = list(getattr(available_example_sentence_sources, "keys", lambda: [])())
        if not roots and DEFAULT_SERVER:
            roots = [DEFAULT_SERVER]
        for root_name in roots:
            accumulate_root(root_name)
    else:
        parts = source_path.split("/")
        if len(parts) == 1:
            accumulate_root(source_path)
        else:
            node = available_example_sentence_sources(source_path)
            lemma_counts = Counter(getattr(node, "lemma_counts", {}) or {})
            if not lemma_counts:
                print(f'lemma_counts empty for "{source_path}"')

    top = Counter(lemma_counts).most_common(max(1, top_n))
    known_set = set(known_words or [])
    words = [w for w, _ in top if w not in known_set]
    if not words:
        raise RuntimeError("No lemmas available to probe.")
    freqs = [lemma_counts[w] for w in words]
    sorted_idx = np.argsort(freqs)[::-1]
    sorted_words = [words[i] for i in sorted_idx]
    n_words = len(sorted_words)

    s = {
        "q": 0,
        "max_q": int(max_questions),
        "spread": 0.15,
        "max_known": 0.0,
        "min_unknown": 1.0,
        "cur_pos": None,
        "cur_word": None,
        "done": False,
        "conserv_margin": max(0.02, min(0.25, conservatism * 0.12)),
    }
    rng = np.random.default_rng()
    estimated_words = []
    session_set = set()
    # Track explicit user answers during probing
    stage1_known_yes = set()
    stage1_known_no = set()

    def select_next_word():
        mid = (s["max_known"] + s["min_unknown"]) / 2
        low = max(0.0, mid - s["spread"])
        high = min(1.0, mid + s["spread"])
        pos = rng.uniform(max(0.0, low * 0.7), low) if rng.random() < 0.2 else rng.uniform(low, high)
        idx = max(0, min(int(pos * n_words), n_words - 1))
        bin_size = max(1, n_words // 50)
        start = max(0, idx - bin_size // 2)
        end = min(n_words, start + bin_size)
        j = rng.integers(start, end)
        return sorted_words[j], j / n_words

    def finalize_stage1():
        nonlocal estimated_words, session_set
        if s["min_unknown"] < 1.0 and s["max_known"] > 0.0:
            gap = max(0.0, s["min_unknown"] - s["max_known"])
            theta = s["max_known"] - s["conserv_margin"] * gap
        elif s["min_unknown"] < 1.0:
            theta = s["min_unknown"] - s["conserv_margin"]
        elif s["max_known"] > 0.0:
            theta = s["max_known"] - 0.5 * s["conserv_margin"]
        else:
            theta = 0.0
        theta = max(0.0, min(1.0, theta))
        # Apply conservative downward adjustment: reduce estimated fraction by ~1/3.
        theta_adjusted = max(0.0, min(1.0, theta * (2.0 / 3.0)))
        num_known = int(theta_adjusted * n_words)
        base = set(sorted_words[:num_known])
        base.update(stage1_known_yes)
        base.difference_update(stage1_known_no)
        rank = {w: i for i, w in enumerate(sorted_words)}
        estimated_words = sorted(base, key=lambda w: rank.get(w, len(sorted_words)))
        session_set = set(estimated_words)

    app = Flask(__name__)

    PAGE_HTML = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Estimate Known Words</title>
<style>
:root { --fs: 17px; }
body { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
        font-size: var(--fs); line-height:1.45; margin:24px; color:#111; }
.wrap { max-width: 1100px; }
.controls { margin-top:12px; display:flex; gap:10px; flex-wrap:wrap; }
button { padding:8px 12px; }
#word { font-size:22px; font-weight:600; }
#meta { color:#666; margin-top:6px; }
/* Stage 2 */
.bar { display:flex; gap:10px; align-items:center; margin-bottom:10px; flex-wrap:wrap; }
.btn { padding:8px 12px; border:1px solid #444; border-radius:8px; background:#f7f7f7; cursor:pointer; }
.btn:hover { background:#eee; }
#count { color:#555; font-weight:600; margin-left:auto; }
#status {
  position: sticky;
  top: 0;
  z-index: 10;
  margin-bottom: 12px;       /* was margin-top */
  padding: 10px 12px;
  border-radius: 8px;
  display: none;
}
#status.ok  { display:block; background:#e8f7ec; border:1px solid #2e7d32; color:#1b5e20; }
#status.err { display:block; background:#fdecea; border:1px solid #c62828; color:#8e0000; }#exit { display:none; }
#grid { display:grid; grid-template-columns: repeat(5, minmax(0, 500px)); gap:8px 16px; align-content:start; justify-content:start; }
label { white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.chk { width:18px; height:18px; margin-right:8px; }
#stage1 { display:block; }
#stage2 { display:none; }
</style>
</head>
<body>
<div class="wrap">
<!-- Stage 1 -->
<section id="stage1">
    <h2>Known word estimation</h2>
    <p>
      This is a small interactive program to estimate the words you already know.
      We sample lemmas (root forms of words) from the example sentences in our <a href="https://gitlab.com/ankipan/ankipan_db" target="_blank">Database</a> and sort them by frequency.
      You are then shown individual words at different frequency levels. Based on your answers, we estimate a boundary between
      lemmas you probably know or don't know yet. You can see and refine the final estimate of your known words at the end.
    </p>

    <details>
      <summary>How this estimate works</summary>
      <ul>
        <li>
          We assume that on average, words that occur more frequently in our example sentence corpora are more likely to be known than rare words.
        </li>
        <li>
          Your "I know it / I don't know it" answers move the boundary between "known" and "unknown" along this frequency-sorted list.
        </li>
        <li>
          To stay conservative, we further down-regulate the estimate to avoid false positives as much as possible.
        </li>
      </ul>
    </details>

    <div id="word">…</div>
    <div id="meta">…</div>
    <div class="controls">
      <button id="yes">I know it</button>
      <button id="no">I don't know it</button>
      <button id="fin">Finish now</button>
    </div>
</section>

<!-- Stage 2 -->
<section id="stage2">
  <div id="status" role="status" aria-live="polite"></div>
  <div class="bar">
    <button id="save" class="btn">Save</button>
    <button id="exit" class="btn" style="display:none">Exit</button>
    <span id="count"></span>
  </div>
  <div id="grid"></div>
  <div class="bar" style="margin-top:16px;">
    <button id="save-bottom" class="btn">Save</button>
    <button id="exit-bottom" class="btn" style="display:none">Exit</button>
    <span id="count-bottom"></span>
  </div>
</section>
</div>

<script>
// ------- Stage 1: Query words for percentile estimate -------
async function initStage1(){
    const r = await fetch('/init'); const j = await r.json();
    if (j.done){ return enterStage2(); }
    renderProbe(j);
}
function renderProbe(j){
    document.getElementById('word').textContent = j.word;
    document.getElementById('meta').textContent = 'Rank ~ ' + Math.round(j.rank_pct) + '%  |  ' + j.q + '/' + j.max_q + ' answered';
}
async function answer(val){
    const r = await fetch('/answer', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({known: val})});
    const j = await r.json();
    if (j.done){ return enterStage2(); }
    renderProbe(j);
}
async function finishNow(){
    await fetch('/finish', {method:'POST'});
    return enterStage2();
}

document.getElementById('yes').addEventListener('click', () => answer(true));
document.getElementById('no').addEventListener('click', () => answer(false));
document.getElementById('fin').addEventListener('click', finishNow);

// ------- Stage 2: Provide overview of likely known words -------
async function enterStage2(){
    const r = await fetch('/stage2_words'); const j = await r.json();
    const words = j.words || [];

    // build grid
    const grid = document.getElementById('grid');
    grid.innerHTML = '';
    function makeRow(w){
      const lab = document.createElement('label');
      const cb = document.createElement('input');
      cb.type = 'checkbox'; cb.className = 'chk'; cb.value = w; cb.checked = true;
      lab.appendChild(cb); lab.appendChild(document.createTextNode(' ' + w));
      return lab;
    }
    words.forEach(w => grid.appendChild(makeRow(w)));

    function boxes(){ return Array.from(document.querySelectorAll('input.chk')); }
    function updateCount(){
      const b = boxes(); const sel = b.filter(x => x.checked).length;
      const msg = 'Selected ' + sel + ' / ' + b.length + ' known words to add to collection (shift-click to select or deselect ranges)';
      const elTop = document.getElementById('count');
      const elBottom = document.getElementById('count-bottom');
      if (elTop) elTop.textContent = msg;
      if (elBottom) elBottom.textContent = msg;
    }
    grid.addEventListener('change', updateCount);
    const lastByCol = new Map(); // colIndex -> last clicked checkbox index in that column

    grid.addEventListener('click', (e) => {
    const target = e.target;
    if (!(target instanceof HTMLInputElement) || !target.classList.contains('chk')) return;

    // Current checkbox index in DOM order
    const all = boxes();
    const idx = all.indexOf(target);
    if (idx === -1) return;
    const cols = getComputedStyle(grid).gridTemplateColumns.split(' ').length || 5; // fallback 5
    const col = idx % cols;

    if (e.shiftKey && lastByCol.has(col)) {
        // Range select within the same column
        const last = lastByCol.get(col);
        // Only act if last click was in the same column
        if (last % cols === col) {
        const [lo, hi] = idx < last ? [idx, last] : [last, idx];
        const rowLo = Math.floor(lo / cols);
        const rowHi = Math.floor(hi / cols);
        const val = target.checked; // apply target's new state to the whole column segment

        for (let r = rowLo; r <= rowHi; r++) {
            const i = r * cols + col;
            if (all[i]) all[i].checked = val;
        }
        updateCount();
        }
    }

    // Remember last click position per column
    lastByCol.set(col, idx);
    });
    updateCount();

    async function handleSave(){
    const statusEl = document.getElementById('status');
    const btn = document.getElementById('save');
    const btnBottom = document.getElementById('save-bottom');
    const exitBtn = document.getElementById('exit');
    const exitBtnBottom = document.getElementById('exit-bottom');
    const selected = boxes().filter(x => x.checked).map(x => x.value);
    const oldLabel = btn ? btn.textContent : 'Save';
    const oldLabelBottom = btnBottom ? btnBottom.textContent : oldLabel;
    if (btn) { btn.disabled = true; btn.textContent = 'Saving…'; }
    if (btnBottom) { btnBottom.disabled = true; btnBottom.textContent = 'Saving…'; }

    try {
        const res = await fetch('/apply', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ selected })
        });
        const js = await res.json();

        if (js && js.ok){
        statusEl.className = 'ok';
        statusEl.textContent =
            '✅ Words set. (selected: ' + (js.selected_n||0) +
            ', size: ' + (js.before||0) + ' → ' + (js.after||0) + ')';
        if (exitBtn) exitBtn.style.display = 'inline-block';
        if (exitBtnBottom) exitBtnBottom.style.display = 'inline-block';
        } else {
        statusEl.className = 'err';
        statusEl.textContent = '❌ Error applying selection.';
        }
        statusEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch(e){
        statusEl.className = 'err';
        statusEl.textContent = '❌ Network error.';
    } finally {
        if (btn) { btn.disabled = false; btn.textContent = oldLabel; }
        if (btnBottom) { btnBottom.disabled = false; btnBottom.textContent = oldLabelBottom; }
    }
    }
    document.getElementById('save').onclick = handleSave;
    document.getElementById('save-bottom').onclick = handleSave;
    document.getElementById('exit').onclick = async function(){
      const statusEl = document.getElementById('status');
      statusEl.className = 'ok';
      statusEl.textContent = "👋 Exiting... You can close this tab if it doesn't close automatically.";
      try { await fetch('/exit', { method:'POST' }); } catch(e){}
      setTimeout(() => { try { window.close(); } catch(e){} }, 200);
    };
    document.getElementById('exit-bottom').onclick = document.getElementById('exit').onclick;
    document.getElementById('stage1').style.display = 'none';
    document.getElementById('stage2').style.display = 'block';
}

// boot stage 1
initStage1();
</script>
</body>
</html>"""

    # --- routes ---
    @app.get("/")
    def page():
        return render_template_string(PAGE_HTML)

    @app.get("/init")
    def init_():
        if s["done"]:
            return jsonify({"done": True})
        w1, p1 = select_next_word()
        s["cur_word"], s["cur_pos"] = w1, p1
        return jsonify({"done": False, "word": w1, "rank_pct": p1 * 100.0, "q": s["q"], "max_q": s["max_q"]})

    @app.post("/answer")
    def answer_():
        if s["done"]:
            return jsonify({"done": True})
        payload = request.get_json(force=True) or {}
        known = bool(payload.get("known"))
        pos = s["cur_pos"]
        cur_word = s["cur_word"]
        if cur_word:
            if known:
                stage1_known_yes.add(cur_word)
                stage1_known_no.discard(cur_word)
            else:
                stage1_known_no.add(cur_word)
                stage1_known_yes.discard(cur_word)
        if pos is not None:
            if known: s["max_known"] = max(s["max_known"], pos)
            else:     s["min_unknown"] = min(s["min_unknown"], pos)
        s["q"] += 1
        s["spread"] = max(0.05, s["spread"] * 0.95)
        if s["q"] >= s["max_q"]:
            s["done"] = True
            finalize_stage1()
            return jsonify({"done": True})
        w1, p1 = select_next_word()
        s["cur_word"], s["cur_pos"] = w1, p1
        return jsonify({"done": False, "word": w1, "rank_pct": p1 * 100.0, "q": s["q"], "max_q": s["max_q"]})

    @app.post("/finish")
    def finish_():
        if not s["done"]:
            s["done"] = True
            finalize_stage1()
        return jsonify({"done": True})

    @app.get("/stage2_words")
    def stage2_words():
        return jsonify({"words": list(estimated_words)})

    @app.post("/apply")
    def apply_():
        payload = request.get_json(force=True) or {}
        selected = set(payload.get("selected", []))
        before = len(known_words)

        # mutate in place
        known_words.extend(selected)

        after = len(known_words)
        return jsonify({"ok": True, "selected_n": len(selected), "before": before, "after": after})

    @app.post("/exit")
    def exit_():
        print("[KnownWords] Exit pressed: shutting down server")
        def _shutdown():
            time.sleep(0.15)
            app.config["__server__"].shutdown()
        threading.Thread(target=_shutdown, daemon=True).start()
        return jsonify({"ok": True})

    # ---- run with explicit server handle so we can shutdown cleanly ----
    srv = make_server(host, port, app)
    app.config["__server__"] = srv
    actual_port = srv.socket.getsockname()[1]

    if open_browser:
        browser_host = "localhost" if host in ("0.0.0.0", "::") else host
        threading.Timer(0.5, lambda: webbrowser.open(f"http://{browser_host}:{actual_port}/", new=1)).start()

    try:
        srv.serve_forever()
    finally:
        try:
            srv.server_close()
        except Exception:
            pass

    return actual_port
