# Shows how a subscription to a Kafka topic can be setup
# A running Kafka broker can be setup simply using Docker, the Confluent platform includes a nice management console, see:
# https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html
# The aiokafka package can be installed using pip, see https://github.com/aio-libs/aiokafka
import asyncio
import pickle
import datetime
import time
from aiokafka import AIOKafkaConsumer


async def kafka_topic_subscription(topic: str, server: str, start: float) -> float:
    """Subscribe to data from a Kafka topic.
    
    The start argument is not required and is only here to enable some performance testing.
    """
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=server,
        # Using pickle for this demo, more realistic options would be JSON, MessagePack, etc
        value_deserializer=lambda m: pickle.loads(m),
        # For this demo we always replay all messages
        auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            yield msg.value
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


##
## The rest is all testing and profiling code, only kafka_topic_subscription is needed to subscribe to data
##


class MessageCounter:
    """A little message counter utility class"""

    def __init__(self):
        self.count = 0


def create_message_counter(start: datetime.datetime) -> MessageCounter:
    """Creates a MessageCounter. start is used to sync the timing."""
    return MessageCounter()


def count_message(mc: MessageCounter, d: float) -> int:
    """Add one to the MessageCounter. Is updated every time a new double is received."""
    mc.count += 1
    return mc.count


def messages_per_second_processed(
    num_messages: float, start: datetime.datetime
) -> float:
    """Calculates the message processing rate."""
    return num_messages / (datetime.datetime.now() - start).total_seconds()


def current_time() -> datetime.datetime:
    """A non-volatile way to get the current time and trigger the subscription to start."""
    return datetime.datetime.now()


async def main():
    start = time.perf_counter()
    mc = MessageCounter()
    async for _ in kafka_topic_subscription("doubles", "localhost:9092", start):
        mc.count += 1
        if mc.count >= 1_000_000:
            break
    end = time.perf_counter()
    print(mc.count / (end - start))


if __name__ == "__main__":
    asyncio.run(main())
