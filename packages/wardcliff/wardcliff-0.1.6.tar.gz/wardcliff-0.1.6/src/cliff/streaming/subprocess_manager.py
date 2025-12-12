"""
Subprocess management for the Ink UI process.

Handles launching, monitoring, and terminating the Bun-based Ink terminal UI.
"""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class InkSubprocess:
    """
    Manages the Ink/Bun subprocess lifecycle.

    Spawns the Ink terminal UI as a child process and manages
    the stdio pipes for JSON-RPC communication.
    """

    def __init__(
        self,
        ui_dir: Optional[Path] = None,
        runner: Optional[str] = None,
    ):
        """
        Initialize the subprocess manager.

        Args:
            ui_dir: Path to the ui/ directory containing the Ink app.
                    Defaults to project_root/ui
            runner: Package runner to use ("bun", "npm", or auto-detected)
        """
        self.ui_dir = ui_dir or self._find_ui_dir()
        self.runner = runner or self._find_runner()
        self.process: Optional[subprocess.Popen] = None
        self._read_task: Optional[asyncio.Task] = None

    def _find_ui_dir(self) -> Path:
        """Find the ui/ directory relative to the package."""
        # Check multiple possible locations
        candidates = [
            # Relative to this file (development)
            Path(__file__).parent.parent.parent.parent / "ui",
            # Relative to cwd
            Path.cwd() / "ui",
            # Cached in user directory
            Path.home() / ".wardcliff" / "ui",
        ]

        for candidate in candidates:
            if candidate.exists() and (candidate / "package.json").exists():
                return candidate

        # Return default even if not found (will error on start)
        return candidates[0]

    def _find_runner(self) -> str:
        """Find an available package runner (bun or npm)."""
        # Prefer bun if available
        bun_in_path = shutil.which("bun")
        if bun_in_path:
            return "bun"

        # Check common bun installation locations
        home = Path.home()
        bun_candidates = [
            home / ".bun" / "bin" / "bun",
            Path("/usr/local/bin/bun"),
            Path("/opt/homebrew/bin/bun"),
        ]

        for candidate in bun_candidates:
            if candidate.exists():
                return "bun"

        # Fall back to npm if available
        npm_in_path = shutil.which("npm")
        if npm_in_path:
            return "npm"

        # Default to npm and let it fail with a helpful error
        return "npm"

    async def start(self) -> subprocess.Popen:
        """
        Start the Ink subprocess.

        Returns:
            The Popen object for the subprocess
        """
        if self.process is not None:
            raise RuntimeError("Ink subprocess already running")

        # Verify ui directory exists
        if not self.ui_dir.exists():
            raise FileNotFoundError(
                f"UI directory not found: {self.ui_dir}\n"
                "Make sure the Ink UI has been installed."
            )

        # Verify package.json exists
        package_json = self.ui_dir / "package.json"
        if not package_json.exists():
            raise FileNotFoundError(
                f"package.json not found in: {self.ui_dir}\n"
                "The UI directory appears to be incomplete."
            )

        # Set up environment
        env = os.environ.copy()
        env["NODE_ENV"] = "production"
        # Disable Bun's auto-update checks
        env["BUN_NO_UPDATE_NOTIFIER"] = "1"
        # Force color output for Ink
        env["FORCE_COLOR"] = "1"

        logger.info("Starting Ink UI from %s with %s", self.ui_dir, self.runner)

        try:
            self.process = subprocess.Popen(
                [self.runner, "run", "start"],
                cwd=str(self.ui_dir),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                bufsize=0,  # Unbuffered for real-time communication
            )
        except FileNotFoundError as e:
            raise RuntimeError(
                f"Could not start Ink UI. Neither Bun nor npm found.\n"
                f"Install Node.js: https://nodejs.org/\n"
                f"Or install Bun: curl -fsSL https://bun.sh/install | bash\n"
                f"Error: {e}"
            ) from e

        logger.info("Ink subprocess started with PID %d", self.process.pid)
        return self.process

    async def stop(self, timeout: float = 5.0) -> None:
        """
        Gracefully stop the subprocess.

        Args:
            timeout: Seconds to wait before force-killing
        """
        if self.process is None:
            return

        logger.info("Stopping Ink subprocess")

        # Cancel any read task
        if self._read_task is not None:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass
            self._read_task = None

        # Try graceful termination first
        self.process.terminate()

        try:
            # Wait for process to exit
            loop = asyncio.get_event_loop()
            await asyncio.wait_for(
                loop.run_in_executor(None, self.process.wait),
                timeout=timeout,
            )
            logger.info("Ink subprocess terminated gracefully")
        except asyncio.TimeoutError:
            # Force kill if it doesn't exit in time
            logger.warning("Ink subprocess did not terminate, killing")
            self.process.kill()
            await loop.run_in_executor(None, self.process.wait)

        self.process = None

    async def wait(self) -> int:
        """
        Wait for the subprocess to exit.

        Returns:
            The exit code of the subprocess
        """
        if self.process is None:
            raise RuntimeError("No subprocess running")

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.process.wait)

    @property
    def stdin(self) -> Optional[subprocess.PIPE]:
        """Get the subprocess stdin pipe."""
        return self.process.stdin if self.process else None

    @property
    def stdout(self) -> Optional[subprocess.PIPE]:
        """Get the subprocess stdout pipe."""
        return self.process.stdout if self.process else None

    @property
    def stderr(self) -> Optional[subprocess.PIPE]:
        """Get the subprocess stderr pipe."""
        return self.process.stderr if self.process else None

    @property
    def is_running(self) -> bool:
        """Check if the subprocess is still running."""
        if self.process is None:
            return False
        return self.process.poll() is None

    async def stream_stderr(self) -> None:
        """
        Stream stderr from the subprocess to the logger.

        Should be started as an asyncio task to capture any error output.
        """
        if self.process is None or self.process.stderr is None:
            return

        loop = asyncio.get_event_loop()

        while self.is_running:
            try:
                line = await loop.run_in_executor(
                    None, self.process.stderr.readline
                )
                if not line:
                    break

                text = line.decode("utf-8").strip()
                if text:
                    logger.warning("[Ink stderr] %s", text)
            except Exception:
                break


class InkProcessError(Exception):
    """Raised when there's an error with the Ink subprocess."""
    pass
