# DIAGNOSE/project_diagnose/rendering.py

from .analyzer import (
    format_stats,
    format_ai_analysis,
    format_future_analysis,
)

def render_tree(stats):
    return "# ===== Структура проекта =====\n" + stats.get("tree", "")


def render_text_report(stats):
    blocks = []
    blocks.append(format_stats(stats))
    blocks.append(format_ai_analysis(stats))
    blocks.append(format_future_analysis(stats))
    return "\n".join(blocks)
