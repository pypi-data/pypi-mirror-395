# -*- coding: utf-8 -*-
from collections.abc import Sequence
from typing import Optional, cast

from sanic.exceptions import SanicException
from sanic.log import websockets_logger
from sanic.server.protocols.websocket_protocol import WebSocketProtocol
from sanic.server.websockets.impl import WebsocketImplProtocol
from websockets.extensions.permessage_deflate import ServerPerMessageDeflateFactory
from websockets.protocol import State
from websockets.server import ServerProtocol
from websockets.typing import Subprotocol

# 定义 WebSocket 状态常量
OPEN = State.OPEN
CLOSING = State.CLOSING
CLOSED = State.CLOSED


class CompressedWebSocketProtocol(WebSocketProtocol):
    """
    支持压缩扩展,父类WebSocketProtocol from sanic==25.3.0,
    """

    # 压缩配置 (可根据需求调整)
    # server_max_window_bits: 压缩窗口大小 (9-15)，越大压缩率越高但内存占用越大
    # compress_settings: 设置压缩级别 (0-9)
    WINDOW_BITS = 15
    COMPRESS_LEVEL = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.websocket: Optional[WebsocketImplProtocol] = None

    async def websocket_handshake(
        self, request, subprotocols: Optional[Sequence[str]] = None
    ):
        """
        执行 WebSocket 握手：在发送 HTTP 101 响应给客户端之前，先在服务器端完成 WebSocket 对象的初始化。
        """
        try:
            # 1. 处理子协议 (Subprotocols)
            if subprotocols is not None:
                # 将集合或列表转换为 websockets 库需要的 Subprotocol 列表
                subprotocols = cast(
                    Optional[Sequence[Subprotocol]],
                    list([Subprotocol(subprotocol) for subprotocol in subprotocols]),
                )

            # 2. 配置压缩扩展 (Per-message Deflate)
            extensions = [
                ServerPerMessageDeflateFactory(
                    server_max_window_bits=self.WINDOW_BITS,
                    client_max_window_bits=self.WINDOW_BITS,
                    compress_settings={"level": self.COMPRESS_LEVEL},
                )
            ]

            # 3. 初始化 websockets 库的 ServerProtocol
            ws_proto = ServerProtocol(
                max_size=self.websocket_max_size,
                subprotocols=subprotocols,
                state=OPEN,
                logger=websockets_logger,
                extensions=extensions,
            )

            # 4. 生成握手响应 (Accept)
            ws_request = self.sanic_request_to_ws_request(request)
            resp = ws_proto.accept(ws_request)

        except Exception:
            msg = (
                "Failed to open a WebSocket connection.\n"
                "See server log for more information.\n"
            )
            # 这里使用 websockets_logger 记录具体堆栈
            websockets_logger.error("WebSocket handshake error", exc_info=True)
            raise SanicException(msg, status_code=500)

        # 5. 检查握手结果状态码
        if not (100 <= resp.status_code <= 299):
            # 握手被拒绝 (例如协议不匹配)
            raise SanicException(
                resp.body or "WebSocket handshake rejected", resp.status_code
            )

        # ========================================================
        # 先初始化 Sanic 的 WebSocket 包装器，再发送网络响应
        # ========================================================

        # 6. 初始化 WebSocketImplProtocol
        self.websocket = WebsocketImplProtocol(
            ws_proto,
            ping_interval=self.websocket_ping_interval,
            ping_timeout=self.websocket_ping_timeout,
            close_timeout=self.websocket_timeout,
        )

        # 7. 绑定 Event Loop 并完成连接建立
        # 获取 loop 的方式兼容旧版 Sanic/Asyncio 写法
        loop = getattr(request.transport, "loop", None)

        # connection_made 会将 transport 绑定到 websocket 协议上
        # 此时 self.websocket 已准备好处理 data_received
        await self.websocket.connection_made(self, loop=loop)

        # 8. 设置元数据 (用于日志)
        # 注意：self._http 是 HttpProtocol 的内部引用
        self.websocket_url = self._http.request.url
        self.websocket_peer = f"{id(self):X}"[-5:-1] + "unx"
        if ip := self._http.request.client_ip:
            self.websocket_peer = f"{ip}:{self._http.request.port}"

        self.log_websocket("OPEN")

        # ========================================================
        # 此时发送响应，即使客户端瞬间发来数据，data_received 也能正确路由
        # ========================================================

        # 9. 构造并发送 HTTP 响应
        first_line = (f"HTTP/1.1 {resp.status_code} {resp.reason_phrase}\r\n").encode()

        rbody = bytearray(first_line)

        # 拼接头部
        header_bytes = "".join(
            [f"{k}: {v}\r\n" for k, v in resp.headers.items()]
        ).encode()
        rbody += header_bytes
        rbody += b"\r\n"

        # 拼接 Body (如果有)
        if resp.body:
            rbody += resp.body
            rbody += b"\r\n\r\n"

        # 发送数据到 Socket
        await super(WebSocketProtocol, self).send(rbody)

        return self.websocket

    def data_received(self, data):
        """
        接收数据回调。
        由于 handshake 中提前初始化了 self.websocket，
        这里能准确判断是否应由 WebSocket 协议处理数据。
        """
        if self.websocket is not None:
            self.websocket.data_received(data)
        else:
            # 仍处于 HTTP 阶段或握手尚未开始
            super(WebSocketProtocol, self).data_received(data)
