# DIAGNOSE/project_diagnose/web.py

from flask import Flask, render_template_string, Response
from .analyzer import analyze_project
from .rendering import render_text_report, render_tree

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Project Diagnose</title>
    <style>
        :root {
            color-scheme: light dark;
        }
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            padding: 20px;
            margin: 0;
            background: #f4f4f4;
            color: #222;
            transition: background 0.2s, color 0.2s;
        }
        body.dark {
            background: #121212;
            color: #e0e0e0;
        }
        h1, h2 {
            margin-top: 0;
        }
        .toolbar {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            align-items: center;
        }
        button, a.button-link {
            border: none;
            padding: 8px 14px;
            border-radius: 999px;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;
            background: #333;
            color: #fff;
        }
        body.dark button,
        body.dark a.button-link {
            background: #444;
            color: #f4f4f4;
        }
        button:hover,
        a.button-link:hover {
            opacity: 0.9;
        }
        input[type="text"] {
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid #aaa;
            min-width: 220px;
            font-size: 14px;
            background: inherit;
            color: inherit;
        }
        body.dark input[type="text"] {
            border-color: #555;
        }
        .block {
            margin-bottom: 30px;
        }
        pre {
            background: #f6f6f6;
            padding: 12px 14px;
            border-radius: 8px;
            white-space: pre-wrap;
            max-height: 60vh;
            overflow: auto;
        }
        body.dark pre {
            background: #1e1e1e;
        }
        .highlight {
            background: #ffe8a3;
        }
        body.dark .highlight {
            background: #4b3b12;
        }
        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 11px;
            background: #ddd;
            color: #333;
            margin-left: 6px;
        }
        body.dark .badge {
            background: #333;
            color: #eee;
        }
    </style>
</head>
<body>
    <h1>Диагностика проекта</h1>

    <div class="toolbar">
        <button id="themeToggle">Тёмная / светлая тема</button>
        <button id="refactorBtn">Рефакторинг</button>
        <a href="/report.txt" class="button-link" download>Скачать отчёт (.txt)</a>

        <span style="margin-left:10px; font-size:13px;">Поиск «депрессивного» кода:</span>
        <input type="text" id="searchInput" placeholder="todo, hack, temp, fixme..." />
        <span class="badge">фильтрует отчёт ниже</span>
    </div>

    <div class="block">
        <h2>Структура проекта</h2>
        <pre id="treeBlock">{{ tree }}</pre>
    </div>

    <div class="block">
        <h2>Отчёт</h2>
        <pre id="reportBlock">{{ report }}</pre>
    </div>

    <script>
        // ТЕМА
        const body = document.body;
        const themeToggle = document.getElementById('themeToggle');

        function applyStoredTheme() {
            const theme = localStorage.getItem('project_diagnose_theme');
            if (theme === 'dark') {
                body.classList.add('dark');
            }
        }
        applyStoredTheme();

        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark');
            localStorage.setItem(
                'project_diagnose_theme',
                body.classList.contains('dark') ? 'dark' : 'light'
            );
        });

        // "Рефакторинг"
        const refactorBtn = document.getElementById('refactorBtn');
        refactorBtn.addEventListener('click', () => {
            alert("Кнопка рефакторинга найдена.\n\nК сожалению, рефакторинг жизни и проекта по нажатию пока не реализован.");
        });

        // Поиск «депрессивного» кода
        const searchInput = document.getElementById('searchInput');
        const reportBlock = document.getElementById('reportBlock');
        const originalReport = reportBlock.textContent;

        function escapeRegExp(str) {
            return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        }

        searchInput.addEventListener('input', () => {
            const query = searchInput.value.trim();
            if (!query) {
                reportBlock.textContent = originalReport;
                return;
            }

            const pattern = new RegExp(escapeRegExp(query), 'gi');
            const highlighted = originalReport.replace(pattern, match => '[[HIGHLIGHT]]' + match + '[[END]]');

            const html = highlighted
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/\[\[HIGHLIGHT\]\](.*?)\[\[END\]\]/g, '<span class="highlight">$1</span>');

            reportBlock.innerHTML = html;
        });
    </script>
</body>
</html>
"""

# Кешировать на время жизни процесса, чтобы не гонять анализ по каждому запросу
_stats_cache = None
_report_cache = None
_tree_cache = None


def get_stats():
    global _stats_cache, _report_cache, _tree_cache
    if _stats_cache is None:
        stats = analyze_project()
        _stats_cache = stats
        _report_cache = render_text_report(stats)
        _tree_cache = render_tree(stats)
    return _stats_cache, _report_cache, _tree_cache


@app.route("/")
def index():
    _, report, tree = get_stats()
    return render_template_string(
        PAGE,
        tree=tree,
        report=report
    )


@app.route("/report.txt")
def download_report():
    _, report, _ = get_stats()
    return Response(
        report,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=project_report.txt"}
    )


def run_web():
    print("Web-интерфейс запущен: http://127.0.0.1:5000")
    app.run(debug=False)
