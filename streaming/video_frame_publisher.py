import cv2
import asyncio
import logging
import numpy as np
from io import BytesIO
from contextlib import closing
from aiokafka import AIOKafkaProducer

LOG = logging.getLogger(__name__)

Video_FILE = r"C:\Users\russe\Downloads\Y2Mate.is - Best of Charlie Chaplin silent comedy-KHUMoKnlxUc-480p-1658397579222.mp4"


def get_gray_frames(filename):
    video = cv2.VideoCapture(filename)
    while video.isOpened():
        rete, frame = video.read()
        if rete:
            # Resize
            # (col, rows)
            resized_frame = cv2.resize(frame, (250, 250), interpolation=cv2.INTER_AREA)
            # Convert to gray
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_RGB2GRAY)
            # Trim black space on left and right
            trimmed_frame = gray_frame[..., 30:220]
            # Set the data type to double
            trimmed_frame = trimmed_frame.astype(np.double)
            yield trimmed_frame
        else:
            break
    video.release()


async def send():
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        for f in get_gray_frames(Video_FILE):
            # Convert from array to bytes
            with closing(BytesIO()) as np_bytes:
                np.save(np_bytes, f, allow_pickle=False)
                await producer.send("video", np_bytes.getvalue())
    except:
        LOG.error("Failed to send", exc_info=True)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(send())
