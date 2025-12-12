import asyncio
from logging import Logger
from datetime import datetime, timezone
from typing import Union, Tuple

import serial_asyncio


class StreamProtocol(asyncio.Protocol):
    def __init__(
        self,
        logger: Logger,
        loop: asyncio.AbstractEventLoop | None,
        encoding: str,
        newline: bytes,
    ):
        self.encoding = encoding
        self.newline = newline
        self._buffer = bytearray()
        self.loop = loop or asyncio.get_event_loop()
        self.log = logger
        # Futures for external awaiters
        self.on_data_received: asyncio.Future | None = None
        self.on_conn_lost: asyncio.Future = self.loop.create_future()
        # Internal state
        self.transport: asyncio.Transport | None = None

    # ----------------------
    # The iterator interface
    # ----------------------

    def __aiter__(self) -> "StreamProtocol":
        # The iterator is its own async iterator.
        return self

    async def __anext__(self) -> Tuple[datetime, str]:
        if self.on_data_received is not None and not self.on_data_received.done():
            self.on_data_received.cancel()
        self.on_data_received = self.loop.create_future()
        return await self.on_data_received

    # --------------------
    # Very generic methods
    # --------------------

    def close(self) -> None:
        self.transport.close()

    # ---------------------------------------
    # The asyncio Protocol callback interface
    # ---------------------------------------

    def connection_made(self, transport: asyncio.Transport) -> None:
        self.transport = transport

    def connection_lost(self, exc: Exception | None) -> None:
        if not self.on_conn_lost.cancelled() and not self.on_conn_lost.done():
            self.on_conn_lost.set_result(True)

        if (
            self.on_data_received is not None
            and not self.on_data_received.done()
            and not self.on_data_received.cancelled()
        ):
            self.on_data_received.set_exception(
                ConnectionError("Connection lost before incoming message was complete")
            )
        self.transport.close()

    def data_received(self, data: bytes) -> None:
        # Accumulate incoming bytes
        self._buffer.extend(data)
        # Process all complete lines currently in buffer
        while True:
            idx = self._buffer.find(self.newline)
            if idx == -1:
                break  # no full line yet
            now = datetime.now(timezone.utc)
            # Extract one line including newline
            line = self._buffer[: idx + len(self.newline)]
            del self._buffer[: idx + len(self.newline)]  # delete extracted line from buffer
            message = line.decode(self.encoding, errors="replace")
            if (
                self.on_data_received is not None
                and not self.on_data_received.cancelled()
                and not self.on_data_received.done()
            ):
                self.log.debug(message)
                self.on_data_received.set_result((now, message))
                # Only fulfill one waiter; caller can call next_message() again.
                break


class SerialProtocol(StreamProtocol):
    def __init__(
        self,
        logger: Logger,
        port: str,
        baudrate: int,
        loop: asyncio.AbstractEventLoop | None = None,
        encoding: str = "utf-8",
        newline: bytes = b"\r\n",
    ):
        super().__init__(logger, loop, encoding, newline)
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.log.info("Using %s", self.__class__.__name__)

    async def open(self) -> None:
        self.log.info("Opening Serial connection to %s @ %s", self.port, self.baudrate)
        transport, self.protocol = await serial_asyncio.create_serial_connection(
            self.loop, lambda: self, self.port, baudrate=self.baudrate
        )

    # ---------------------------------------
    # The asyncio Protocol callback interface
    # ---------------------------------------

    def connection_made(self, transport: asyncio.Transport) -> None:
        self.log.info("Serial connection to %s @ %s open", self.port, self.baudrate)
        super().connection_made(transport)

    def connection_lost(self, exc: Exception | None):
        self.log.warn("Lost serial connection to %s @ %s", self.port, self.baudrate)
        super().connection_lost(exc)


class TcpProtocol(StreamProtocol):
    def __init__(
        self,
        logger: Logger,
        host: str,
        port: int,
        loop: asyncio.AbstractEventLoop | None = None,
        encoding: str = "utf-8",
        newline: bytes = b"\r\n",
    ) -> None:
        super().__init__(logger, loop, encoding, newline)

        self.host = host
        self.port = port
        self.log.info("Using %s", self.__class__.__name__)

    async def open(self) -> None:
        self.log.info("Opening TCP connection to (%s, %s)", self.host, self.port)
        transport, self.protocol = await self.loop.create_connection(
            lambda: self, self.host, self.port
        )

    # ---------------------------------------
    # The asyncio Protocol callback interface
    # ---------------------------------------

    def connection_made(self, transport: asyncio.Transport) -> None:
        self.log.info("TCP connection to (%s, %s) open", self.host, self.port)
        super().connection_made(transport)

    def connection_lost(self, exc: Exception | None):
        self.log.warn("Lost TCP connection to (%s, %s)", self.host, self.port)
        super().connection_lost(exc)


class UdpProtocol(asyncio.DatagramProtocol):
    def __init__(
        self,
        logger: Logger,
        local_host: str = "0.0.0.0",
        local_port: int = 2255,
        loop: asyncio.AbstractEventLoop | None = None,
        encoding: str = "utf-8",
        newline: bytes = b"\r\n",
    ):
        self.loop = loop or asyncio.get_event_loop()
        self.log = logger
        self.encoding = encoding
        self.newline = newline
        self.local_host = local_host
        self.local_port = local_port
        # Futures for external awaiters
        self.on_data_received: asyncio.Future | None = None
        self.on_conn_lost: asyncio.Future = self.loop.create_future()
        self.log.info("Using %s", self.__class__.__name__)

    async def open(self) -> None:
        self.log.info("Opening UDP endpoint on (%s, %s)", self.local_host, self.local_port)
        transport, self.protocol = await self.loop.create_datagram_endpoint(
            lambda: self, local_addr=(self.local_host, self.local_port)
        )

    def close(self) -> None:
        self.transport.close()

    # ---------------------------------------
    # The asyncio Protocol callback interface
    # ---------------------------------------

    def connection_made(self, transport: asyncio.Transport) -> None:
        self.log.info("UDP socket listening to (%s, %s)", self.local_host, self.local_port)
        self.transport = transport

    def connection_lost(self, exc: Exception | None) -> None:
        self.log.warn("Closed UDP endpoint on (%s, %s)", self.local_host, self.local_port)
        if not self.on_conn_lost.cancelled() and not self.on_conn_lost.done():
            self.on_conn_lost.set_result(True)
        if (
            self.on_data_received is not None
            and not self.on_data_received.done()
            and not self.on_data_received.cancelled()
        ):
            self.on_data_received.set_exception(
                ConnectionError("socket closed before incoming message was complete")
            )
        self.transport.close()

    def datagram_received(self, payload: bytes, addr: str):
        now = datetime.now(timezone.utc)
        message = payload.decode(self.encoding, errors="replace")
        if (
            self.on_data_received is not None
            and not self.on_data_received.cancelled()
            and not self.on_data_received.done()
        ):
            self.log.debug(message)
            self.on_data_received.set_result((now, message))

    # ----------------------
    # The iterator interface
    # ----------------------

    def __aiter__(self) -> "UdpProtocol":
        # The iterator is its own async iterator.
        return self

    async def __anext__(self) -> Tuple[datetime, str]:
        if self.on_data_received is not None and not self.on_data_received.done():
            self.on_data_received.cancel()
        self.on_data_received = self.loop.create_future()
        return await self.on_data_received


def chop(endpoint: str, sep=":"):
    """Chop a list of strings, separated by sep and
    strips individual string items from leading and trailing blanks"""
    chopped = tuple(elem.strip() for elem in endpoint.split(sep))
    if len(chopped) == 1 and chopped[0] == "":
        chopped = tuple()
    return chopped


def factory(endpoint: str, logger: Logger) -> Union[TcpProtocol, SerialProtocol]:
    proto, A, B = chop(endpoint)
    if proto == "serial":
        comm = SerialProtocol(logger=logger, port=A, baudrate=B)
    elif proto == "tcp":
        comm = TcpProtocol(logger=logger, host=A, port=B)
    elif proto == "udp":
        comm = UdpProtocol(logger=logger, local_host=A, local_port=B)
    else:
        raise NotImplementedError(f"Unsupported protocol: {proto}")
    return comm
