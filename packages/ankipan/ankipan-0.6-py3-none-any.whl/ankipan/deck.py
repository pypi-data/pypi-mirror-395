from collections import OrderedDict, Counter
from pathlib import Path
from wcwidth import wcswidth
from typing import Iterable, Dict, Union, List
import logging
import math

from ankipan import Reader, File, Client, SourcePath
from ankipan.util import pad_clip

logger = logging.getLogger(__name__)

class Deck:
    def __init__(self,
                 learning_lang: str,
                 native_lang: str,
                 learning_collection_words: List[str],
                 known_collection_words: List[str],
                 ignoring_collection_words: Iterable,
                 example_sentence_fields: List[SourcePath] = None,
                 source_words: Dict[str, int] = None):
        self.learning_lang = learning_lang
        self.reader = Reader(learning_lang)
        self.source_words = Counter(source_words) if source_words else Counter()

        self.added_files = []
        self.learning_collection_words = learning_collection_words
        self.known_collection_words = known_collection_words
        self.ignoring_collection_words = ignoring_collection_words

        self.example_sentence_fields = example_sentence_fields
        self._lemma_percentiles_by_domain = None

        self.word_lemma_mapping = {}
        self._explicit_new_words = None

    def sort_word_by_average(self, items):
        a = self.lemma_percentiles_by_domain.get("Average", {})
        def key(w, a=a):
            try:
                x = float(a.get(w))
                if not math.isfinite(x):
                    raise ValueError
                return (0, x, w)  # valid score first; then numeric; then tie-breaker
            except (TypeError, ValueError):
                return (1, float('inf'), w)
        return sorted(items, key=key)

    def _select_lemmas(self, *, include=None, exclude=()):
        lemmas = set(self.source_words)
        if include is not None: lemmas &= set(include)
        if exclude:             lemmas -= set(exclude)
        return self.sort_word_by_average(lemmas)

    def _base_new_words(self):
        return self._select_lemmas(exclude = set(self.learning_collection_words) |
                                           set(self.known_collection_words) |
                                           set(self.ignoring_collection_words))

    @property
    def new_words(self):
        base = self._base_new_words()
        if self._explicit_new_words is None:
            return base
        explicit = self._explicit_new_words
        return [w for w in base if w in explicit]

    learning_words = property(lambda s: s._select_lemmas(include=s.learning_collection_words))
    known_words    = property(lambda s: s._select_lemmas(include=s.known_collection_words))
    ignoring_words = property(lambda s: s._select_lemmas(include=s.ignoring_collection_words))

    @property
    def lemma_percentiles_by_domain(self):
        if self._lemma_percentiles_by_domain is None:
            if self.example_sentence_fields:
                self._lemma_percentiles_by_domain = OrderedDict(Client.get_lemma_percentiles(self.learning_lang, self.example_sentence_fields, list(self.source_words.keys())))
            else:
                logger.warning(f'No example sentence source paths specified for deck, not comparing occurrence frequencies with other sources')
                self._lemma_percentiles_by_domain = OrderedDict()

            common = [word for word, count in self.source_words.most_common()]
            for word in self.source_words:
                self._lemma_percentiles_by_domain.setdefault('Current Deck', {})[word] = common.index(word) / len(self.source_words) if self.source_words[word] != 1 else None
            self._lemma_percentiles_by_domain.move_to_end('Current Deck', last=False)

            for word in self.source_words:
                percentile_values = [lemma_counts[word] for domain, lemma_counts in self._lemma_percentiles_by_domain.items() if lemma_counts.get(word) is not None]
                self._lemma_percentiles_by_domain.setdefault('Average', {})[word] = None if not percentile_values else (sum(percentile_values) / len(percentile_values))
            self._lemma_percentiles_by_domain.move_to_end('Average', last=False)

        return self._lemma_percentiles_by_domain

    def sorted_words(self, domain_name='Average'):
        items = self.lemma_percentiles_by_domain[domain_name].items()
        return [lemma for lemma, v in sorted(items, key=lambda kv: (kv[1] is None, kv[1]))]

    def set_new_words(self,
                      new_words: Iterable,
                      known_words: Iterable = None,
                      *,
                      words_to_consider: Iterable = None):
        if known_words is None:
            known_words = []
        new_words = set(new_words)
        known_words = list(known_words)
        known_words_set = set(known_words)
        if words_to_consider is None:
            words_iterable = list(self.source_words.keys())
            self._explicit_new_words = None
        else:
            words_iterable = list(words_to_consider)
            self._explicit_new_words = set(new_words)
        for word in words_iterable:
            if word in new_words:
                if word in self.known_collection_words:
                    self.known_collection_words.remove(word)
                if word in self.learning_collection_words:
                    self.learning_collection_words.remove(word)
            elif word in known_words_set and word not in self.known_collection_words:
                self.known_collection_words.append(word)
            elif word not in self.ignoring_collection_words:
                self.ignoring_collection_words.append(word)

    def __repr__(self):
        return str(self)

    def __str__(self):
        if not any([self.new_words, self.learning_words, self.known_words, self.ignoring_words]):
            return "No words in collection"

        titles = [
            f"New Words ({len(self.new_words)})",
            f"Learning Words ({len(self.learning_words)})",
            f"Known and ignoring Words ({len(self.known_words)} + {len(self.ignoring_words)})",
        ]

        deck_name = "Current Deck"
        deck_percentiles = self.lemma_percentiles_by_domain.get(deck_name, {})

        def order(word):
            v = deck_percentiles.get(word)
            return (v is None, v)

        def _truncate(words: list[str]) -> list[str]:
            if len(words) <= 100:
                return words
            omitted = len(words) - 100
            marker = f"... ({omitted} more omitted) ..."
            return list(words[:50]) + [marker] + list(words[-50:])

        columns = {
            titles[0]: _truncate(self.new_words),
            titles[1]: _truncate(self.learning_words),
            titles[2]: _truncate(list(set().union(self.known_words, self.ignoring_words))),
        }

        samples = ["100.00%", "  0.00%", "Only occurs once"]
        word_width = max(14, max((wcswidth(w) for w in self.source_words.keys()), default=12) + 2)
        pct_width  = max(10, wcswidth(deck_name) + 2, max(wcswidth(s) for s in samples) + 2)

        inner_gap = " "
        block_width = word_width + wcswidth(inner_gap) + pct_width
        outer_gap = " | "

        header = inner_gap.join([pad_clip("word", word_width), pad_clip(deck_name, pct_width)])
        title_line = outer_gap.join(pad_clip(t, block_width) for t in titles)

        lines = [
            title_line,
            "_" * wcswidth(title_line),
            outer_gap.join(pad_clip(header, block_width) for _ in titles),
            "",
        ]

        max_rows = max(len(words) for words in columns.values()) if columns else 0

        for i in range(max_rows):
            row_blocks = []
            for t in titles:
                words = columns[t]
                if i < len(words):
                    w = words[i]
                    v = deck_percentiles.get(w)
                    txt = "Only occurs once" if v is None else ("100.00%" if v == 1.0 else f"{v:.2%}")
                    block = inner_gap.join([pad_clip(w, word_width), pad_clip(txt, pct_width)])
                else:
                    block = ""
                row_blocks.append(pad_clip(block, block_width))
            lines.append(outer_gap.join(row_blocks))

        return "\n".join(lines)


    def add(self,
            path: Union[str, Path] = None,
            *,
            string: str = None,
            lemma_counts: Union[Dict[str, int], Counter] = None):
        """
        Add words from file(s) to word collection

        Parameters
        ----------
        path: path to file(s)
        string (optional): parse string instead of file, only valid if no file is specified

        """
        if path and string:
            raise RuntimeError('Please only supply either a path or a string.')
        elif lemma_counts is not None:
            if not (isinstance(lemma_counts, dict) or isinstance(words, Counter)):
                raise RuntimeError(f'Deck requires Dict- or Counter like datastructure to update, received {type(lemma_counts)}:\n  {lemma_counts}')
        if lemma_counts is not None:
            self.source_words.update(lemma_counts)
        else:
            if string is not None:
                files = [File(self.learning_lang, string,)]
            else:
                file_paths = self.reader.collect_file_paths(path)
                files = self.reader.open_files(file_paths)
            self.reader.process_files(files, save_sentence_mapping=True)
            for file in files:
                self.source_words.update(Counter(file.lemma_counts))
                self.word_lemma_mapping.update(file.processed_words)
                self.added_files.append(file)
        self._lemma_percentiles_by_domain = None
        self._explicit_new_words = None

    def remove_words(self, words: Union[str, Iterable]):
        """
        Remove words from word collection

        Parameters
        ----------
        words: words to remove

        """
        if isinstance(words, str):
            words = [words]
        elif not (isinstance(words, list) or isinstance(words, set)):
            raise RuntimeError('Only string or list allowed in collection.remove command')
        for word in words:
            if word not in self.source_words: raise RuntimeError(f'Word "{word}" is not part of this wordcollection, abort.')
        [self.source_words.pop(word) for word in words]

    def remove_range(self, lower: int, upper: int):
        self.remove([word for word, count in self.source_words.items() if count >= lower and count < upper])

    def select_new_words(
        self,
        n_words: int = 300,
        host: str = "127.0.0.1",
        port: int = 8760,
        open_browser: bool = True,
    ):
        import threading, time, webbrowser
        from flask import Flask, request, jsonify, render_template_string
        from werkzeug.serving import make_server

        try:
            if len(self.source_words) > n_words:
                logger.warning(f"Only rendering {n_words} of {len(self.source_words)}.")
        except Exception:
            pass

        domains = list(self.lemma_percentiles_by_domain.keys())

        known_collection = set(getattr(self, "known_collection_words", []) or [])
        known_set = set(known_collection)
        ignoring_set = set(getattr(self, "ignoring_collection_words", []))
        if not known_set and hasattr(self, "known_words"):
            known_set = set(self.known_words)
        if not ignoring_set and hasattr(self, "ignoring_words"):
            ignoring_set = set(self.ignoring_words)

        selectable_words = [w for w in self.sorted_words() if w not in known_collection]
        words_to_show = selectable_words[:n_words]

        rows = []
        for w in words_to_show:
            is_known = w in known_set
            is_skip  = (w in ignoring_set) and (not is_known)
            r = {"id": w, "Skip": is_skip, "Known": is_known, "Word": w}
            for d in domains:
                v = self.lemma_percentiles_by_domain.get(d, {}).get(w)
                r[d] = None if v is None else float(v)
            rows.append(r)
        app = Flask(__name__)
        html = r"""
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Select New Words</title>
    <link href="https://unpkg.com/tabulator-tables@5.6.0/dist/css/tabulator.min.css" rel="stylesheet">
    <style>
        body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 20px; }
        .controls { display:flex; gap:12px; align-items:center; margin-bottom:12px; flex-wrap:wrap; }
        .btn { padding:8px 12px; border:1px solid #444; border-radius:6px; background:#f5f5f5; cursor:pointer; }
        .btn[disabled] { opacity: 0.6; cursor: not-allowed; }
        .btn:hover { background:#eee; }
        #grid { border: 1px solid #ddd; }
        .tabulator-col .tabulator-col-title { white-space: normal !important; word-break: break-word; overflow-wrap: anywhere; line-height: 1.2; display: inline-block; width: 100%; }
        .chk { width: 18px; height: 18px; cursor: pointer; }
        #status { margin-top: 12px; padding: 10px 12px; border-radius: 8px; display:none; }
        #status.ok { display:block; background: #e8f7ec; border: 1px solid #2e7d32; color: #1b5e20; }
        #status.err { display:block; background: #fdecea; border: 1px solid #c62828; color: #8e0000; }
        #exit { display:none; margin-top:10px; }
    </style>
    </head>
    <body>
    <h2>Select New Words</h2>
    <div>Select words you already know, and erroneous/invalid words to skip (Shift-click to toggle ranges). <br>
        Entries that are not selected will be classified as new words to learn and will be added to the collection as flashcards.
        Numbers/colors reference frequency percentile for each example sentence source specified in the collection.</div>
    <div class="controls">
        <input id="quick" placeholder="Filter Word..." />
        <button id="apply" class="btn">Set unknown words</button>
        <button id="clear" class="btn">Clear selections</button>
        <span id="counts" style="color:#666"></span>
    </div>

    <div id="grid"></div>
    <div id="status" role="status" aria-live="polite"></div>
    <button id="exit" class="btn">Exit</button>

    <script src="https://unpkg.com/tabulator-tables@5.6.0/dist/js/tabulator.min.js"></script>
    <script>
        const ROWS    = {{ rows|tojson }};
        const DOMAINS = {{ domains|tojson }};

        let TABLE = null;
        let LAST_INDEX = {Skip: null, Known: null};

        function pctFormatter(cell){
        const v = cell.getValue();
        const el = cell.getElement();
        if (v === null || v === undefined) { el.style.backgroundColor = "#ffffff"; return ""; }
        if (v < 0.10)      el.style.backgroundColor = "#c6f7c6";
        else if (v < 0.25) el.style.backgroundColor = "#fff7b5";
        else               el.style.backgroundColor = "#f7c6c6";
        return Number(v).toFixed(4);
        }

        function checkboxFormatter(col){
        return function(cell){
            const wrap = document.createElement("div");
            wrap.style.display = "flex"; wrap.style.justifyContent = "center";
            const cb = document.createElement("input");
            cb.type = "checkbox"; cb.className = "chk"; cb.checked = !!cell.getValue();

            cb.addEventListener("click", (e) => {
            e.stopPropagation();
            const rows = TABLE.getRows("active");
            const clickedRow = cell.getRow();
            const idx = rows.indexOf(clickedRow);
            const newVal = cb.checked;

            const last = LAST_INDEX[col];
            if (e.shiftKey && last !== null){
                const start = Math.min(last, idx);
                const end   = Math.max(last, idx);
                for (let i=start; i<=end; i++){
                const r = rows[i]; const d = r.getData();
                if (d[col] !== newVal){ d[col] = newVal; r.update(d); }
                }
            } else {
                const d = clickedRow.getData(); d[col] = newVal; clickedRow.update(d);
            }
            LAST_INDEX[col] = idx;
            updateCounts();
            });

            wrap.appendChild(cb); return wrap;
        }
        }

        const columns = [
        { title:"Skip",  field:"Skip",  width:100, hozAlign:"center", headerHozAlign:"center", formatter: checkboxFormatter("Skip"),  headerSort:false },
        { title:"Known", field:"Known", width:100, hozAlign:"center", headerHozAlign:"center", formatter: checkboxFormatter("Known"), headerSort:false },
        { title:"Word",  field:"Word",  minWidth:220, headerHozAlign:"left", sorter:"string", headerFilter:"input", headerFilterPlaceholder:"type to filter..." },
        ];
        for (const d of DOMAINS){
        columns.push({ title:d, field:d, width:100, formatter:pctFormatter, headerSort:false, headerHozAlign:"center" });
        }

        const table = new Tabulator("#grid", {
            data: ROWS, layout:"fitDataStretch", height:"70vh",
            columns: columns, index:"id", pagination:false, movableColumns:true,
        });
        TABLE = table;

        document.getElementById("quick").addEventListener("input", (e) => {
        const q = e.target.value || "";
        if (!q){ table.clearFilter(true); } else { table.setFilter("Word", "like", q); }
        updateCounts();
        });

        function updateCounts(){
        const data = table.getData("active");
        let nSkip=0, nKnown=0; for (const r of data){ if(r.Skip) nSkip++; if(r.Known) nKnown++; }
        document.getElementById("counts").textContent = `Selected — Skip: ${nSkip}, Known: ${nKnown}`;
        }
        updateCounts();

        document.getElementById("clear").addEventListener("click", async () => {
        const all = table.getData(); all.forEach(r => { r.Skip=false; r.Known=false; });
        table.replaceData(all); updateCounts();
        try { await fetch("/log", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({action:"clear"}) }); } catch(e){}
        });

        document.getElementById("apply").addEventListener("click", async () => {
        const btnApply = document.getElementById("apply");
        const btnClear = document.getElementById("clear");
        const statusEl = document.getElementById("status");
        const btnExit  = document.getElementById("exit");
        btnApply.disabled = true; btnClear.disabled = true;

        const all = table.getData();
        const skip  = all.filter(r => !!r.Skip).map(r => r.Word);
        const known = all.filter(r => !!r.Known).map(r => r.Word);

        try{
            const res = await fetch("/apply", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({ skip, known }) });
            const js = await res.json();
            if (js.ok){
            statusEl.className = "ok";
            statusEl.textContent = `✅ Words set. Click 'Exit' to return to Python.  (skip: ${js.skip_n}, known: ${js.known_n}, new: ${js.new_n})`;
            btnExit.style.display = "inline-block";
            } else {
            statusEl.className = "err";
            statusEl.textContent = "❌ Something went wrong setting words. Check your Python console for details.";
            btnApply.disabled = false; btnClear.disabled = false;
            }
        } catch(e){
            statusEl.className = "err";
            statusEl.textContent = "❌ Network error. The words may not have been set. Check your Python console.";
            btnApply.disabled = false; btnClear.disabled = false;
        }
        });

        // Exit: ask server to shut down; then best-effort close tab/window
        document.getElementById("exit").addEventListener("click", async () => {
        const statusEl = document.getElementById("status");
        statusEl.className = "ok";
        statusEl.textContent = "👋 Exiting... You can close this tab if it doesn't close automatically.";
        try { await fetch("/exit", { method:"POST" }); } catch(e){}
        setTimeout(() => { try { window.close(); } catch(e){} }, 200);
        });
    </script>
    </body>
    </html>
    """

        @app.route("/")
        def index():
            return render_template_string(html, rows=rows, domains=domains)

        @app.post("/log")
        def log_action():
            payload = request.get_json(force=True) or {}
            print(f"[Tabulator] Button pressed: {payload.get('action')}")
            return jsonify({"ok": True})

        @app.post("/apply")
        def apply():
            payload = request.get_json(force=True) or {}
            skip_words = payload.get("skip", []) or []
            selected_known = payload.get("known", []) or []
            known_words = list(set(selected_known) | set(self.known_collection_words or []))
            words_on_screen = list(words_to_show)
            new_words = set(words_on_screen) - set(skip_words) - set(selected_known)
            self.set_new_words(new_words, known_words, words_to_consider=words_on_screen)
            print(f"[Tabulator] Apply pressed: skip={len(skip_words)}, known={len(selected_known)}, new={len(new_words)}")
            return jsonify({"ok": True, "skip_n": len(skip_words), "known_n": len(selected_known), "new_n": len(new_words)})

        @app.post("/exit")
        def exit_():
            print("[Tabulator] Exit pressed: shutting down server")
            def _shutdown():
                time.sleep(0.15)
                app.config["__server__"].shutdown()
            threading.Thread(target=_shutdown, daemon=True).start()
            return jsonify({"ok": True})

        srv = make_server(host, port, app)
        app.config["__server__"] = srv

        if open_browser:
            browser_host = "localhost" if host in ("0.0.0.0", "::") else host
            threading.Timer(0.5, lambda: webbrowser.open(f"http://{browser_host}:{port}/", new=1)).start()

        try:
            srv.serve_forever()
        finally:
            try:
                srv.server_close()
            except Exception:
                pass
