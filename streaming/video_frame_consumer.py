import asyncio
import logging
import numpy as np
from io import BytesIO
from contextlib import closing
from aiokafka import AIOKafkaConsumer

LOG = logging.getLogger(__name__)


async def kafka_topic_subscription(topic: str, server: str, fps: str) -> np.ndarray:
    """Subscribe to data from a Kafka topic"""
    consumer = AIOKafkaConsumer(
        topic, bootstrap_servers=server, auto_offset_reset="earliest"
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            # Convert from bytes to array
            with closing(BytesIO(msg.value)) as np_bytes:
                yield np.load(np_bytes, allow_pickle=False)
                # Get the message rate to approximately match the desired frames per second
                await asyncio.sleep(1.0 / float(fps))
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


async def main():
    async for data in kafka_topic_subscription("video", "localhost:9092", 30):
        print(data)


if __name__ == "__main__":
    asyncio.run(main())
