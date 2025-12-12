# ----------------------------------------------------------------------
# Copyright (c) 2025 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

import json
import logging
import asyncio
import collections

from asyncio import PriorityQueue
from datetime import datetime, timezone, timedelta
from typing import AsyncIterator, Optional, Any, Union, Tuple

from . import protocol, logger
from .constants import MessagePriority
from .model import PhotometerInfo
from .protocol import SerialProtocol, TcpProtocol

# ----------------
# Global variables
# ----------------


class PhotometerReadings:
    def __init__(
        self,
        comm: Union[SerialProtocol, TcpProtocol],
    ):
        self.comm = comm

    def __aiter__(self) -> AsyncIterator[str]:
        """
        Método para inicializar el iterador asíncrono.
        Retorna un AsyncIterator de enteros (puedes cambiar el tipo).
        """
        return aiter(self.comm)

    async def __anext__(self) -> Tuple[datetime, str]:
        """
        Método para obtener el siguiente ítem asincrónico.
        Retorna un entero o lanza StopAsyncIteration para finalizar la iteración.
        """
        return await anext(self.comm)


class Photometer:
    token: int = 0  # To break ties in priority queue

    def __init__(
        self,
        info: PhotometerInfo,
        mqtt_queue: PriorityQueue,
    ):
        self.info = info
        self.period = info.period
        self.log = logging.getLogger(info.name)
        self.log.setLevel(logger.level(info.log_level))
        self.comm = protocol.factory(endpoint=info.endpoint, logger=self.log)
        self.mqtt_queue = mqtt_queue
        self.queue = collections.deque(maxlen=1)  # ring buffer 1 slot long
        self.counter = 0
        self.readings = PhotometerReadings(self.comm)

    async def __aenter__(self) -> "Photometer":
        """
        Context manager that opens/closes the underlying communication interface.
        """
        await self.comm.open()
        return self

    async def __aexit__(
        self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]
    ) -> Optional[bool]:
        """
        Context manager that opens/closes the underlying communication interface.
        """
        if exc_type is not None:
            self.comm.close()
        return False

    async def enqueue(self, priority: MessagePriority, message):
        await self.mqtt_queue.put((priority, Photometer.token, message))
        Photometer.token += 1

    async def register(self) -> None:
        message = self.info.to_dict()
        self.log.info(message)
        await self.enqueue(MessagePriority.MQTT_REGISTER, message)
        self.log.info("Waiting 5 secs. before sending register message again")
        await asyncio.sleep(5)
        await self.enqueue(MessagePriority.MQTT_REGISTER, message)

    async def reader(self) -> None:
        """Photometer reader sub-task"""
        await self.register()
        async with self:  # Open the device
            async for tstamp, message in self.readings:
                if message:
                    try:
                        message = json.loads(message)
                    except json.decoder.JSONDecodeError:
                        pass
                    else:
                        if isinstance(message, dict):
                            tstamp = tstamp + timedelta(seconds=0.5)
                            message["tstamp"] = tstamp.strftime("%Y-%m-%dT%H:%M:%SZ")
                            self.queue.append(message)  # Internal deque

    async def sampler(self) -> None:
        """Photometer sampler sub-task"""
        while True:
            try:
                await asyncio.sleep(self.period)
                if len(self.queue):
                    message = self.queue.pop()
                    message["seq"] = self.counter
                    self.counter += 1
                    self.log.info(message)
                    await self.enqueue(MessagePriority.MQTT_READINGS, message)
                else:
                    self.log.warn("missing data. Check %s connection", self.comm.__class__.__name__)
            except Exception as e:
                self.log.exception(e)
                break


async def reader(photometer: Photometer) -> None:
    """Photometer master task"""
    async with asyncio.TaskGroup() as tg:
        tg.create_task(photometer.reader())
        tg.create_task(photometer.sampler())
