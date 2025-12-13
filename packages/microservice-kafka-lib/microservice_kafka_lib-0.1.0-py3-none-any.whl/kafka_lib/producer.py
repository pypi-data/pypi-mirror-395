import asyncio
import json
import logging
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self, bootstrap_servers: str, loop, reconnect_interval: float = 3.0):
        self._bootstrap_servers = bootstrap_servers
        self._loop = loop
        self._producer: AIOKafkaProducer | None = None
        self._reconnect_interval = reconnect_interval

    async def start(self) -> None:
        if self._producer is not None:
            return

        while True:
            producer = AIOKafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                loop=self._loop,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            try:
                await producer.start()
                self._producer = producer
                logger.info("KafkaProducer connected to %s", self._bootstrap_servers)
                break
            except KafkaConnectionError as e:
                logger.warning(
                    "KafkaProducer: Kafka not ready (%s). Retry in %.1f sec",
                    e,
                    self._reconnect_interval,
                )
                await asyncio.sleep(self._reconnect_interval)

    async def stop(self) -> None:
        if self._producer is not None:
            await self._producer.stop()
            logger.info("KafkaProducer stopped")
            self._producer = None

    async def send(self, topic: str, value: dict, key: str | None = None) -> None:
        if self._producer is None:
            raise RuntimeError("Producer is not started")
        key_bytes = key.encode("utf-8") if key is not None else None
        await self._producer.send_and_wait(topic, value=value, key=key_bytes)
        logger.info("Sent message to topic %s: %s", topic, value)
