import os
import json
from flask import Flask, render_template, Response, request, jsonify

from .analyzer import (
    analyze_project,
    calc_chaos_score,
    calc_tech_karma,
    calc_future_regret_index,
    USER_CFG_PATH,
    build_tree_json,
    collect_files,
)
from .rendering import render_text_report, render_tree
from .config_schema import DiagnoseConfig

app = Flask(__name__, template_folder="templates", static_folder="static")

_stats_cache = None
_report_cache = None
_tree_cache = None
_metrics_cache = None


def compute_metrics(stats):
    return {
        "chaos": calc_chaos_score(stats),
        "tech_karma": calc_tech_karma(stats),
        "future_regret": calc_future_regret_index(stats),
        "ext_lines": stats.get("ext_lines", {}),
        "total_size": stats.get("total_size", 0),
    }


def get_stats():
    global _stats_cache, _report_cache, _tree_cache, _metrics_cache
    if _stats_cache is None:
        stats = analyze_project()
        _stats_cache = stats
        _report_cache = render_text_report(stats)
        _tree_cache = render_tree(stats)
        _metrics_cache = compute_metrics(stats)
    return _stats_cache, _report_cache, _tree_cache, _metrics_cache


@app.route("/")
def index():
    _, report, tree, metrics = get_stats()
    return render_template("index.html", report=report, tree=tree, metrics=metrics)


@app.route("/report.txt")
def download_txt():
    _, report, _, _ = get_stats()
    return Response(report, mimetype="text/plain")


# ===================== SETTINGS =====================

def load_config_for_ui():
    if os.path.exists(USER_CFG_PATH):
        try:
            with open(USER_CFG_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
            cfg = DiagnoseConfig(**raw)
            return cfg.model_dump()
        except Exception:
            return DiagnoseConfig().model_dump()
    return DiagnoseConfig().model_dump()


@app.route("/settings")
def settings():
    cfg = load_config_for_ui()
    tree = build_tree_json()
    return render_template("settings.html", config=cfg, tree=tree)


@app.route("/save_settings", methods=["POST"])
def save_settings():
    data = request.json
    cfg_obj = data.get("config")

    try:
        cfg = DiagnoseConfig(**cfg_obj)
        with open(USER_CFG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg.model_dump(), f, indent=4, ensure_ascii=False)

        global _stats_cache, _report_cache, _tree_cache, _metrics_cache
        _stats_cache = _report_cache = _tree_cache = _metrics_cache = None

        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# ===================== DUMP =====================

@app.route("/dump")
def dump_project():
    files = collect_files()
    buffer = []

    for path in files:
        rel = os.path.relpath(path, os.getcwd())
        buffer.append(f"# -------- {rel}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                buffer.append(f.read())
        except Exception as e:
            buffer.append(f"<<Error reading file: {e}>>")
        buffer.append("\n")

    out = "\n".join(buffer)

    return Response(
        out,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=project_dump.txt"}
    )


def run_web():
    print("Web-интерфейс запущен: http://127.0.0.1:5000")
    app.run(debug=False)
