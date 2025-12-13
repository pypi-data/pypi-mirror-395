#!/usr/bin/env python3
"""
Cross-platform test runner that mirrors the behavior of the provided Bash script,
but reads all parameters from an external JSON file.

Supported OS: Windows, Linux, macOS
Python: 3.9+
"""
from __future__ import annotations

import json
import os
import shlex
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------- Utilities ----------

def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def now_ts() -> str:
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

def platform_is_windows() -> bool:
    return os.name == "nt"

def safe_join(*parts: str) -> str:
    return str(Path(*parts))

def merge_env(base_env: Dict[str, str], extra: Dict[str, str] | None) -> Dict[str, str]:
    env = dict(base_env)
    if extra:
        env.update({k: str(v) for k, v in extra.items()})
    return env

def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def write_text(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")

def popen_args_for_shell(cmd: List[str] | str, use_shell: bool) -> Tuple[List[str] | str, bool]:
    # On Windows, using shell=True runs via cmd.exe; otherwise we keep it False unless explicitly requested.
    return (cmd, use_shell)

def format_cmd_for_log(cmd: List[str] | str) -> str:
    if isinstance(cmd, str):
        return cmd
    # produce a shell-like escaped string for logs
    return " ".join(shlex.quote(x) for x in cmd)

class RunResult:
    def __init__(self, returncode: int, stdout: str, stderr: str, timeout: bool):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.timeout = timeout

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
    Run a command with timeout and optional grace period (kill_after).
    - timeout: wall-clock seconds to wait before sending a soft termination.
    - kill_after: seconds to wait after soft termination before force-kill.
    Behavior:
      * POSIX: send SIGTERM, then after kill_after send SIGKILL.
      * Windows: call .terminate(), then after kill_after call .kill().
    """
    if env is None:
        env = os.environ.copy()

    # Ensure parent exists for log
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)

    # Prepare Popen
    popen_cmd, popen_shell = popen_args_for_shell(cmd, use_shell)
    start = time.time()
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

    timed_out = False
    stdout_chunks: List[str] = []
    stderr_chunks: List[str] = []

    def _terminate():
        if proc.poll() is None:
            try:
                if platform_is_windows():
                    proc.terminate()
                else:
                    proc.send_signal(signal.SIGTERM)
            except Exception:
                pass

    def _kill():
        if proc.poll() is None:
            try:
                proc.kill()
            except Exception:
                pass

    # Stream + timeout handling
    while True:
        try:
            out = proc.stdout.readline() if proc.stdout else ""
            err = proc.stderr.readline() if proc.stderr else ""
        except Exception:
            out = ""
            err = ""

        if out:
            stdout_chunks.append(out)
            if log_file:
                with log_file.open("a", encoding="utf-8") as f:
                    f.write(out)
        if err:
            stderr_chunks.append(err)
            if log_file:
                with log_file.open("a", encoding="utf-8") as f:
                    f.write(err)

        if proc.poll() is not None:
            # process ended
            break

        if timeout is not None and (time.time() - start) > timeout and not timed_out:
            timed_out = True
            _terminate()
            # give it grace period
            if kill_after is None:
                kill_after = 15
            grace_start = time.time()
            while proc.poll() is None and (time.time() - grace_start) < kill_after:
                time.sleep(0.2)
            if proc.poll() is None:
                _kill()

        # small sleep to avoid busy loop
        time.sleep(0.02)

    stdout = "".join(stdout_chunks)
    stderr = "".join(stderr_chunks)
    return RunResult(proc.returncode or 0, stdout, stderr, timed_out)

# ---------- Config ----------

@dataclass
class GitConfig:
    repo_dir: str
    remote_url: str
    branch: str = "master"
    # shallow fetch for speed
    depth: int = 1
    # optional credentials: rely on pre-configured SSH key or HTTPS credential manager

@dataclass
class PytestConfig:
    python_executable: Optional[str] = None   # default: current interpreter
    additional_args: List[str] = field(default_factory=lambda: ["-q"])
    xdist_workers: Optional[int] = None       # e.g., 8
    xdist_dist: Optional[str] = None          # e.g., "load"
    junit_xml: Optional[str] = None           # path to save JUnit XML if needed
    timeout: Optional[int] = 1800             # seconds
    kill_after: Optional[int] = 30            # seconds
    tests_root: Optional[str] = None          # e.g., "tests"
    env: Dict[str, str] = field(default_factory=dict)

@dataclass
class DepsConfig:
    install: bool = False
    requirements_file: Optional[str] = None
    pip_executable: Optional[str] = None      # default: python -m pip
    timeout: Optional[int] = 900
    kill_after: Optional[int] = 30

@dataclass
class RerunFailedConfig:
    enabled: bool = False
    command: Optional[List[str]] = None       # e.g., ["python", "run_failed_tests.py"]
    timeout: Optional[int] = 1200
    kill_after: Optional[int] = 30

@dataclass
class AVScanConfig:
    enabled: bool = False
    paths: List[str] = field(default_factory=list)
    # Only runs if 'clamscan' is available
    timeout: Optional[int] = 1800
    kill_after: Optional[int] = 30

@dataclass
class ArchiveConfig:
    enabled: bool = False
    paths: List[str] = field(default_factory=list)
    output_zip: Optional[str] = None

@dataclass
class RunnerConfig:
    log_dir: str
    working_dir: str
    git: GitConfig
    deps: DepsConfig = DepsConfig()
    pytest: PytestConfig = PytestConfig()
    rerun_failed: RerunFailedConfig = RerunFailedConfig()
    av_scan: AVScanConfig = AVScanConfig()
    archive: ArchiveConfig = ArchiveConfig()
    extra_env: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_json(path: Path) -> "RunnerConfig":
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

# ---------- Core Steps ----------

def step_git_sync(cfg: RunnerConfig, log_path: Path) -> None:
    repo_dir = Path(cfg.git.repo_dir)
    ensure_dir(repo_dir)

    env = merge_env(os.environ, cfg.extra_env)

    # init if empty
    if not (repo_dir / ".git").exists():
        res = run_cmd(["git", "init"], cwd=repo_dir, env=env, log_file=log_path)
        if res.returncode != 0:
            raise RuntimeError(f"git init failed: {res.stderr}")

    # set origin
    run_cmd(["git", "remote", "remove", "origin"], cwd=repo_dir, env=env, log_file=log_path)
    res = run_cmd(["git", "remote", "add", "origin", cfg.git.remote_url], cwd=repo_dir, env=env, log_file=log_path)
    if res.returncode != 0:
        # ignore if already added by another process
        pass

    # fetch
    fetch_cmd = ["git", "fetch", "--prune"]
    if cfg.git.depth:
        fetch_cmd += [f"--depth={int(cfg.git.depth)}"]
    fetch_cmd += ["origin", cfg.git.branch]
    res = run_cmd(fetch_cmd, cwd=repo_dir, env=env, timeout=cfg.pytest.timeout, kill_after=cfg.pytest.kill_after, log_file=log_path)
    if res.returncode != 0:
        raise RuntimeError(f"git fetch failed: {res.stderr}")

    # checkout FETCH_HEAD
    res = run_cmd(["git", "checkout", "-f", "FETCH_HEAD"], cwd=repo_dir, env=env, log_file=log_path)
    if res.returncode != 0:
        raise RuntimeError(f"git checkout failed: {res.stderr}")

def step_install_deps(cfg: RunnerConfig, log_path: Path) -> None:
    if not cfg.deps.install:
        return
    req = cfg.deps.requirements_file
    if not req:
        return
    repo_dir = Path(cfg.git.repo_dir)
    req_path = repo_dir / req
    if not req_path.exists():
        raise FileNotFoundError(f"requirements file not found: {req_path}")
    # determine pip
    if cfg.deps.pip_executable:
        pip_cmd = [cfg.deps.pip_executable]
    else:
        py = cfg.pytest.python_executable or sys.executable
        pip_cmd = [py, "-m", "pip"]
    cmd = pip_cmd + ["install", "-r", str(req_path)]
    res = run_cmd(cmd, cwd=repo_dir, timeout=cfg.deps.timeout, kill_after=cfg.deps.kill_after, log_file=log_path)
    if res.returncode != 0:
        raise RuntimeError(f"pip install failed: {res.stderr}")

def step_pytest(cfg: RunnerConfig, log_path: Path) -> int:
    repo_dir = Path(cfg.git.repo_dir)
    py = cfg.pytest.python_executable or sys.executable

    cmd = [py, "-m", "pytest"]
    if cfg.pytest.xdist_workers:
        cmd += ["-n", str(cfg.pytest.xdist_workers)]
        if cfg.pytest.xdist_dist:
            cmd += ["--dist", cfg.pytest.xdist_dist]
    if cfg.pytest.junit_xml:
        junit_path = str(repo_dir / cfg.pytest.junit_xml)
        cmd += ["--junitxml", junit_path]
    cmd += cfg.pytest.additional_args or []

    tests_root = cfg.pytest.tests_root
    if tests_root:
        cmd.append(tests_root)

    env = merge_env(os.environ, cfg.extra_env)
    env = merge_env(env, cfg.pytest.env)

    res = run_cmd(
        cmd,
        cwd=repo_dir,
        env=env,
        timeout=cfg.pytest.timeout,
        kill_after=cfg.pytest.kill_after,
        log_file=log_path,
    )
    return res.returncode

def step_rerun_failed(cfg: RunnerConfig, log_path: Path) -> Optional[int]:
    if not cfg.rerun_failed.enabled or not cfg.rerun_failed.command:
        return None
    repo_dir = Path(cfg.git.repo_dir)
    res = run_cmd(
        cfg.rerun_failed.command,
        cwd=repo_dir,
        timeout=cfg.rerun_failed.timeout,
        kill_after=cfg.rerun_failed.kill_after,
        log_file=log_path,
    )
    return res.returncode

def step_av_scan(cfg: RunnerConfig, log_path: Path) -> Optional[int]:
    if not cfg.av_scan.enabled or not cfg.av_scan.paths:
        return None
    if which("clamscan") is None:
        write_text(log_path, "\n[WARN] clamscan not found; AV scan skipped\n")
        return None
    code = 0
    for p in cfg.av_scan.paths:
        res = run_cmd(
            ["clamscan", "-r", "--bell", p],
            timeout=cfg.av_scan.timeout,
            kill_after=cfg.av_scan.kill_after,
            log_file=log_path,
        )
        # clamscan returns 1 if a virus is found; we still log and continue
        if res.returncode != 0 and code == 0:
            code = res.returncode
    return code

def step_archive(cfg: RunnerConfig, ts: str, log_path: Path) -> Optional[Path]:
    if not cfg.archive.enabled:
        return None
    paths = [Path(p) for p in cfg.archive.paths if p]
    if not paths:
        return None
    out = Path(cfg.archive.output_zip or safe_join(cfg.log_dir, f"artifacts_{ts}.zip"))
    out.parent.mkdir(parents=True, exist_ok=True)
    # Build zip
    import zipfile
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in paths:
            p = p.resolve()
            if p.is_file():
                z.write(p, arcname=p.name)
            elif p.is_dir():
                for root, _, files in os.walk(p):
                    for f in files:
                        fp = Path(root) / f
                        z.write(fp, arcname=str(Path(p.name) / fp.relative_to(p)))
    # also include main log
    if log_path.exists():
        with zipfile.ZipFile(out, "a", compression=zipfile.ZIP_DEFLATED) as z:
            z.write(log_path, arcname=log_path.name)
    return out

# ---------- Public API ----------

def run_pipeline(config_path: str) -> int:
    """
    Execute the pipeline using settings from JSON file.
    Returns overall exit code (0 = success, non-zero otherwise).
    """
    cfg = RunnerConfig.from_json(Path(config_path))

    ts = now_ts()
    log_dir = Path(cfg.log_dir)
    ensure_dir(log_dir)
    log_path = log_dir / f"run_{ts}.log"
    write_text(log_path, f"== Start run {ts} ==\n")

    overall_status = 0
    try:
        step_git_sync(cfg, log_path)
        write_text(log_path, "[OK] Git sync completed\n")

        step_install_deps(cfg, log_path)
        write_text(log_path, "[OK] Dependencies step completed (or skipped)\n")

        rc = step_pytest(cfg, log_path)
        write_text(log_path, f"[INFO] pytest exit code: {rc}\n")
        if rc != 0:
            overall_status = rc
            # optional rerun
            rrc = step_rerun_failed(cfg, log_path)
            if rrc is not None:
                write_text(log_path, f"[INFO] rerun_failed exit code: {rrc}\n")
                overall_status = rrc if rrc != 0 else 0

        avc = step_av_scan(cfg, log_path)
        if avc is not None:
            write_text(log_path, f"[INFO] AV scan exit code: {avc}\n")
            if overall_status == 0 and avc != 0:
                overall_status = avc

        artifact = step_archive(cfg, ts, log_path)
        if artifact:
            write_text(log_path, f"[OK] Artifacts archived to: {artifact}\n")

    except Exception as e:
        write_text(log_path, f"[ERROR] {type(e).__name__}: {e}\n")
        # non-zero
        return 1

    write_text(log_path, f"== Finish run {now_ts()} (status={overall_status}) ==\n")
    return int(overall_status)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cross_platform_test_runner.py <config.json>")
        sys.exit(2)
    sys.exit(run_pipeline(sys.argv[1]))
