import os, secrets, socket, subprocess, sys, time, urllib.request
from pathlib import Path

LEMOND_DIR = Path(__file__).parent / "vendor" / "lemonade"
LEMOND_BIN = LEMOND_DIR / ("lemond.exe" if sys.platform == "win32" else "lemond")

def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

def start_lemond(retries: int = 3) -> tuple[subprocess.Popen, str, int]:
    last_err: Exception | None = None
    for _ in range(retries):
        port = _free_port()
        key = secrets.token_urlsafe(32)
        env = {**os.environ, "LEMONADE_API_KEY": key}
        proc = subprocess.Popen(
            [str(LEMOND_BIN), str(LEMOND_DIR), str(LEMOND_DIR), "--host", "127.0.0.1", "--no-broadcast", "--port", str(port)],
            env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        try:
            _wait_for_health(port, key, timeout_s=30)
            return proc, key, port
        except RuntimeError as e:
            stop_lemond(proc)
            proc.wait()
            last_err = e
    raise RuntimeError(f"lemond failed to start after {retries} attempts") from last_err

def _wait_for_health(port: int, key: str, timeout_s: int) -> None:
    url = f"http://127.0.0.1:{port}/api/v1/health"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(req, timeout=1) as r:
                if r.status == 200:
                    return
        except Exception:
            time.sleep(0.25)
    raise RuntimeError(f"lemond on port {port} did not become healthy within {timeout_s}s")


def stop_lemond(proc):
    """Encerra a árvore privada: o backend llama-server também é um subprocesso."""
    if sys.platform == 'win32':
        subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    elif proc.poll() is None:
        proc.terminate()
    if proc.poll() is None:proc.wait(timeout=15)
