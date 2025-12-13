import os
from ..utils.util import randstr
from ..utils.log import *
import aiohttp
import asyncio
import requests
from typing import Dict, Any, TypedDict, Optional

__all__ = ['Payload', 'send', 'async_send', 'Register']

_APP_NAME = os.getenv("APP_NAME", "ieops")
_MODEL_SERVER_SOCKET = os.getenv("MODEL_SERVER_SOCKET", f"{_APP_NAME}.sock")
_IEOPS_PROXY_URL = os.getenv("IEOPS_PROXY_URL", "http://10.146.0.6:30054/api/model")
_MODEL_THREAD_CONCURRENCY = os.getenv("MODEL_THREAD_CONCURRENCY", "8")
_REGISTER_INTERVAL = os.getenv("REGISTER_INTERVAL", 10)
_REGISTER_ENABLED = os.getenv("REGISTER_ENABLED", "true")

# async connector (lazy init)
_CONNECTOR: Optional[aiohttp.TCPConnector] = None

# sync session (lazy init)
_SYNC_SESSION: Optional[requests.Session] = None


class Payload(TypedDict):
    path: str
    payload: Dict[str, Any]


def _get_async_connector() -> aiohttp.TCPConnector:
    """lazy init async connector (needs to be called in event loop)"""
    global _CONNECTOR
    if _CONNECTOR is None:
        _CONNECTOR = aiohttp.TCPConnector()
    return _CONNECTOR


def _get_sync_session() -> requests.Session:
    global _SYNC_SESSION
    if _SYNC_SESSION is None:
        _SYNC_SESSION = requests.Session()
    return _SYNC_SESSION


def send(_payload: Payload) -> Optional[Exception]:
    """send request to IEOPS proxy"""
    try:
        session = _get_sync_session()
        url = f"{_IEOPS_PROXY_URL}/{_payload['path']}"
        resp = session.post(url, json=_payload['payload'], timeout=0.8)
        if resp.status_code == 200:
            uvicorn_logger.info(f"Client send request to [{_payload['path']}] success")
            return None
        return Exception(f"Client send request to [{_payload['path']}] failed: {resp.status_code}")
    except requests.Timeout as e:
        uvicorn_logger.warning(f"Client send request to [{_payload['path']}] timeout: {e}")
        return e
    except requests.RequestException as e:
        uvicorn_logger.warning(f"Client send request to [{_payload['path']}] failed: {e}")
        return e


async def async_send(_payload: Payload) -> Optional[Exception]:
    """async send request to IEOPS proxy"""
    err = None
    try:
        url = f"{_IEOPS_PROXY_URL}/{_payload['path']}"
        client_timeout = aiohttp.ClientTimeout(total=0.8)
        async with aiohttp.ClientSession(
            connector=_get_async_connector(), 
            connector_owner=False,
            timeout=client_timeout
        ) as session:
            async with session.post(url, json=_payload['payload']) as resp:
                if resp.status == 200:
                    # uvicorn_logger.info(f"Client send request to [{_payload['path']}] success")
                    return None
                err = Exception(f"Client send request to [{_payload['path']}] failed: {resp.status}")
    except asyncio.TimeoutError:
        uvicorn_logger.warning(f"Client send request to [{_payload['path']}] timeout")
        err = Exception(f"Request timeout after 0.8s")
    except aiohttp.ClientError as e:
        uvicorn_logger.warning(f"Client send request to [{_payload['path']}] failed: {e}")
        err = e
    except asyncio.CancelledError:
        uvicorn_logger.info("Client stopped")
        raise
    return err


class Register:
    def __init__(self):
        self._appinfo = self._app_info()
        
    def _app_info(self):
        self._tokens = [randstr(8) for _ in range(int(_MODEL_THREAD_CONCURRENCY))]
        return {
            "app": _APP_NAME,
            "server_socket": _MODEL_SERVER_SOCKET,
            "tokens": self._tokens,
        }

    async def register(self):
        if _REGISTER_ENABLED.lower() == "false":
            uvicorn_logger.info("Register is disabled, skipping...")
            return
        uvicorn_logger.info("Registering {} to IEOPS proxy...".format(_APP_NAME))
        try:
            while True:
                await async_send(Payload(path="register", payload=self._appinfo))
                await asyncio.sleep(int(_REGISTER_INTERVAL))
        except asyncio.CancelledError:
            uvicorn_logger.info("Register stopped")
            raise
        finally:
            if _CONNECTOR is not None:
                await _CONNECTOR.close()
            if _SYNC_SESSION is not None:
                _SYNC_SESSION.close()
