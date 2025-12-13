# DIAGNOSE/project_diagnose/cli.py

import argparse
from .analyzer import analyze_project, dump_project
from .rendering import render_text_report, render_tree
from .web import run_web

def main():
    parser = argparse.ArgumentParser(description="Диагностика проекта")

    parser.add_argument(
        "command",
        choices=["analyze", "report", "tree", "full", "web", "dump"],
        help="Команда анализа"
    )

    parser.add_argument(
        "--html",
        action="store_true",
        help="Вывести отчёт в HTML"
    )

    args = parser.parse_args()

    if args.command == "dump":
        dump_project()
        return

    stats = analyze_project()

    if args.command == "analyze":
        print("Анализ выполнен.")
        return

    if args.command == "tree":
        print(render_tree(stats))
        return

    if args.command == "web":
        run_web()
        return

    if args.command == "report":
        if args.html:
            print("<pre>")
            print(render_text_report(stats))
            print("</pre>")
        else:
            print(render_text_report(stats))
        return

    if args.command == "full":
        print(render_tree(stats))
        print()
        print(render_text_report(stats))
