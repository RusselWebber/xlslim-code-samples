# Creates test data for use in kafka_double_consumer.py and kafka_consumer.xlsx
# A running Kafka broker can be setup simply using Docker, the Confluent platform includes a nice management console, see:
# https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html
# The aiokafka package can be installed using pip, see https://github.com/aio-libs/aiokafka
import pickle
import asyncio
from aiokafka import AIOKafkaProducer


async def send():
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092", value_serializer=lambda m: pickle.dumps(m),
    )
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce messages
        for i in range(1_000_000):
            await producer.send("doubles", float(i))
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(send())
