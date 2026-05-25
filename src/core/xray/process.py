from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
from typing import Any

from src.core.xray.config import XrayConfigError


class XrayProcessManager:
    def __init__(self, binary_path: str, config: dict[str, Any]):
        self.binary_path = Path(binary_path).expanduser().resolve()
        self.config = config
        self.process: subprocess.Popen[bytes] | None = None
        self.runtime_config_path: Path | None = None

    def start(self) -> None:
        if self.process is not None and self.process.poll() is None:
            return
        if not self.binary_path.is_file():
            raise FileNotFoundError(f"xray binary not found: {self.binary_path}")
        self.runtime_config_path = self._write_runtime_config()
        self._validate_runtime_config()
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        self.process = subprocess.Popen(
            [str(self.binary_path), "run", "-c", str(self.runtime_config_path)],
            cwd=str(self.binary_path.parent),
            stdin=subprocess.DEVNULL,
            creationflags=creationflags,
        )
        try:
            self.process.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            return
        raise RuntimeError(f"xray exited immediately with code {self.process.returncode}")

    def stop(self) -> None:
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)
        self.process = None
        self._cleanup_runtime_config()

    def _write_runtime_config(self) -> Path:
        temp_file = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            prefix="sni-spoofing-xray-",
            encoding="utf-8",
            newline="\n",
            delete=False,
        )
        with temp_file:
            json.dump(self.config, temp_file, ensure_ascii=True, indent=2)
            temp_file.write("\n")
        return Path(temp_file.name)

    def _validate_runtime_config(self) -> None:
        if self.runtime_config_path is None:
            raise RuntimeError("runtime xray config path is not initialized")
        result = subprocess.run(
            [str(self.binary_path), "run", "-test", "-c", str(self.runtime_config_path)],
            cwd=str(self.binary_path.parent),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode == 0:
            return
        self._cleanup_runtime_config()
        details = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
        raise XrayConfigError(f"xray rejected the generated config:\n{details}")

    def _cleanup_runtime_config(self) -> None:
        if self.runtime_config_path is not None:
            self.runtime_config_path.unlink(missing_ok=True)
            self.runtime_config_path = None


__all__ = ["XrayProcessManager"]
