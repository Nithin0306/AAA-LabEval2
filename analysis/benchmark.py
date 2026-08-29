"""
benchmark.py — Core utilities for running a compiled binary and
measuring wall-clock time and peak RSS memory.
"""

import subprocess
import time
import resource
import os
import tempfile


def run_impl(binary: str, input_str: str, timeout: float = 30.0) -> dict:
    """
    Run a compiled binary with the given stdin string.

    Returns a dict with:
        output      : str   — captured stdout
        time_ms     : float — wall-clock time in milliseconds
        memory_kb   : int   — peak RSS in kilobytes
        returncode  : int   — process exit code
    """
    binary = os.path.abspath(binary)
    encoded = input_str.encode()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".in") as tmp:
        tmp.write(encoded)
        tmp_path = tmp.name

    try:
        t0 = time.perf_counter()

        proc = subprocess.run(
            [binary],
            stdin=open(tmp_path, "rb"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )

        t1 = time.perf_counter()
        elapsed_ms = (t1 - t0) * 1000.0

        mem_kb = _peak_rss_kb(binary, tmp_path, timeout)

        return {
            "output": proc.stdout.decode(errors="replace"),
            "time_ms": elapsed_ms,
            "memory_kb": mem_kb,
            "returncode": proc.returncode,
        }

    finally:
        os.unlink(tmp_path)


def run_impl_repeated(binary: str, input_str: str, reps: int = 5, timeout: float = 30.0) -> dict:
    """
    Run the binary `reps` times and return the median time and memory.
    """
    results = [run_impl(binary, input_str, timeout) for _ in range(reps)]
    times = sorted(r["time_ms"] for r in results)
    mems = sorted(r["memory_kb"] for r in results)
    mid = reps // 2
    return {
        "output": results[0]["output"],
        "time_ms": times[mid],
        "memory_kb": mems[mid],
        "returncode": results[0]["returncode"],
    }


def _peak_rss_kb(binary: str, input_path: str, timeout: float) -> int:
    """
    Use /usr/bin/time -v to capture peak RSS.
    Falls back to 0 if unavailable.
    """
    try:
        proc = subprocess.run(
            ["/usr/bin/time", "-v", binary],
            stdin=open(input_path, "rb"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        stderr = proc.stderr.decode(errors="replace")
        for line in stderr.splitlines():
            if "Maximum resident set size" in line:
                return int(line.split(":")[-1].strip())
    except Exception:
        pass
    return 0
