import asyncio
import json
import logging
from collections.abc import Awaitable, Callable

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

logger = logging.getLogger(__name__)

MessageHandler = Callable[[dict], Awaitable[None]]


class KafkaConsumer:
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        loop,
        handler: MessageHandler,
        reconnect_interval: float = 3.0,
    ):
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._group_id = group_id
        self._loop = loop
        self._handler = handler
        self._reconnect_interval = reconnect_interval

        self._consumer: AIOKafkaConsumer | None = None
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        if self._consumer is not None:
            return

        while True:
            consumer = AIOKafkaConsumer(
                self._topic,
                loop=self._loop,
                bootstrap_servers=self._bootstrap_servers,
                group_id=self._group_id,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                enable_auto_commit=True,
            )
            try:
                await consumer.start()
                self._consumer = consumer
                logger.info(
                    "KafkaConsumer connected (topic=%s, group_id=%s)",
                    self._topic,
                    self._group_id,
                )
                self._task = self._loop.create_task(self._consume_loop())
                break
            except KafkaConnectionError as e:
                logger.warning(
                    "KafkaConsumer: Kafka not ready (%s). Retry in %.1f sec",
                    e,
                    self._reconnect_interval,
                )
                await asyncio.sleep(self._reconnect_interval)

    async def _consume_loop(self) -> None:
        assert self._consumer is not None
        try:
            async for msg in self._consumer:
                logger.info("Received message from %s: %s", msg.topic, msg.value)
                try:
                    await self._handler(msg.value)
                except Exception:
                    logger.exception("Error in handler")
        except asyncio.CancelledError:
            logger.info("KafkaConsumer consume loop cancelled")
        finally:
            logger.info("KafkaConsumer consume loop finished")

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

        if self._consumer is not None:
            await self._consumer.stop()
            logger.info("KafkaConsumer stopped")
            self._consumer = None
