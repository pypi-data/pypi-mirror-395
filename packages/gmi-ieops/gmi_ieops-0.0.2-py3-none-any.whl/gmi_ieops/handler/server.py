# pyright: strict, reportUnusedFunction=false, reportUnknownVariableType=false
import queue
from typing import Any, AsyncGenerator, Generator, Callable, Optional, Dict, List
from typing_extensions import TypedDict
from concurrent.futures import ThreadPoolExecutor
import json
import time
import os
import asyncio
from ..utils.log import *
from .tokenizer import TokenizerPool
import inspect
import threading
import traceback
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from abc import ABC, abstractmethod

ENGINE_READY : bool = False

SERVER_CODE_OK = 0
SERVER_CODE_ERROR = 1
SERVER_CODE_STOP = 2

_APP_NAME = os.getenv("APP_NAME", "ieops")

_MODEL_SERVER_SOCKET = os.getenv("MODEL_SERVER_SOCKET", f"{_APP_NAME}.sock")
_MODEL_SERVER_PORT = os.getenv("MODEL_SERVER_PORT", 8001)
_MODEL_SERVER_HOST = os.getenv("MODEL_SERVER_HOST", "127.0.0.1")

_THREAD_CONCURRENCY = os.getenv("MODEL_THREAD_CONCURRENCY", "8")
_MODEL_GRPC_PORT = os.getenv("MODEL_GRPC_PORT", 8001)
_MODEL_TIMEOUT = os.getenv("MODEL_TIMEOUT", 600)
_GRACEFUL_SHUTDOWN_TIME = os.getenv("GRACEFUL_SHUTDOWN_TIME", 3)
_MAX_MESSAGE_LENGTH = os.getenv("MAX_MESSAGE_LENGTH", 10*1024*1024)


class ModelError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class QueueItem(TypedDict):
    code: int
    data: bytes


class Server(ABC):
    @abstractmethod
    def shutdown(self) -> None:
        """request server graceful shutdown"""
    @abstractmethod
    async def serve(self) -> None:
        """serve the server"""


class OpenAIServer(Server):
    def __init__(self, func: Callable[[Any], Generator[Any, bool, None]], abort : Optional[Callable[[str], None]] = None) -> None:
        self._func = func
        self._cancelled_events : Dict[str,bool] = {}
        self._abort = abort
        self._executor = ThreadPoolExecutor(max_workers = int(_THREAD_CONCURRENCY) * 2 + 3)
        self._app=FastAPI(lifespan=self._lifespan)
        self._server: Optional[uvicorn.Server] = None
        self._setup_routes()
        
    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        # start
        uvicorn_logger.info("Server starting...")
        yield
        # clean up when shutting down
        uvicorn_logger.info("Server shutting down...")
        # cancel all in-progress requests
        for trace_id in list(self._cancelled_events.keys()):
            self._cancelled_events[trace_id] = True
        # give in-progress requests a chance to complete (optional)
        await asyncio.sleep(0.5)  # wait for 0.5 seconds to let requests have a chance to check the cancel flag
        self._executor.shutdown(wait=True)
        try:
            TokenizerPool(None).shutdown(wait=True)
        except Exception as e:
            uvicorn_logger.error(f"Error shutting down TokenizerPool: {e}")
    
    def shutdown(self) -> None:
        """request server graceful shutdown"""
        if self._server:
            self._server.should_exit = True

    async def serve(self) -> None:
        # configure uvicorn
        if _MODEL_SERVER_SOCKET:
            config = uvicorn.Config(
                self._app,
                uds=_MODEL_SERVER_SOCKET,
                log_level="info",
                loop="asyncio",
                timeout_graceful_shutdown=int(_GRACEFUL_SHUTDOWN_TIME)  # graceful shutdown timeout
            )
        else:
            config = uvicorn.Config(
                self._app,
                host=_MODEL_SERVER_HOST,
                port=int(_MODEL_SERVER_PORT),
                log_level="info",
                loop="asyncio",
                timeout_graceful_shutdown=int(_GRACEFUL_SHUTDOWN_TIME)  # graceful shutdown timeout
            )
        
        self._server = uvicorn.Server(config)
        await self._server.serve()

    def _setup_routes(self) -> None:
        """set API endpoints"""
        @self._app.get("/")
        async def root():
            """Root endpoint with basic info"""
            return {
                "message": "vLLM Load Balancing Server",
                "status": "ready" if ENGINE_READY else "initializing",
                "endpoints": {
                    "health": "/ping",
                    "generate": "/v1/completions",
                    "chat": "/v1/chat/completions"
                }
            }
        @self._app.get("/health")
        async def health():
            return {"status": "ok"}
        
        @self._app.post("/sse/infer")
        async def infer_sse(request: Request):
            body = await request.body()
            return StreamingResponse(
                self._sse_generator(body),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                }
            )
        
        @self._app.post("/infer")
        async def infer(request: Request):
            """non-streaming interface, return complete JSON response"""
            body = await request.body()
            results: List[Any] = []
            last_code = SERVER_CODE_OK
            async for item in self._generator(body):
                code = item["code"]
                data = item["data"]
                if isinstance(data, bytes):
                    data = data.decode("utf-8")
                if code == SERVER_CODE_ERROR:
                    last_code = code
                    results.append({"error": data})
                    break
                if code == SERVER_CODE_STOP:
                    break
                try:
                    results.append(json.loads(data))
                except json.JSONDecodeError:
                    results.append(data)
            return {"code": last_code, "results": results}

    async def _sse_generator(self, request: bytes) -> AsyncGenerator[str, None]:
        """SSE response generator"""
        async for item in self._generator(request):
            code = item["code"]
            data = item["data"]
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            yield f"{json.dumps({'code': code, 'data': data}, ensure_ascii=False)}\n\n"

    async def _generator(self, request: bytes) -> AsyncGenerator[Dict[str, Any], None]: 
        start = int(time.time() * 1000)
        loop = asyncio.get_event_loop()
        headers: Dict[str, str] = {}
        payload: Any = None
        try:
            request_data = json.loads(request.decode("utf-8"))
            headers = request_data.get("headers", {})
            payload = request_data.get("payload", request_data)  # compatible with old format
        except json.JSONDecodeError:
            # 如果不是 JSON，当作纯 payload 处理
            payload = request.decode("utf-8")
            
        trace_id: str = str(headers.get("x-trace-id", "traceid-" + await arandstr(8)))
        log.get_logger(trace_id=trace_id).info("query size: {}", len(payload) if isinstance(payload, (str, bytes)) else len(json.dumps(payload)))
        # 如果 payload 已经是 dict，直接使用；否则解析 JSON
        query: Dict[str, Any] = payload if isinstance(payload, dict) else json.loads(payload)
        query['trace_id'] = trace_id
        if trace_id in self._cancelled_events:
            log.get_logger(trace_id=trace_id).warning("trace_id already exists")
            yield {"code": SERVER_CODE_ERROR, "data": f"{trace_id} already exists".encode("utf-8")}
            return
        self._cancelled_events[trace_id] = False
        all_data : List[Any] = []
        try:
            if inspect.isasyncgenfunction(self._func):
                threading.Thread(target=self._time_counter, args=(trace_id, int(_MODEL_TIMEOUT))).start()
                async for v in self._func(query):
                    if self._cancelled_events[trace_id]:
                        del self._cancelled_events[trace_id]
                        if self._abort is not None:
                            await self._abort(trace_id) # type: ignore
                        raise asyncio.TimeoutError
                    if v is None:
                        break
                    if isinstance(v, ModelError):
                        yield {"code": SERVER_CODE_ERROR, "data": v.message.encode("utf-8")}
                        all_data.append(" [ model error: "+v.message+" ]")
                        break
                    if "results" in v:
                        for ret in v["results"]:
                            all_data.append(ret["content"])
                    yield {"code": SERVER_CODE_OK, "data": json.dumps(v, ensure_ascii=False).encode("utf-8")}
            else:
                q : "queue.Queue[QueueItem]" = queue.Queue()
                # await loop.run_in_executor(self._executor, self._cancelled_events[token].clear)
                await asyncio.wait_for(loop.run_in_executor(self._executor, self._func_caller, trace_id, query, q), int(_MODEL_TIMEOUT)//10) # type: ignore
                while True:
                    v:Any = await loop.run_in_executor(self._executor, q.get)
                    if v['code'] == SERVER_CODE_STOP:
                        yield {"code": SERVER_CODE_STOP, "data": b""}
                        break
                    if v['code'] == SERVER_CODE_ERROR:
                        yield {"code": SERVER_CODE_ERROR, "data": json.dumps(v, ensure_ascii=False).encode("utf-8")}
                        break
                    yield {"code": SERVER_CODE_OK, "data": json.dumps(v, ensure_ascii=False).encode("utf-8")}
        except asyncio.CancelledError as e:
            log.get_logger(trace_id=trace_id).error("cancelled: {}", e)
            yield {"code": SERVER_CODE_ERROR, "data": b"cancelled"} 
        except asyncio.TimeoutError as e:
            log.get_logger(trace_id=trace_id).error("timeout: {}", e)
            yield {"code": SERVER_CODE_ERROR, "data": b"timeout"}
        except Exception as e:
            log.get_logger(trace_id=trace_id).error("error: {}\n{}", e, traceback.format_exc())
            try:
                yield {"code": SERVER_CODE_ERROR, "data": traceback.format_exc().encode("utf-8")}
            except Exception as e:
                log.get_logger(trace_id=trace_id).error("error: {}\n{}", e, traceback.format_exc().encode("utf-8"))
        finally:
            log.get_logger(trace_id=trace_id).info("all responses length: {}, cost: {}ms", len(all_data), int(time.time() * 1000) - start)
            # await loop.run_in_executor(self._executor, self._cancelled_events[token].set)
            if trace_id in self._cancelled_events:
                self._cancelled_events[trace_id] = True
            log.get_logger(trace_id=trace_id).info("all content: {}", "".join(all_data))

    def _func_caller(self, trace_id: str, payload: Dict[str, Any], q: "queue.Queue[QueueItem]"):
        try:
            it = self._func(payload)
            if not hasattr(it, "send"):
                # 不是生成器
                q.put(QueueItem(code=SERVER_CODE_OK, data=json.dumps(it, ensure_ascii=False).encode("utf-8")))
                q.put(QueueItem(code=SERVER_CODE_STOP, data=b""))
                return
            v = it.send(None) # pyright: ignore
            while True:
                q.put(QueueItem(code=SERVER_CODE_OK, data=json.dumps(v, ensure_ascii=False).encode("utf-8")))
                if self._cancelled_events[trace_id]:
                    try:
                        v = it.send(True)
                    except StopIteration:
                        break
                    break
                else:
                    try:
                        v = it.send(False)
                    except StopIteration:
                        break
        except Exception:
            # TODO: log exception here
            log.get_logger(trace_id=trace_id).error("error: {}", traceback.format_exc())
            q.put(QueueItem(code=SERVER_CODE_ERROR, data=traceback.format_exc().encode("utf-8")))
        else:
            # put none to stop the loop
            q.put(QueueItem(code=SERVER_CODE_STOP, data=b""))
        finally:
            log.get_logger(trace_id=trace_id).info("func_caller finished")
            del self._cancelled_events[trace_id]

    def _time_counter(self, trace_id : str, timeout: int):
        for _ in range(timeout):
            if self._cancelled_events[trace_id]:
                log.get_logger(trace_id=trace_id).info("time counter stop") # type: ignore
                del self._cancelled_events[trace_id]
                return
            time.sleep(0.1)
        self._cancelled_events[trace_id] = True


class ComfyUIServer(Server):
    def __init__(self) -> None:
        raise NotImplementedError("ComfyUIServer is not implemented")

    def shutdown(self) -> None:
        """request server graceful shutdown"""
        pass

    async def serve(self) -> None:
        """serve the server"""
        pass


__all__ = ["Server", "OpenAIServer", "ComfyUIServer", "ENGINE_READY", "ModelError"]