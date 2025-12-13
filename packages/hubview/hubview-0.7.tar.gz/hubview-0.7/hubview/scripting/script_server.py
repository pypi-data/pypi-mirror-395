import subprocess
import threading
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Union
from flask import abort
import signal


class ScriptRunner:
    """
    Generic runner for Python or shell commands.
    - Starts each command in its own process group.
    - stop() terminates the whole group (children included).
    """
    def __init__(
        self,
        cmd: List[str],
        log_file: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        name: str = "",
        stop_timeout: float = 3.0,
    ):
        self.cmd = cmd
        self.log_file = log_file
        self.cwd = cwd
        self.env = env
        self.name = name
        self.stop_timeout = stop_timeout

        self.process: Optional[subprocess.Popen] = None
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        self._stop_requested = threading.Event()

    def start(self) -> str:
        with self.lock:
            if self.process is not None and self.process.poll() is None:
                return "Already running"

            self._stop_requested.clear()

            def run():
                proc: Optional[subprocess.Popen] = None
                try:
                    os.makedirs(os.path.dirname(self.log_file) or ".", exist_ok=True)

                    with open(self.log_file, "a", buffering=1, encoding="utf-8") as log:
                        popen_kwargs: Dict[str, Any] = dict(
                            stdout=log,
                            stderr=subprocess.STDOUT,
                            bufsize=1,
                            text=True,
                            cwd=self.cwd,
                            env=(os.environ | self.env) if self.env else None,
                        )

                        if os.name != "nt":
                            # new session => new process group (killable as a unit)
                            popen_kwargs["start_new_session"] = True
                        else:
                            # windows process group
                            popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP

                        proc = subprocess.Popen(self.cmd, **popen_kwargs)

                        with self.lock:
                            self.process = proc

                        # Wait for completion or stop request
                        while True:
                            if self._stop_requested.is_set():
                                break
                            if proc.poll() is not None:
                                break
                            time.sleep(0.1)

                        # stop escalation (group kill)
                        if self._stop_requested.is_set() and proc.poll() is None:
                            self._terminate_group(proc)

                finally:
                    with self.lock:
                        self.process = None

            self.thread = threading.Thread(target=run, daemon=True)
            self.thread.start()
            return "Started"

    def _terminate_group(self, proc: subprocess.Popen):
        if os.name != "nt":
            # POSIX: kill the whole process group
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                return

            try:
                proc.wait(timeout=self.stop_timeout)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()
        else:
            # Windows: terminate parent, then hard kill if needed
            proc.terminate()
            try:
                proc.wait(timeout=self.stop_timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()

    def stop(self) -> str:
        with self.lock:
            proc = self.process
            if proc is None or proc.poll() is not None:
                self.process = None
                return "Not running"
            self._stop_requested.set()

        # Nudge stop immediately (thread will also enforce)
        if proc.poll() is None:
            self._terminate_group(proc)

        return "Stopping"

    def is_running(self) -> bool:
        with self.lock:
            return self.process is not None and self.process.poll() is None

    def get_output(self, last_n: int = 50) -> str:
        if not os.path.exists(self.log_file):
            return ""

        lines: List[bytes] = []
        with open(self.log_file, "rb") as f:
            f.seek(0, os.SEEK_END)
            pos = f.tell()
            buf = bytearray()
            while pos > 0 and len(lines) <= last_n:
                step = min(1024, pos)
                pos -= step
                f.seek(pos)
                buf[:0] = f.read(step)
                lines = buf.splitlines()

        tail = lines[-last_n:]
        text = "\n".join(line.decode("utf-8", errors="replace") for line in tail)
        return text + ("\n" if text else "")
@dataclass
class ScriptSpec:
    """
    One script entry. You can specify either:
      - cmd: explicit command list, OR
      - python + path (+ args) for convenience.
    """
    log: str
    cmd: Optional[List[str]] = None
    python: Optional[str] = None
    path: Optional[str] = None
    args: List[str] = field(default_factory=list)
    cwd: Optional[str] = None
    env: Optional[Dict[str, str]] = None


class ScriptManager:
    def __init__(self, scripts_dict: Dict[str, dict]):
        self.specs: Dict[str, ScriptSpec] = {}
        self.runners: Dict[str, ScriptRunner] = {}

        for name, cfg in scripts_dict.items():
            spec = ScriptSpec(
                log=cfg["log"],
                cmd=cfg.get("cmd"),
                python=cfg.get("python"),
                path=cfg.get("path"),
                args=list(cfg.get("args", [])),
                cwd=cfg.get("cwd"),
                env=cfg.get("env"),
            )

            # Build cmd if not provided
            if spec.cmd is None:
                if not spec.path:
                    raise ValueError(f"Script '{name}' must define either cmd or path.")
                py = spec.python or sys.executable
                spec.cmd = [py]
                # add "-u" automatically for python scripts
                if os.path.splitext(spec.path)[1].lower() == ".py":
                    spec.cmd += ["-u", spec.path]
                else:
                    # non-python "path" means "execute directly"
                    spec.cmd += [spec.path]
                spec.cmd += spec.args

            self.specs[name] = spec
            self.runners[name] = ScriptRunner(
                cmd=spec.cmd,
                log_file=spec.log,
                cwd=spec.cwd,
                env=spec.env,
                name=name,
            )

    def names(self):
        return sorted(self.runners.keys())

    def get(self, name: str) -> ScriptRunner:
        if name not in self.runners:
            abort(404)
        return self.runners[name]

    def spec(self, name: str) -> ScriptSpec:
        if name not in self.specs:
            abort(404)
        return self.specs[name]
