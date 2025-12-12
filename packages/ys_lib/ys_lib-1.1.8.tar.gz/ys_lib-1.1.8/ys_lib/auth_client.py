# -*- coding: utf-8 -*-
import asyncio
import json
from typing import Any, Callable, Union
from loguru import logger
import websockets
import websockets.client


class AuthClient:
    def __init__(
        self,
        uri: str,
        generator: Callable,
        connect_callback: Union[Callable, None] = None,
        event_callback: Union[Callable, None] = None,
    ):
        assert uri and generator
        self.uri: str = uri
        self.generator: Callable = generator
        self.connect_callback: Union[Callable, None] = connect_callback
        self.event_callback: Union[Callable, None] = event_callback
        self.ws: websockets.client.WebSocketClientProtocol | None = None
        self.ready: asyncio.Event = asyncio.Event()
        self.app_id: str = ""
        self.conn_id: int = -1
        self.req_id: int = -1
        self.responses: dict[str, asyncio.Queue] = {}

        self.connect_task: asyncio.Task = asyncio.create_task(self.connect_ws())

    @property
    def request_id(self):
        self.req_id += 1
        return f"{self.conn_id}_{self.req_id}"

    async def connect_ws(self):
        while not self.ready.is_set():
            set_app_task: asyncio.Task | None = None
            ping_task: asyncio.Task | None = None
            try:
                logger.debug(f"connecting to AuthServer...")
                self.ws = await websockets.connect(  # type: ignore
                    uri=self.uri,
                    max_size=2**32 - 1,
                    max_queue=2**8,
                    # read_limit=2**32 - 1,
                    write_limit=2**32 - 1,
                    ssl=None,
                )
                logger.success(f"connected to AuthServer!")
                self.ready.set()
                if self.connect_callback:
                    await self.connect_callback(connected=True)
                while self.ready:
                    payload: dict | None = await self.recv()
                    if not payload:
                        continue
                    response_id: str | None = payload.get("response_id", None)
                    if response_id:
                        await self.responses[response_id].put(payload)
                    if payload.get("event") == "push_connection_id":
                        self.conn_id = payload.get("data").get("connection_id")  # type: ignore
                        self.req_id = -1
                        set_app_task = asyncio.create_task(self.set_app())
                        ping_task = asyncio.create_task(self.start_ping())
                        continue
                    if self.event_callback:
                        await self.event_callback(payload)
            except Exception as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
            finally:
                logger.warning("AuthServer disconnected")
                # 取消任务
                if ping_task:
                    ping_task.cancel()
                if set_app_task:
                    set_app_task.cancel()
                # 关闭连接
                if self.ws:
                    await self.ws.close()
                    self.ws = None
                self.ready.clear()
                self.app_id = ""
                if self.connect_callback:
                    await self.connect_callback(connected=False)
                await asyncio.sleep(3)
        # 取消重连
        self.connect_task.cancel()

    async def wait_response(self, request_id: str) -> tuple[Any, str]:
        error: str = ""
        data: Any = None
        try:
            rj: dict = await asyncio.wait_for(
                self.responses[request_id].get(), timeout=10
            )
            if rj.get("code") != 0:
                error = rj["message"]
            data: Any = rj.get("data")
        except Exception as e:
            error = e.__class__.__name__
        return error, data

    async def send(self, data: dict):
        try:
            if self.ws:
                message: str = json.dumps(data)
                # logger.info(f" send {message}")
                await self.ws.send(message)
                self.responses[data["request_id"]] = asyncio.Queue()
        except Exception as e:
            logger.error(f"[{e.__class__.__name__}]{e}")
            if self.ws:
                await self.ws.close()
                self.ws = None

    async def recv(self) -> dict | None:
        payload: str = await self.ws.recv()  # type: ignore
        try:
            if payload:
                # logger.debug(f"recv {payload}")
                return json.loads(payload)
        except Exception as e:
            logger.error(f"[{e.__class__.__name__}]{e}")
        return None

    async def login(self, info: dict) -> tuple[str, Any]:
        if not self.ready.is_set():
            return "鉴权模块未连接", None
        request_id: str = self.request_id
        data: dict = {"event": "login", "request_id": request_id, "data": info}
        await self.send(data)
        error, response = await self.wait_response(request_id)
        return error, response

    async def logout_by_session_id(self, info: dict) -> tuple[str, Any]:
        if not self.ready.is_set():
            return "鉴权模块未连接", None
        request_id: str = self.request_id
        data: dict = {
            "event": "logout_by_session_id",
            "request_id": request_id,
            "data": info,
        }
        await self.send(data)
        error, response = await self.wait_response(request_id)
        return error, response

    async def set_app(self):
        while not self.app_id:
            await self.ready.wait()
            request_id: str = self.request_id
            send_data: dict = {
                "request_id": request_id,
                "event": "set_app",
                "data": self.generator(),
            }
            await self.send(send_data)
            try:
                response: dict = await asyncio.wait_for(
                    self.responses[request_id].get(), timeout=3
                )
                code: int | None = response.get("code")
                data: dict | None = response.get("data")
                if code == 0 and data:
                    self.app_id = data.get("app_id")
                    logger.success(f"set app success,appid={self.app_id}")
                else:
                    logger.error(f"set app failed,{response}")
            except asyncio.TimeoutError as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
            except Exception as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
            await asyncio.sleep(1)

    async def start_ping(self, interval=3):
        while True:
            await self.ready.wait()
            request_id: str = self.request_id
            data: dict = {
                "request_id": request_id,
                "event": "ping",
            }
            try:
                await self.send(data)
                await asyncio.wait_for(self.responses[request_id].get(), timeout=3)
            except asyncio.TimeoutError as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
                await self.ws.close(reason="ping超时")  # type: ignore
            await asyncio.sleep(interval)
