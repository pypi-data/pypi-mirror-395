import asyncio
import inspect
import time
import traceback
from typing import Any, Callable, Literal, Tuple

import orjson
import websockets
from loguru import logger


class XComBase:
    def __init__(self, tag: str = "", verbose: bool = True, debug: bool = False):
        self._tag = tag
        self._verbose = verbose
        self._debug = debug

    @property
    def _identifier(self) -> str:
        return self.__class__.__name__ + (f"-{self._tag}" if self._tag else "")


class XComSvr(XComBase):
    """Interprocess Communication by Websocket - Server"""

    def __init__(
        self,
        msg_callbacks: dict[str, Callable],
        unix_sock: str | None = None,
        host: str | None = None,
        port: int | None = None,
        keep_alive: bool = True,
        restart_policy: Literal["always", "never"] = "always",
        tag: str = "",
        verbose: bool = True,
        debug: bool = False,
    ):
        """_summary_

        Args:
            msg_callbacks (dict[str, Callable]): {req_type: async callback)
            unix_sock (str | None, optional): _description_. Defaults to None.
            host (str | None, optional): _description_. Defaults to None.
            port (str | None, optional): _description_. Defaults to None.
            keep_alive (bool, optional): Keep connection alive (for keep alive client) or close connection (for transient client). Defaults to True.
            restart_policy (Literal[&quot;always&quot;, &quot;never&quot;], optional): _description_. Defaults to "always".
            debug (bool, optional): _description_. Defaults to False.
        """
        super().__init__(tag, verbose, debug)
        self._use_unix_sock: bool
        self._unix_sock: str | None
        self._host: str | None
        self._port: int | None

        # sanity check
        assert (unix_sock is not None) ^ ((host is not None) & (port is not None))
        if unix_sock:
            self._use_unix_sock = True
            self._unix_sock = unix_sock
            self._host = None
            self._port = None
        else:
            self._use_unix_sock = False
            self._unix_sock = None
            self._host = host
            self._port = port

        self._keep_alive = keep_alive
        assert restart_policy in ["always", "never"]
        self._restart_policy: str = restart_policy

        self._callbacks: dict[str, Callable] = dict()
        for req_type, callback in msg_callbacks.items():
            self.register_msg_callback(req_type, callback)

    def register_msg_callback(self, req_type: str, callback: Callable):
        if callback is None or not inspect.iscoroutinefunction(callback):
            raise TypeError(f"msg_callback for req_type={req_type} must be a coroutine function")
        else:
            self._callbacks[req_type] = callback

    async def _req_handler(self, ws: websockets.ServerConnection):
        while True:
            try:
                raw_req_d = orjson.loads(await ws.recv())
            except websockets.exceptions.ConnectionClosedError as e:
                logger.debug("Connection closed with code {} and reason {}".format(e.code, e.reason))
                break
            except websockets.exceptions.ConnectionClosedOK as e:
                break

            logger.debug("Receive raw request {}".format(raw_req_d))

            if raw_req_d["req_type"] not in self._callbacks:
                raw_rsp_d = {
                    "ts": int(time.time() * 1000000),
                    "err_msg": "Callback for req_type={} not found.".format(raw_req_d["req_type"]),
                }
            else:
                try:
                    rsp_d = await self._callbacks[raw_req_d["req_type"]](raw_req_d["data"])
                except Exception as e:
                    raw_rsp_d = {
                        "ts": int(time.time() * 1000000),
                        "err_msg": "Callback failed with exception={}. reason={}. raw_req={}.".format(
                            e.__class__.__name__,
                            str(e),
                            str(raw_req_d),
                        ),
                    }
                else:
                    raw_rsp_d = {
                        "ts": int(time.time() * 1000000),
                        "data": rsp_d,
                    }

            logger.debug("Send raw rsponse {}".format(raw_rsp_d))
            await ws.send(orjson.dumps(raw_rsp_d))

            if not self._keep_alive:
                break

    async def run(self):
        while True:
            try:
                if self._use_unix_sock:
                    logger.debug("Listen to {}".format(self._unix_sock))
                    server = await websockets.unix_serve(self._req_handler, self._unix_sock)
                    async with server:
                        await asyncio.Future()
                else:
                    logger.debug("Listen to {}:{}".format(self._host, self._port))
                    async with websockets.serve(self._req_handler, self._host, self._port):
                        await asyncio.Future()
            except (KeyboardInterrupt, asyncio.CancelledError):
                logger.info("Stop gracefully.")
                break
            except Exception as e:
                logger.error("Failed with {}. error={}".format(e.__class__.__name__, str(e)))
                logger.debug(traceback.format_exc())
                if self._restart_policy == "always":
                    logger.info(f"Restart server.")
                    await asyncio.sleep(0.5)
                else:
                    break


class XComTCli(XComBase):
    """Interprocess Communication by Websocket - Tansient Client

    Mode: one request, one response, e.g., REQ->RSP->REQ->RSP
    """

    def __init__(
        self,
        unix_sock: str | None = None,
        host: str | None = None,
        port: int | None = None,
        req_type: str | None = None,
        tag: str = "",
        verbose: bool = True,
        debug: bool = False,
    ) -> None:
        super().__init__(tag, verbose, debug)
        self._use_unix_sock: bool
        self._unix_sock: str | None
        self._host: str | None
        self._port: int | None

        # sanity check
        assert (unix_sock is not None) ^ ((host is not None) & (port is not None))
        if unix_sock:
            self._use_unix_sock = True
            self._unix_sock = unix_sock
            self._host = None
            self._port = None
        else:
            self._use_unix_sock = False
            self._unix_sock = None
            self._host = host
            self._port = port
        self._req_type: str | None = req_type

    async def _raw_req(self, raw_req_b: bytes, timeout: float) -> Tuple[bytes | None, str | None]:
        """
        Args:
            raw_req_b (bytes): _description_
            timeout (float): in seconds

        Returns:
            Tuple[bytes, str]:
                if all success, return received bytes, None
                otherwise, return None, error reason str
        """
        try:
            async with asyncio.timeout(timeout):
                if self._use_unix_sock:
                    async with websockets.unix_connect(self._unix_sock) as ws:
                        await ws.send(raw_req_b)
                        raw_rsp_b = await ws.recv(decode=False)
                        return raw_rsp_b, None
                else:
                    async with websockets.connect("ws://{}:{}".format(self._host, self._port)) as ws:
                        await ws.send(raw_req_b)
                        raw_rsp_b = await ws.recv(decode=False)
                        return raw_rsp_b, None
        except (ConnectionRefusedError, FileNotFoundError) as e:
            return None, f"Connection failed with {str(e)}."
        except TimeoutError:
            return None, f"Request timeout."
        except Exception as e:
            return None, "Connection error. Error type: {}. Error msg: {}..".format(e.__class__.__name__, str(e))

    async def req(
        self,
        req_d: dict[str, Any],
        req_type: str | None = None,
        timeout: float = 0.5,
    ) -> Tuple[dict[str, Any], None, float] | Tuple[None, str, float] | Tuple[None, str | None, None]:
        """_summary_

        Args:
            req_d (dict[str, Any]): _description_

        Returns:
            Tuple[dict[str, Any] | None, str | None]: rsp_data, error message, latancy_ms
        """
        if req_type:
            final_req_type = req_type
        elif self._req_type:
            final_req_type = self._req_type
        else:
            raise ValueError("Must specify req_type!")
        raw_req_d = {
            "req_type": final_req_type,
            "ts": int(time.time() * 1000000),
            "data": req_d,
        }
        raw_rsp_b, err_msg = await self._raw_req(orjson.dumps(raw_req_d), timeout=timeout)
        if raw_rsp_b is None:
            return None, err_msg, None
        else:
            raw_rsp_d = orjson.loads(raw_rsp_b)
            if "data" in raw_rsp_d:
                return raw_rsp_d["data"], None, raw_rsp_d["ts"]
            else:
                return None, raw_rsp_d["err_msg"], raw_rsp_d["ts"]


class XComKACli(XComBase):
    """保持连接的ws client, 发请求和收回复是异步的。
    主要用在请求后需要NO BLOCK等待回复或者不需要等待回复的场景。
    """

    def __init__(
        self,
        req_type: str,
        unix_sock: str | None = None,
        host: str | None = None,
        port: int | None = None,
        reconnect_wait: float = 0.5,
        tag: str = "",
        verbose: bool = True,
        debug: bool = False,
    ):
        """_summary_

        Args:
            uri (str): _description_
            req_type (str): request type str
            reconnect_wait (float, optional): wait seconds before reconnect. Defaults to 0.5.
            debug (bool, optional): _description_. Defaults to False.
        """
        super().__init__(tag, verbose, debug)
        self._use_unix_sock: bool
        self._unix_sock: str | None
        self._host: str | None
        self._port: int | None

        # sanity check
        assert (unix_sock is not None) ^ ((host is not None) & (port is not None))
        if unix_sock:
            self._use_unix_sock = True
            self._unix_sock = unix_sock
            self._host = None
            self._port = None
        else:
            self._use_unix_sock = False
            self._unix_sock = None
            self._host = host
            self._port = port
        assert req_type, "req_type must not be none!"
        self._req_type: str = req_type
        self._reconnect_wait: float = reconnect_wait
        self._debug: bool = debug
        self._ws: websockets.ClientConnection | None = None
        self._msg_callback: Callable | None = None
        self._tag: str = tag
        self._closing_flag: bool = False

    def register_msg_callback(self, msg_callback: Callable):
        if inspect.iscoroutinefunction(msg_callback):
            self._msg_callback = msg_callback
        else:
            raise TypeError("msg_callback must be a coroutine function")

    async def send(
        self,
        req_d: dict[str, Any],
        timeout: int = 1,
    ) -> str | None:
        """_summary_

        Args:
            req_d (dict[str, Any]): _description_
            req_type (str | None, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_

        Returns:
            str | None: if error, return err msg, else return None
        """
        raw_req_d = {
            "req_type": self._req_type,
            "ts": int(time.time() * 1000000),
            "data": req_d,
        }
        if self._ws is not None:
            try:
                async with asyncio.timeout(timeout):
                    await self._ws.send(orjson.dumps(raw_req_d))
                return None
            except TimeoutError:
                return f"Send timeout."
            except Exception as e:
                return "Send failed. Error type {}. Error msg {}.".format(e.__class__.__name__, str(e))
        else:
            return f"Connection is not ready for sending."

    async def _listen(self):
        if self._ws is None:
            return
        while True:
            try:
                raw_rsp_b = await self._ws.recv()
            except Exception as e:
                logger.error(
                    "recv() error. Error type {}. Error msg {}.".format(
                        e.__class__.__name__,
                        str(e),
                    )
                )
                break
            else:
                raw_rsp_d = orjson.loads(raw_rsp_b)
                if "err_msg" in raw_rsp_d:
                    logger.error("Recv error msg {}".format(raw_rsp_d["err_msg"]))
                elif self._msg_callback is not None:
                    try:
                        await self._msg_callback(raw_rsp_d["data"])
                    except Exception as e:
                        logger.error(
                            "Error during msg callback. Error type {}. Error msg {}.".format(
                                e.__class__.__name__,
                                str(e),
                            )
                        )
                        logger.debug(traceback.format_exc())
                else:
                    logger.warning(f"Discard response {raw_rsp_d} as no callback registered!")

    async def run(self):
        while True:
            if self._ws is not None:
                try:
                    await self._ws.close()
                except Exception as e:
                    logger.error(
                        "Meet {} during closing ws client. Force clearing previous connection now. Error msg {}".format(
                            e.__class__.__name__,
                            str(e),
                        )
                    )
                    self._ws = None
                else:
                    self._ws = None
            try:
                if self._use_unix_sock:
                    async with websockets.unix_connect(self._unix_sock) as self._ws:
                        if self._debug:
                            logger.info(f"Connected to {self._unix_sock}")
                        await self._listen()
                else:
                    async with websockets.connect("ws://{}:{}".format(self._host, self._port)) as self._ws:
                        if self._debug:
                            logger.info(f"Connected to {self._host}:{self._port}")
                        await self._listen()
            except (ConnectionRefusedError, FileNotFoundError) as e:
                logger.error(f"Connection failed with {str(e)}.")
            except (asyncio.CancelledError, KeyboardInterrupt) as e:
                logger.info(f"Close gracefully.")
                self._closing_flag = True
                if self._ws is not None:
                    await self._ws.close()
                break
            except Exception as e:
                logger.error(
                    "Connection failed. Error type {}. Error msg {}".format(
                        e.__class__.__name__,
                        str(e),
                    )
                )
                if self._debug:
                    logger.debug(traceback.format_exc())
            finally:
                if not self._closing_flag:
                    logger.info(f"Reconnect after {self._reconnect_wait} second(s)")
                    await asyncio.sleep(self._reconnect_wait)
