# -*- coding: utf-8 -*-
import asyncio
import json
import ssl
from typing import Any, Callable

import certifi
import websockets
import websockets.client
from loguru import logger


async def on_xt_connect_callback(connected: bool):
    logger.warning(f"on_xt_connect_callback connected={connected}")


async def on_xt_event_callback(payload: dict):
    event: str = payload.get("t") or ""
    body: dict = payload.get("b", {})
    match event:
        case "on_multi_login":
            pass
        case "push_connection_id":
            pass
        case "push_account_status":
            pass
        case "push_account_changed":
            pass
        case "push_position_changed":
            pass
        case "push_position_stat_changed":
            pass
        case "push_order_changed":
            pass
        case "push_deal_changed":
            pass


class XtTradeClient:
    def __init__(
        self,
        uri: str,
        xt_users_token: str,
        connect_callback: Callable = on_xt_connect_callback,
        event_callback: Callable = on_xt_event_callback,
    ):
        assert uri and isinstance(uri, str), f"uri={uri}"
        self.uri: str = uri
        assert xt_users_token and isinstance(xt_users_token, str), (
            "xt_users_token必须为非空字符串"
        )
        self.xt_users_token: str = xt_users_token
        self.connect_callback: Callable = connect_callback
        self.event_callback: Callable = event_callback
        self.ws: websockets.client.WebSocketClientProtocol | None = None
        self.ready: asyncio.Event = asyncio.Event()
        self.conn_id_received: asyncio.Event = asyncio.Event()
        self.logined: asyncio.Event = asyncio.Event()
        self.conn_id: str = ""
        self.req_id: int = 0
        self.account_keys: set[str] = set()
        self.responses: dict[int, asyncio.Queue] = {}
        self.connect_task: asyncio.Task = asyncio.create_task(self.connect_ws())

    @property
    def request_id(self) -> int:
        self.req_id += 1
        return self.req_id

    @property
    def xt_account_keys(self) -> list:
        return list(self.account_keys)

    async def connect_ws(self):
        while not self.ready.is_set():
            recv_task: asyncio.Task | None = None
            ping_task: asyncio.Task | None = None
            try:
                logger.warning("connecting to TradeServer...")
                sc = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                sc.check_hostname = False
                sc.verify_mode = ssl.CERT_NONE
                sc.load_verify_locations(certifi.where())
                self.ws = await websockets.connect(
                    uri=self.uri,
                    max_size=2**32 - 1,
                    max_queue=2**8,
                    write_limit=2**32 - 1,
                    ssl=sc if self.uri.startswith("wss") else None,
                )
                logger.success("connected to TradeServer!")
                self.ready.set()
                await self.connect_callback(connected=True)
                recv_task = asyncio.create_task(self.exec_recv())
                # login
                await self.conn_id_received.wait()
                error, response = await self.multi_login(
                    xt_users_token=self.xt_users_token
                )
                assert not error, f"login fail! error={error}"
                logger.success(f"login success! response={response}")
                self.logined.set()
                ping_task = asyncio.create_task(self.start_ping())
                await recv_task
            except Exception as e:
                logger.exception(f"[{e.__class__.__name__}]{e}")
            finally:
                logger.warning("TradeServer disconnected")
                # close ws
                if self.ws:
                    await self.ws.close()
                    self.ws = None
                self.responses.clear()
                # cancel tasks
                if recv_task:
                    recv_task.cancel()
                if ping_task:
                    ping_task.cancel()
                self.ready.clear()
                self.conn_id_received.clear()
                self.logined.clear()
                await self.connect_callback(connected=False)
                await asyncio.sleep(3)
        # cancel connect task
        self.connect_task.cancel()

    async def exec_recv(self):
        while True:
            payload: dict | None = await self.recv()
            if not payload:
                continue
            event: str = payload.get("t", "")
            body: dict = payload.get("b", {})
            if event == "push_connection_id":
                self.conn_id: str = body.get("connection_id", "")
                self.req_id = 0
                self.conn_id_received.set()
            elif event == "push_account_status":
                account_key: str = body.get("account_key", "")
                assert account_key, f"account_key={account_key}"
                self.account_keys.add(account_key)
            response_id: str | None = payload.get("i", None)
            if response_id:
                await self.responses[response_id].put(payload)
            await self.event_callback(payload)

    async def wait_response(
        self, request_id: int, timeout: int = 20
    ) -> tuple[str, Any]:
        error: str = ""
        data: Any | None = None
        try:
            rj: dict = await asyncio.wait_for(
                self.responses[request_id].get(), timeout=timeout
            )
            body: dict = rj.get("b")  # type: ignore
            assert body, f"body={body}"
            if body.get("code") != 0:
                error = body.get("msg")
            data = body.get("data")
        except Exception as e:
            logger.error(e)
            error = e.__class__.__name__
        return error, data

    async def send(self, data: dict):
        try:
            if self.ws:
                message: str = json.dumps(data, ensure_ascii=False)
                request_id: int = data["i"]
                assert request_id and request_id not in self.responses
                logger.info(f" send {message}")
                await self.ws.send(message)
                self.responses[request_id] = asyncio.Queue()
        except Exception as e:
            logger.exception(f"[{e.__class__.__name__}]{e}")
            if self.ws:
                await self.ws.close()
                self.ws = None

    async def recv(self) -> dict | None:
        if self.ws:
            payload: str = await self.ws.recv()  # type: ignore
            try:
                if payload:
                    logger.info(f"recv={payload[:200]}")
                    _json = json.loads(payload)
                    return _json
            except Exception as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
        return None

    async def multi_login(self, xt_users_token: str):
        await self.ready.wait()
        request_id: int = self.request_id
        data: dict = {"i": request_id, "t": "multi_login", "b": xt_users_token}
        await self.send(data=data)
        error, response = await self.wait_response(request_id)
        return error, response

    async def start_ping(self, interval=10) -> None:
        while True:
            await self.ready.wait()
            request_id: int = self.request_id
            data: dict = {
                "i": request_id,
                "t": "ping",
            }
            try:
                await self.send(data=data)
            except Exception as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
                await asyncio.sleep(1)
                continue
            try:
                await asyncio.wait_for(
                    self.responses[request_id].get(), timeout=interval
                )
            except asyncio.TimeoutError as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
                if self.ws:
                    await self.ws.close()
                continue
            await asyncio.sleep(interval)

    async def query_accounts(self):
        request_id: int = self.request_id
        data: dict = {"i": request_id, "t": "query_accounts"}
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def query_balances(self, info: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "query_balances",
            "b": info,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def query_positions(self, info: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "query_positions",
            "b": info,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def query_position_statics(self, info: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "query_position_statics",
            "b": info,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def query_init_position_statics(self, info: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "query_init_position_statics",
            "b": info,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def query_history_position_statics(self, info: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "query_history_position_statics",
            "b": info,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def query_orders(self, info: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "query_orders",
            "b": info,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def query_deals(self, info: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "query_deals",
            "b": info,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def query_commands(self, info: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "query_commands",
            "b": info,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def make_order(self, order: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "make_order",
            "b": order,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def make_order_by_market(self, order: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "make_order_by_market",
            "b": order,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def cancel_order(self, order: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "cancel_order",
            "b": order,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def cancel_command(self, command: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "cancel_command",
            "b": command,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def vwap_buy(self, account: str, seconds: int, symbols: list[dict]):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "vwap_buy",
            "b": {"account": account, "seconds": seconds, "symbols": symbols},
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def vwap_sell(self, account: str, seconds: int, symbols: list[dict]):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "vwap_sell",
            "b": {"account": account, "seconds": seconds, "symbols": symbols},
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def market_sell(self, account: str, symbols: list[dict]):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "market_sell",
            "b": {"account": account, "symbols": symbols},
        }
        await self.send(data=data)
        return await self.wait_response(request_id)

    async def subscribe_quote(self, info: dict):
        request_id: int = self.request_id
        data: dict = {
            "i": request_id,
            "t": "subscribe_quote",
            "b": info,
        }
        await self.send(data=data)
        return await self.wait_response(request_id)
