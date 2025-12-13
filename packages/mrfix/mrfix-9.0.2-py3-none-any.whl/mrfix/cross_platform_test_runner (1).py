#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Цель: кроссплатформенный оркестратор, повторяющий шаги вашего bash-скрипта,
#       но читающий все параметры из JSON. Практически каждая строка снабжена
#       пояснениями "что/зачем/почему".

from __future__ import annotations  # Обеспечивает поддержку аннотаций типов строкой (для Python <3.11)

# === Стандартная библиотека: используем только то, что есть "из коробки" ===
import json                       # Чтение/запись JSON-файлов с конфигурацией
import os                         # Работа с переменными окружения, путями и пр.
import shlex                      # Форматирование команд для логов (shell-подобная экранизация)
import shutil                     # Утилиты вроде which(), копирование файлов
import signal                     # Кроссплатформенные сигналы для завершения процессов
import subprocess                 # Запуск внешних процессов (git, pip, pytest и т.д.)
import sys                        # Доступ к argv, пути к интерпретатору и пр.
import time                       # Метки времени, ожидания/таймауты
from dataclasses import dataclass, field   # Компактное описание конфигов
from pathlib import Path                   # Кроссплатформенные пути (Windows/Linux/macOS)
from typing import Dict, List, Optional, Tuple  # Аннотации типов для читабельности и IDE

# ------------------------------ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ------------------------------

def which(cmd: str) -> Optional[str]:
    """Кроссплатформенный поиск исполняемого файла в PATH. Возвращает полный путь или None."""
    return shutil.which(cmd)

def ensure_dir(p: Path) -> None:
    """Гарантирует существование каталога (создаёт с parents=True). Ничего не делает, если уже есть."""
    p.mkdir(parents=True, exist_ok=True)

def now_ts() -> str:
    """Возвращает строку-временную метку для имён логов/артефактов."""
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

def platform_is_windows() -> bool:
    """True на Windows (os.name == 'nt'), иначе False. Важно для корректного завершения процессов."""
    return os.name == "nt"

def safe_join(*parts: str) -> str:
    """Безопасно склеивает части пути кроссплатформенно (через pathlib)."""
    return str(Path(*parts))

def merge_env(base_env: Dict[str, str], extra: Dict[str, str] | None) -> Dict[str, str]:
    """Сливает базовое окружение с доп. переменными из конфига; значения приводим к строкам."""
    env = dict(base_env)
    if extra:
        env.update({k: str(v) for k, v in extra.items()})
    return env

def read_json(path: Path) -> dict:
    """Читает JSON-файл и возвращает dict. Unicode-safe (utf-8)."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def write_text(path: Path, data: str) -> None:
    """Пишет текст в файл, создавая каталоги при необходимости."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")

def popen_args_for_shell(cmd: List[str] | str, use_shell: bool) -> Tuple[List[str] | str, bool]:
    """
    Возвращает пару (команда, флаг shell). Мы явно прокидываем shell=True только по запросу,
    иначе оставляем False (без промежуточной оболочки) — так безопаснее/кроссплатформеннее.
    """
    return (cmd, use_shell)

def format_cmd_for_log(cmd: List[str] | str) -> str:
    """Возвращает команду как строку, пригодную для логирования (shell-подобное quoting)."""
    if isinstance(cmd, str):
        return cmd
    return " ".join(shlex.quote(x) for x in cmd)

class RunResult:
    """Простой контейнер результата запуска внешней команды."""
    def __init__(self, returncode: int, stdout: str, stderr: str, timeout: bool):
        self.returncode = returncode  # Код возврата процесса (0 — успех)
        self.stdout = stdout          # Собранный stdout
        self.stderr = stderr          # Собранный stderr
        self.timeout = timeout        # Был ли таймаут (True/False)

def run_cmd(
    cmd: List[str] | str,
    cwd: Optional[Path] = None,
    env: Optional[Dict[str, str]] = None,
    timeout: Optional[int] = None,
    kill_after: Optional[int] = None,
    log_file: Optional[Path] = None,
    use_shell: bool = False,
) -> RunResult:
    """
    Запускает внешнюю команду с поддержкой таймаута и "grace period" (kill_after).
    Поведение:
      - при истечении timeout сначала посылается мягкое завершение (terminate/SIGTERM),
      - затем ждём kill_after секунд,
      - если процесс жив — принудительно убиваем (kill/SIGKILL).
    Логи пишутся потоково (строчно) в log_file (если задан).
    """
    if env is None:
        env = os.environ.copy()  # База окружения по умолчанию — текущее окружение процесса

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)  # Гарантируем каталог для лога

    popen_cmd, popen_shell = popen_args_for_shell(cmd, use_shell)  # Уточняем способ запуска
    start = time.time()                                           # Фиксируем начало — для таймаута

    # subprocess.Popen: text=True и universal_newlines=True — построчное чтение в str (не bytes)
    proc = subprocess.Popen(
        popen_cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=popen_shell,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    timed_out = False              # Флаг, сработал ли таймаут
    stdout_chunks: List[str] = []  # Аккумулируем stdout
    stderr_chunks: List[str] = []  # Аккумулируем stderr

    def _terminate():
        """Мягкое завершение: Windows — terminate(), POSIX — SIGTERM."""
        if proc.poll() is None:  # Процесс ещё жив
            try:
                if platform_is_windows():
                    proc.terminate()
                else:
                    proc.send_signal(signal.SIGTERM)
            except Exception:
                pass  # Не падаем в логике мониторинга

    def _kill():
        """Жёсткое убийство процесса, если мягкое не помогло."""
        if proc.poll() is None:
            try:
                proc.kill()
            except Exception:
                pass

    # Основной цикл: читаем вывод построчно, контролируем таймаут/завершение
    while True:
        try:
            out = proc.stdout.readline() if proc.stdout else ""  # Читаем одну строку stdout
            err = proc.stderr.readline() if proc.stderr else ""  # Читаем одну строку stderr
        except Exception:
            out = ""
            err = ""

        if out:
            stdout_chunks.append(out)                # В память
            if log_file:
                with log_file.open("a", encoding="utf-8") as f:
                    f.write(out)                     # И сразу в файл

        if err:
            stderr_chunks.append(err)                # Аналогично для stderr
            if log_file:
                with log_file.open("a", encoding="utf-8") as f:
                    f.write(err)

        if proc.poll() is not None:                  # Процесс завершился сам
            break

        if timeout is not None and (time.time() - start) > timeout and not timed_out:
            # Сработал таймаут в первый раз — отмечаем и запускаем грациозное завершение
            timed_out = True
            _terminate()
            if kill_after is None:
                kill_after = 15  # Значение по умолчанию, если не задано в конфиге

            # Ждём "grace period"
            grace_start = time.time()
            while proc.poll() is None and (time.time() - grace_start) < kill_after:
                time.sleep(0.2)

            # Если всё ещё жив — принудительно убиваем
            if proc.poll() is None:
                _kill()

        time.sleep(0.02)  # Маленький сон, чтобы не грузить CPU (poll/readline в цикле)

    # Собираем итоговые строки
    stdout = "".join(stdout_chunks)
    stderr = "".join(stderr_chunks)
    # subprocess может вернуть None, нормализуем к int
    return RunResult(proc.returncode or 0, stdout, stderr, timed_out)

# ------------------------------ ОПИСАНИЕ КОНФИГА ------------------------------
# dataclass-ы описывают структуру JSON. Так IDE подсказывает поля, а мы получаем валидацию типов.

@dataclass
class GitConfig:
    repo_dir: str                    # Локальный каталог с репозиторием
    remote_url: str                  # URL origin (ssh/https)
    branch: str = "master"           # Целевая ветка для fetch
    depth: int = 1                   # Мелкий fetch для скорости (shallow)

@dataclass
class PytestConfig:
    python_executable: Optional[str] = None          # Если None — используем текущий интерпретатор
    additional_args: List[str] = field(default_factory=lambda: ["-q"])  # Доп. флаги pytest
    xdist_workers: Optional[int] = None              # Кол-во воркеров для pytest-xdist
    xdist_dist: Optional[str] = None                 # Стратегия распределения (load/each/etc.)
    junit_xml: Optional[str] = None                  # Путь для отчёта JUnit (если нужен)
    timeout: Optional[int] = 1800                    # Таймаут на прогон pytest
    kill_after: Optional[int] = 30                   # Грейс-период после таймаута
    tests_root: Optional[str] = None                 # Корень тестов (папка/путь), опционально
    env: Dict[str, str] = field(default_factory=dict)  # Переменные окружения для pytest

@dataclass
class DepsConfig:
    install: bool = False                            # Включить установку зависимостей
    requirements_file: Optional[str] = None          # Путь к requirements.txt внутри repo_dir
    pip_executable: Optional[str] = None             # Явный pip, иначе python -m pip
    timeout: Optional[int] = 900                     # Таймаут на установку
    kill_after: Optional[int] = 30                   # Грейс-период после таймаута

@dataclass
class RerunFailedConfig:
    enabled: bool = False                            # Включить повторный прогон упавших тестов
    command: Optional[List[str]] = None              # Команда запуска (напр., ["python","run_failed_tests.py"])
    timeout: Optional[int] = 1200                    # Таймаут на повторный прогон
    kill_after: Optional[int] = 30                   # Грейс-период

@dataclass
class AVScanConfig:
    enabled: bool = False                            # Включить антивирусную проверку (clamscan)
    paths: List[str] = field(default_factory=list)   # Пути для сканирования
    timeout: Optional[int] = 1800                    # Таймаут на сканирование
    kill_after: Optional[int] = 30                   # Грейс-период

@dataclass
class ArchiveConfig:
    enabled: bool = False                            # Упаковать артефакты в zip
    paths: List[str] = field(default_factory=list)   # Пути, которые нужно добавить в архив
    output_zip: Optional[str] = None                 # Явное имя архива (если None — сгенерируем)

@dataclass
class RunnerConfig:
    log_dir: str                                     # Куда писать логи/артефакты
    working_dir: str                                 # Зарезервировано (на будущее)
    git: GitConfig                                   # Блок git
    deps: DepsConfig = DepsConfig()                  # Блок зависимостей
    pytest: PytestConfig = PytestConfig()            # Блок pytest
    rerun_failed: RerunFailedConfig = RerunFailedConfig()  # Блок повторных прогонов
    av_scan: AVScanConfig = AVScanConfig()           # Блок AV
    archive: ArchiveConfig = ArchiveConfig()         # Блок архивации
    extra_env: Dict[str, str] = field(default_factory=dict)  # Общие доп. переменные окружения

    @staticmethod
    def from_json(path: Path) -> "RunnerConfig":
        """Конструирует RunnerConfig из JSON-файла (валидация полей через dataclass)."""
        data = read_json(path)
        def _dc(cls, key):
            return cls(**data.get(key, {}))
        return RunnerConfig(
            log_dir=data["log_dir"],
            working_dir=data.get("working_dir", data["git"]["repo_dir"]),
            git=GitConfig(**data["git"]),
            deps=_dc(DepsConfig, "deps"),
            pytest=_dc(PytestConfig, "pytest"),
            rerun_failed=_dc(RerunFailedConfig, "rerun_failed"),
            av_scan=_dc(AVScanConfig, "av_scan"),
            archive=_dc(ArchiveConfig, "archive"),
            extra_env=data.get("extra_env", {}),
        )

# ------------------------------ ШАГИ ПАЙПЛАЙНА ------------------------------

def step_git_sync(cfg: RunnerConfig, log_path: Path) -> None:
    """Инициализирует репозиторий, настраивает origin, делает shallow fetch и checkout FETCH_HEAD."""
    repo_dir = Path(cfg.git.repo_dir)       # Каталог репозитория
    ensure_dir(repo_dir)                    # Создаём, если нет

    env = merge_env(os.environ, cfg.extra_env)  # Наследуем окружение процесса + extra_env

    # Если .git нет — инициализируем пустой репозиторий (позволяет fetch по origin)
    if not (repo_dir / ".git").exists():
        res = run_cmd(["git", "init"], cwd=repo_dir, env=env, log_file=log_path)
        if res.returncode != 0:
            raise RuntimeError(f"git init failed: {res.stderr}")

    # На всякий случай удаляем старый origin (если был), чтобы гарантированно задать новый
    run_cmd(["git", "remote", "remove", "origin"], cwd=repo_dir, env=env, log_file=log_path)
    # Пытаемся добавить origin (если существовал — предыдущая команда его сняла)
    res = run_cmd(["git", "remote", "add", "origin", cfg.git.remote_url], cwd=repo_dir, env=env, log_file=log_path)
    # Если добавить не удалось (например, гонка) — не падаем, origin уже может быть настроен

    # Делаем fetch нужной ветки (опционально shallow через --depth), чтобы забрать свежие коммиты
    fetch_cmd = ["git", "fetch", "--prune"]         # --prune удаляет устаревшие ссылки
    if cfg.git.depth:
        fetch_cmd += [f"--depth={int(cfg.git.depth)}"]  # Мелкая история ускоряет/экономит сеть
    fetch_cmd += ["origin", cfg.git.branch]         # Забираем только нужную ветку
    res = run_cmd(fetch_cmd, cwd=repo_dir, env=env,
                  timeout=cfg.pytest.timeout, kill_after=cfg.pytest.kill_after, log_file=log_path)
    if res.returncode != 0:
        # Если fetch не удался — дальнейший сценарий бессмыслен (нет кода тестов)
        raise RuntimeError(f"git fetch failed: {res.stderr}")

    # Жёсткий checkout на FETCH_HEAD — это "то, что только что стянули"
    res = run_cmd(["git", "checkout", "-f", "FETCH_HEAD"], cwd=repo_dir, env=env, log_file=log_path)
    if res.returncode != 0:
        raise RuntimeError(f"git checkout failed: {res.stderr}")

def step_install_deps(cfg: RunnerConfig, log_path: Path) -> None:
    """Опциональная установка зависимостей через pip, если включено в конфиге."""
    if not cfg.deps.install:
        return  # Пользователь отключил установку

    req = cfg.deps.requirements_file       # Имя/путь requirements.txt (относительно repo_dir)
    if not req:
        return  # Нечего ставить — файл не указан

    repo_dir = Path(cfg.git.repo_dir)      # Корень репозитория
    req_path = repo_dir / req              # Полный путь до requirements.txt
    if not req_path.exists():
        # Явно сообщаем, чтобы не было "тихих пропусков"
        raise FileNotFoundError(f"requirements file not found: {req_path}")

    # Определяем, чем запускать pip: явным бинарём или через python -m pip
    if cfg.deps.pip_executable:
        pip_cmd = [cfg.deps.pip_executable]
    else:
        py = cfg.pytest.python_executable or sys.executable  # Берём тот же интерпретатор, что и pytest
        pip_cmd = [py, "-m", "pip"]

    cmd = pip_cmd + ["install", "-r", str(req_path)]  # Сборка команды установки
    res = run_cmd(cmd, cwd=repo_dir,
                  timeout=cfg.deps.timeout, kill_after=cfg.deps.kill_after, log_file=log_path)
    if res.returncode != 0:
        # Не глотаем ошибку — зависимости критичны для тестов
        raise RuntimeError(f"pip install failed: {res.stderr}")

def step_pytest(cfg: RunnerConfig, log_path: Path) -> int:
    """Запускает pytest с учётом xdist, junit, env и таймаутов. Возвращает код возврата pytest."""
    repo_dir = Path(cfg.git.repo_dir)                  # Где выполнять
    py = cfg.pytest.python_executable or sys.executable  # Какой Python использовать

    cmd = [py, "-m", "pytest"]                        # Всегда через модуль, чтобы не зависеть от PATH
    if cfg.pytest.xdist_workers:
        cmd += ["-n", str(cfg.pytest.xdist_workers)]  # Параллелизм
        if cfg.pytest.xdist_dist:
            cmd += ["--dist", cfg.pytest.xdist_dist]  # Стратегия распределения
    if cfg.pytest.junit_xml:
        junit_path = str(repo_dir / cfg.pytest.junit_xml)  # Репорт JUnit, если задан
        cmd += ["--junitxml", junit_path]

    cmd += cfg.pytest.additional_args or []           # Прочие аргументы из конфига

    tests_root = cfg.pytest.tests_root                # Явный путь до тестов (можно не задавать)
    if tests_root:
        cmd.append(tests_root)

    env = merge_env(os.environ, cfg.extra_env)        # Базовое окружение + глобальные доп. переменные
    env = merge_env(env, cfg.pytest.env)              # Плюс окружение, специфичное для pytest

    res = run_cmd(
        cmd,
        cwd=repo_dir,
        env=env,
        timeout=cfg.pytest.timeout,
        kill_after=cfg.pytest.kill_after,
        log_file=log_path,
    )
    return res.returncode  # 0 — успех, иначе pytest сигнализирует проблемами

def step_rerun_failed(cfg: RunnerConfig, log_path: Path) -> Optional[int]:
    """Опциональный шаг повторного прогона (например, run_failed_tests.py)."""
    if not cfg.rerun_failed.enabled or not cfg.rerun_failed.command:
        return None  # Отключено или не задана команда

    repo_dir = Path(cfg.git.repo_dir)  # Выполняем в корне репозитория
    res = run_cmd(
        cfg.rerun_failed.command,
        cwd=repo_dir,
        timeout=cfg.rerun_failed.timeout,
        kill_after=cfg.rerun_failed.kill_after,
        log_file=log_path,
    )
    return res.returncode  # Возвращаем код возврата повторного шага

def step_av_scan(cfg: RunnerConfig, log_path: Path) -> Optional[int]:
    """Опциональный антивирусный скан ClamAV (если установлен clamscan и включено в конфиге)."""
    if not cfg.av_scan.enabled or not cfg.av_scan.paths:
        return None  # Отключено/нечего сканировать

    if which("clamscan") is None:
        # На машине нет clamscan — фиксируем факт и выходим без ошибки
        write_text(log_path, "\n[WARN] clamscan not found; AV scan skipped\n")
        return None

    code = 0  # Итоговый код (если где-то будет 1 из-за найденных вирусов — оставим это значение)
    for p in cfg.av_scan.paths:
        res = run_cmd(
            ["clamscan", "-r", "--bell", p],  # Рекурсивное сканирование, звуковой сигнал при вирусах
            timeout=cfg.av_scan.timeout,
            kill_after=cfg.av_scan.kill_after,
            log_file=log_path,
        )
        # В ClamAV код 1 означает "обнаружены угрозы" — это не сбой запуска, но сигнализируем через код
        if res.returncode != 0 and code == 0:
            code = res.returncode
    return code

def step_archive(cfg: RunnerConfig, ts: str, log_path: Path) -> Optional[Path]:
    """Опционально собирает артефакты (логи/репорты) в ZIP и возвращает путь к архиву."""
    if not cfg.archive.enabled:
        return None  # Архивация отключена

    # Приводим входные пути, фильтруем пустые
    paths = [Path(p) for p in cfg.archive.paths if p]
    if not paths:
        return None  # Нечего архивировать

    # Если имя архива не задано — размещаем в log_dir с временной меткой
    out = Path(cfg.archive.output_zip or safe_join(cfg.log_dir, f"artifacts_{ts}.zip"))
    out.parent.mkdir(parents=True, exist_ok=True)

    # Собираем zip-архив стандартной библиотекой (без внешних зависимостей)
    import zipfile
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in paths:
            p = p.resolve()
            if p.is_file():
                # Одна штука — кладём как есть (arcname — имя внутри архива)
                z.write(p, arcname=p.name)
            elif p.is_dir():
                # Рекурсивно добавляем все файлы каталога, сохраняя относительную структуру
                for root, _, files in os.walk(p):
                    for f in files:
                        fp = Path(root) / f
                        z.write(fp, arcname=str(Path(p.name) / fp.relative_to(p)))

    # Добавим основной лог, чтобы он точно был в артефактах
    if log_path.exists():
        with zipfile.ZipFile(out, "a", compression=zipfile.ZIP_DEFLATED) as z:
            z.write(log_path, arcname=log_path.name)

    return out  # Вернём путь к архиву

# ------------------------------ ПУБЛИЧНОЕ API ------------------------------

def run_pipeline(config_path: str) -> int:
    """
    Точка входа пайплайна. Получает путь к JSON-конфигу, выполняет все шаги.
    Возвращает агрегированный код возврата:
      0 — успех, иначе — код падения pytest/сканера/и пр.
    """
    cfg = RunnerConfig.from_json(Path(config_path))  # Загружаем конфиг из JSON

    ts = now_ts()                                    # Метка времени для логов/архива
    log_dir = Path(cfg.log_dir)                      # Директория под логи
    ensure_dir(log_dir)                              # Создаём при необходимости
    log_path = log_dir / f"run_{ts}.log"             # Имя файла лога
    write_text(log_path, f"== Start run {ts} ==\n")  # Заголовок лога

    overall_status = 0  # Итоговый код (0 — считаем успехом, обновляем по мере шагов)

    try:
        # --- GIT SYNC ---
        step_git_sync(cfg, log_path)
        write_text(log_path, "[OK] Git sync completed\n")

        # --- DEPS INSTALL (optional) ---
        step_install_deps(cfg, log_path)
        write_text(log_path, "[OK] Dependencies step completed (or skipped)\n")

        # --- PYTEST ---
        rc = step_pytest(cfg, log_path)                     # Запускаем тесты
        write_text(log_path, f"[INFO] pytest exit code: {rc}\n")
        if rc != 0:
            overall_status = rc                             # Фиксируем неуспех тестов
            # --- RERUN FAILED (optional) ---
            rrc = step_rerun_failed(cfg, log_path)         # Повторный прогон (если включён)
            if rrc is not None:
                write_text(log_path, f"[INFO] rerun_failed exit code: {rrc}\n")
                # Если повторный прогон прошёл успешно — считаем общий статус успешным
                overall_status = rrc if rrc != 0 else 0

        # --- AV SCAN (optional) ---
        avc = step_av_scan(cfg, log_path)
        if avc is not None:
            write_text(log_path, f"[INFO] AV scan exit code: {avc}\n")
            # Если до этого было всё ОК, но сканер вернул 1 (угрозы) — отдаём этот код
            if overall_status == 0 and avc != 0:
                overall_status = avc

        # --- ARCHIVE (optional) ---
        artifact = step_archive(cfg, ts, log_path)
        if artifact:
            write_text(log_path, f"[OK] Artifacts archived to: {artifact}\n")

    except Exception as e:
        # Любая непойманная ошибка шага: записываем в лог и возвращаем 1 (ошибка пайплайна)
        write_text(log_path, f"[ERROR] {type(e).__name__}: {e}\n")
        return 1

    # Закрывающая запись — фиксируем итоговый код
    write_text(log_path, f"== Finish run {now_ts()} (status={overall_status}) ==\n")
    return int(overall_status)

# ------------------------------ CLI-ОБОБОЛОЧКА ------------------------------

if __name__ == "__main__":
    # Простой интерфейс командной строки: 1 аргумент — путь к JSON-конфигу.
    if len(sys.argv) != 2:
        # Возвращаем явную подсказку об использовании и код 2 (часто применяют для "usage error")
        print("Usage: python cross_platform_test_runner.py <config.json>")
        sys.exit(2)
    # Запускаем пайплайн и пробрасываем его код возврата наружу (для CI/cron)
    sys.exit(run_pipeline(sys.argv[1]))
