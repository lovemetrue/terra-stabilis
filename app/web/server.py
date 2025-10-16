from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import uvicorn
import asyncio
import os
import signal
import socket
import subprocess

from app.config import settings
# FastAPI сервер больше не нужен - используем Django Rocket
# Этот файл можно удалить или оставить для совместимости


def _is_port_in_use(port: int, host: str = "0.0.0.0") -> bool:
    """
    Проверяет, занят ли TCP-порт.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def _kill_processes_on_port(port: int) -> None:
    """
    Пытается завершить процессы, занимающие указанный порт (macOS/Linux).
    Использует lsof для нахождения PID и отправляет SIGTERM, затем при необходимости SIGKILL.
    """
    try:
        result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        pids = [int(pid) for pid in result.stdout.strip().splitlines() if pid.strip()]
        for pid in pids:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                continue
        if pids:
            # Даём времени корректно завершиться
            try:
                asyncio.run(asyncio.sleep(0.5))
            except RuntimeError:
                pass
        # Проверяем ещё раз и, если нужно, отправляем SIGKILL
        result2 = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        pids2 = [int(pid) for pid in result2.stdout.strip().splitlines() if pid.strip()]
        for pid in pids2:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                continue
    except FileNotFoundError:
        # lsof недоступен — пропускаем «убийство», обработаем ниже сменой порта
        pass


async def start_web_server() -> None:
    port = settings.ADMIN_PORT
    if _is_port_in_use(port):
        _kill_processes_on_port(port)
        # Если всё ещё занят, сдвигаем порт на следующий свободный
        if _is_port_in_use(port):
            original = port
            for candidate in range(original + 1, original + 50):
                if not _is_port_in_use(candidate):
                    port = candidate
                    break
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


__all__ = ["app", "start_web_server"]
