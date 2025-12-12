from flask import Flask, render_template, Response
from .analyzer import analyze_project, calc_chaos_score, calc_tech_karma, calc_future_regret_index
from .rendering import render_text_report, render_tree

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
def download():
    _, report, _, _ = get_stats()
    return Response(report, mimetype="text/plain")
