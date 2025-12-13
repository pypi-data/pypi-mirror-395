# DIAGNOSE/project_diagnose/analyzer.py

import os
import math
import datetime
from .config_schema import DiagnoseConfig

ROOT = os.getcwd()
OUTPUT_FILE = os.path.join(ROOT, "all_code.txt")

EXCLUDE_DIRS = {"venv", "__pycache__", ".git", ".idea", ".vscode"}
INCLUDE_EXT = {".py", ".json"}
SPECIAL_JSON = {"config_ui.json"}

USER_CFG_PATH = os.path.join(ROOT, "config.diagnose")

def generate_default_config(path):
    default_cfg = {
        "include_ext": [".py", ".json"],
        "exclude_dirs": ["venv", "__pycache__", ".git"],
        "exclude_files": [],
        "include_files": [],
        "special_json": ["config_ui.json"]
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            import json
            json.dump(default_cfg, f, indent=4, ensure_ascii=False)
        print("[diagnose] Создан новый config.diagnose (пустой шаблон).")
    except Exception as e:
        print(f"[diagnose] Не удалось создать config.diagnose: {e}")
        
def load_user_config():
    if not os.path.exists(USER_CFG_PATH):
        generate_default_config(USER_CFG_PATH)
        print("[diagnose] Создан шаблон config.diagnose.")
        return DiagnoseConfig()  # дефолты

    try:
        with open(USER_CFG_PATH, "r", encoding="utf-8") as f:
            raw = f.read()

        import json
        parsed = json.loads(raw)

        cfg = DiagnoseConfig(**parsed)
        print("[diagnose] Загружен и провалидирован config.diagnose")
        return cfg

    except Exception as e:
        print(f"[diagnose] Ошибка в config.diagnose → {e}")
        print("[diagnose] Использую конфигурацию по умолчанию.")
        return DiagnoseConfig()
        

USER_CFG = load_user_config()

# применяем
EXCLUDE_DIRS = set(USER_CFG.exclude_dirs)
INCLUDE_EXT = set(USER_CFG.include_ext)
SPECIAL_JSON = set(USER_CFG.special_json)
EXCLUDE_FILES = set(USER_CFG.exclude_files)
INCLUDE_FILES_EXTRA = set(USER_CFG.include_files)

def should_skip_dir(dirname: str) -> bool:
    name = os.path.basename(dirname)
    return name in EXCLUDE_DIRS


def is_valid_file(filename: str) -> bool:
    # пользовательские исключения
    if filename in EXCLUDE_FILES:
        return False

    # пользовательские explicit include
    if filename in INCLUDE_FILES_EXTRA:
        return True

    _, ext = os.path.splitext(filename)

    # особые JSON
    if ext == ".json" and filename in SPECIAL_JSON:
        return True

    # обычный случай
    return ext in INCLUDE_EXT


def collect_files():
    collected = []

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not should_skip_dir(os.path.join(root, d))]
        for f in files:
            if is_valid_file(f):
                full_path = os.path.join(root, f)
                collected.append(full_path)

    collected.sort()
    return collected


# ========================== НОВОЕ: структура с подписями ==========================

def format_size(bytes_count: int) -> str:
    if bytes_count < 1024:
        return f"{bytes_count} B"
    elif bytes_count < 1024 * 1024:
        return f"{bytes_count / 1024:.1f} KB"
    else:
        return f"{bytes_count / 1024 / 1024:.1f} MB"


def count_lines(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except:
        return 0


def build_tree():
    tree_lines = []

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not should_skip_dir(os.path.join(root, d))]

        level = os.path.relpath(root, ROOT).count(os.sep)
        indent = "    " * level

        dirname = os.path.basename(root)
        tree_lines.append(f"{indent}{dirname}/")

        for f in files:
            full_path = os.path.join(root, f)

            size = format_size(os.path.getsize(full_path))
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
            mtime_str = mtime.strftime("%Y-%m-%d %H:%M")

            lines = count_lines(full_path)

            tree_lines.append(
                f"{indent}    {f}  [{size}, {mtime_str}, {lines} строк]"
            )

    return "\n".join(tree_lines)

# ========================== АНАЛИТИКА ПРОЕКТА ==========================

def gather_stats(files):
    stats = {
        "total_size": 0,
        "ext_lines": {},
        "heavy_files": [],
        "long_files": [],
        "tiny_files": []
    }

    for path in files:
        size = os.path.getsize(path)
        lines = count_lines(path)
        ext = os.path.splitext(path)[1]

        stats["total_size"] += size

        # строки по расширению
        stats["ext_lines"].setdefault(ext, 0)
        stats["ext_lines"][ext] += lines

        stats["heavy_files"].append((size, path))
        stats["long_files"].append((lines, path))

        if lines <= 5 or size < 200:
            stats["tiny_files"].append((size, lines, path))

    # сортировки
    stats["heavy_files"].sort(reverse=True)
    stats["long_files"].sort(reverse=True)
    stats["tiny_files"].sort()

    return stats


def format_stats(stats):
    out = []
    out.append("# ===== Аналитика проекта =====")

    # общий вес
    out.append(f"Суммарный вес файлов: {format_size(stats['total_size'])}\n")

    # строки по расширениям
    out.append("Количество строк по расширениям:")
    for ext, count in stats["ext_lines"].items():
        out.append(f"  {ext}: {count} строк")
    out.append("")

    # топ-5 тяжёлых
    out.append("Топ 5 самых тяжёлых файлов:")
    for size, path in stats["heavy_files"][:5]:
        out.append(f"  {format_size(size):>8}  {os.path.relpath(path, ROOT)}")
    out.append("")

    # топ-5 длинных
    out.append("Топ 5 самых длинных файлов:")
    for lines, path in stats["long_files"][:5]:
        out.append(f"  {lines:>6} строк  {os.path.relpath(path, ROOT)}")
    out.append("")

    # подозрительно маленькие файлы
    out.append("Подозрительно маленькие файлы (возможно мусор):")
    for size, lines, path in stats["tiny_files"][:7]:
        out.append(f"  {format_size(size):>8}, {lines:3} строк  {os.path.relpath(path, ROOT)}")

    out.append("\n")
    return "\n".join(out)

# ====================== AI-оценка безнадёжности проекта ======================

def build_pie_chart(stats):
    total = sum(stats["ext_lines"].values())
    if total == 0:
        return "Нет данных для построения диаграммы."

    pieces = []
    for ext, lines in stats["ext_lines"].items():
        pct = lines / total
        bars = int(pct * 20)
        pieces.append(f"{ext:6} | {'#' * bars}{'.' * (20 - bars)} | {pct * 100:5.1f}%")

    return "\n".join(pieces)


def calc_chaos_score(stats):
    # хаос = количество типов файлов * коэффициент разброса размеров * коэффициент мелкого мусора
    unique_ext = len(stats["ext_lines"])
    size_spread = (stats["heavy_files"][0][0] + 1) / (stats["tiny_files"][0][0] + 1)
    tiny_penalty = len(stats["tiny_files"]) * 0.7

    chaos = unique_ext * math.log(size_spread + 3) + tiny_penalty
    return round(chaos, 2)


def calc_tech_karma(stats):
    # карма = средняя длина файла / количество маленьких файлов
    avg_lines = sum(l for l, _ in stats["long_files"]) / len(stats["long_files"])
    tiny_count = len(stats["tiny_files"]) or 1
    karma = avg_lines / tiny_count
    return round(karma, 2)


def ai_verdict(chaos, karma):
    if chaos < 8 and karma > 150:
        return "Структура удивительно приличная. Почти не стыдно."
    if chaos < 15:
        return "Нормально, жить можно. Иногда."
    if chaos < 22:
        return "Ты как будто пытался. Видно старание. И боль."
    if chaos < 35:
        return "Проект напоминает чердак, куда сносят всё подряд «на потом»."
    return "Сожги и беги. Я сделал вид, что не видел это."


def format_ai_analysis(stats):
    out = []
    out.append("# ===== AI-оценка состояния проекта =====")

    out.append("\nСтруктура по строкам (ASCII pie chart):")
    out.append(build_pie_chart(stats))

    chaos = calc_chaos_score(stats)
    karma = calc_tech_karma(stats)

    out.append(f"\nИндекс хаоса: {chaos}")
    out.append(f"Техническая карма: {karma}")

    verdict = ai_verdict(chaos, karma)
    out.append(f"\nAI-вердикт: {verdict}\n")

    # оценки файлов типа «пора выбросить»
    out.append("Файлы, вызывающие сомнения:")
    suspicious = sorted(stats["tiny_files"], key=lambda x: (x[0], x[1]))
    for size, lines, path in suspicious[:10]:
        score = (5 - min(lines, 5)) * 10 + (200 - min(size, 200)) / 10
        score = round(score, 1)
        out.append(f"  {os.path.relpath(path, ROOT)}  | уровень бесполезности {score}/100")

    out.append("\n")
    return "\n".join(out)

# ====================== Индекс будущего сожаления ======================

def calc_future_regret_index(stats):
    long_files = stats["long_files"]
    tiny_files = stats["tiny_files"]

    if not long_files:
        return 0

    max_lines = long_files[0][0]
    min_lines = long_files[-1][0] if long_files else 1
    spread = max_lines - min_lines

    tiny_factor = len(tiny_files) * 4
    long_factor = math.sqrt(max_lines) * 1.2
    spread_factor = math.log(spread + 5) * 6

    fri = tiny_factor + long_factor + spread_factor
    return round(fri, 2)


# ====================== Граф зависимостей мусорных файлов ======================

def extract_imports(path):
    imports = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("import "):
                    parts = line.split()
                    if len(parts) > 1:
                        imports.append(parts[1].split('.')[0])
                elif line.startswith("from "):
                    parts = line.split()
                    if len(parts) > 1:
                        imports.append(parts[1].split('.')[0])
    except:
        pass
    return imports


def build_suspicious_graph(stats):
    lines = []
    tiny_files = stats["tiny_files"]

    module_map = {}
    for _, _, path in tiny_files:
        mod = os.path.splitext(os.path.basename(path))[0]
        module_map[mod] = path

    # строим граф
    for _, _, path in tiny_files:
        mod = os.path.splitext(os.path.basename(path))[0]
        imports = extract_imports(path)

        for imp in imports:
            if imp in module_map:
                lines.append(f"{mod} --> {imp}")
            else:
                lines.append(f"{mod} --> {imp} (влияет на основной код)")

    if not lines:
        return "Нет зависимостей. Эти файлы бесполезны в гордом одиночестве."

    return "\n".join(lines)


# ====================== Форматирование блока ======================

def format_future_analysis(stats):
    fri = calc_future_regret_index(stats)
    graph = build_suspicious_graph(stats)

    out = []
    out.append("# ===== Прогноз страданий разработчика =====")
    out.append(f"Индекс будущего сожаления (FRI): {fri}")

    if fri < 25:
        out.append("Переживать не о чем. Даже приятно посмотреть.")
    elif fri < 60:
        out.append("Через полгода ты слегка вздохнёшь и продолжишь.")
    elif fri < 120:
        out.append("Будущая боль ощутима. Закладывай время на рефакторинг.")
    else:
        out.append("Просто оставлю это здесь. Ты знаешь, что делается.")

    out.append("\nГраф зависимостей подозрительных файлов:")
    out.append(graph)
    out.append("\n")

    return "\n".join(out)

# ========================== запись итогового файла ==========================

def write_all_code(files):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:

        # АНАЛИТИКА
        stats = gather_stats(files)
        out.write(format_stats(stats))
        # AI-анализ
        out.write(format_ai_analysis(stats))
        # прогноз страданий
        out.write(format_future_analysis(stats))
        # ДЕРЕВО
        out.write("# ===== Структура проекта =====\n")
        out.write(build_tree())
        out.write("\n\n")

        # КОД
        for path in files:
            rel = os.path.relpath(path, ROOT)
            out.write(f"# ------- {rel}\n")
            try:
                with open(path, "r", encoding="utf-8") as src:
                    out.write(src.read())
            except Exception as e:
                out.write(f"<<Error reading file: {e}>>")
            out.write("\n\n")

    print(f"Готово! Файл собран: {OUTPUT_FILE}")

def dump_project():
    files = collect_files()
    write_all_code(files)
    
def analyze_project():
    files = collect_files()
    stats = gather_stats(files)
    stats["files"] = files
    stats["tree"] = build_tree()   
    return stats