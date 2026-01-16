from __future__ import annotations

import logging
import psutil
import ctypes
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def describe_top_processes(limit: int = 5) -> str:
    procs: List[psutil.Process] = []
    for p in psutil.process_iter(attrs=["pid", "name", "cpu_percent"]):
        try:
            # Trigger CPU percent measurement
            p.cpu_percent(interval=None)
            procs.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Wait a bit and re-measure
    psutil.cpu_percent(interval=0.2)
    for p in procs:
        try:
            p.info["cpu_percent"] = p.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            p.info["cpu_percent"] = 0.0

    procs_sorted = sorted(procs, key=lambda p: p.info.get("cpu_percent", 0), reverse=True)
    lines = []
    for p in procs_sorted[:limit]:
        info = p.info
        lines.append(f"PID {info['pid']} {info['name']} – CPU {info.get('cpu_percent', 0):.1f}%")
    if not lines:
        return "I couldn't read any process information."
    summary = "Top processes by CPU usage:\n" + "\n".join(lines)
    logger.info(summary)
    return summary

def kill_process(pid: int) -> str:
    try:
        proc = psutil.Process(pid)
        name = proc.name()
        proc.terminate()
        logger.warning("Terminated process %s (PID %s).", name, pid)
        return f"I terminated process {name} (PID {pid})."
    except psutil.NoSuchProcess:
        msg = f"Process with PID {pid} no longer exists."
        logger.info(msg)
        return msg
    except Exception as e:
        logger.exception("Failed to kill process %s: %s", pid, e)
        return f"I couldn't terminate process {pid}: {e}"

def lock_workstation() -> str:
    try:
        ctypes.windll.user32.LockWorkStation()
        logger.warning("Workstation locked by Malcolm Guardian.")
        return "I've locked your workstation."
    except Exception as e:
        logger.exception("Failed to lock workstation: %s", e)
        return f"I couldn't lock the workstation: {e}"

def execute_tool(tool: str, args: Dict[str, Any]) -> str:
    """Dispatch a tool call and return a human-readable summary."""
    logger.info("Executing tool: %s with args %s", tool, args)
    if tool == "describe_top_processes":
        return describe_top_processes(limit=int(args.get("limit", 5)))
    if tool == "kill_process":
        return kill_process(pid=int(args["pid"]))
    if tool == "lock_workstation":
        return lock_workstation()
    if tool == "enter_quiet_mode":
        return "Entering quiet mode."
    if tool == "exit_quiet_mode":
        return "Exiting quiet mode."
    return f"I don't know how to execute tool '{tool}'."
