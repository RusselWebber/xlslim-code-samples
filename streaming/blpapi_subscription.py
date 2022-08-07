# The blpapi package is installable using pip, see https://www.bloomberg.com/professional/support/api-library/
# The Bloomberg samples are downloadable from https://www.bloomberg.com/professional/support/api-library/
# This code is based on the Blooomberg example SubscriptionExample.py in examples\demoapps in the downloaded Bloomberg samples

import time
import logging
import datetime

from argparse import ArgumentParser, RawTextHelpFormatter
from collections import defaultdict
from threading import Event
from typing import List, Dict, Any, Optional

from blpapi_import_helper import blpapi

from util.SubscriptionOptions import (
    addSubscriptionOptions,
    setSubscriptionSessionOptions,
    createSubscriptionList,
)
from util.ConnectionAndAuthOptions import (
    addConnectionAndAuthOptions,
    createSessionOptions,
)

DEFAULT_QUEUE_SIZE = 10000
LOG = logging.getLogger(__name__)


class SubscriptionEventHandler(object):
    def __init__(self, topics, fields):
        self._data_event = Event()
        self._data_dict = defaultdict(dict)
        self._topics = topics
        self._fields = fields

    def get_data_dict(self):
        return self._data_dict

    def wait_for_data_event(self):
        self._data_event.wait()

    def clear_data_event(self):
        self._data_event.clear()

    def getTimeStamp(self):
        return time.strftime("%Y/%m/%d %X")

    def processSubscriptionStatus(self, event):
        timeStamp = self.getTimeStamp()
        for msg in event:
            topic = msg.correlationId().value()
            LOG.debug(f"{timeStamp}: {topic}")
            LOG.debug(msg)
            if msg.messageType() == blpapi.Names.SUBSCRIPTION_FAILURE:
                LOG.warning(f"Subscription for {topic} failed")
            elif msg.messageType() == blpapi.Names.SUBSCRIPTION_TERMINATED:
                # Subscription can be terminated if the session identity
                # is revoked.
                LOG.warning(f"Subscription for {topic} TERMINATED")

    def processSubscriptionDataEvent(self, event):
        for msg in event:
            topic = msg.correlationId().value()
            if topic in self._topics:
                self._data_dict[topic].update(
                    {k: v for k, v in msg.toPy().items() if k in self._fields}
                )

    def processMiscEvents(self, event):
        for msg in event:
            if msg.messageType() == blpapi.Names.SLOW_CONSUMER_WARNING:
                LOG.warning(
                    f"{blpapi.Names.SLOW_CONSUMER_WARNING} - The event queue is "
                    + "beginning to approach its maximum capacity and "
                    + "the application is not processing the data fast "
                    + "enough. This could lead to ticks being dropped"
                    + " (DataLoss).\n"
                )

            elif msg.messageType() == blpapi.Names.SLOW_CONSUMER_WARNING_CLEARED:
                LOG.warning(
                    f"{blpapi.Names.SLOW_CONSUMER_WARNING_CLEARED} - the event "
                    + "queue has shrunk enough that there is no "
                    + "longer any immediate danger of overflowing the "
                    + "queue. If any precautionary actions were taken "
                    + "when SlowConsumerWarning message was delivered, "
                    + "it is now safe to continue as normal.\n"
                )

            elif msg.messageType() == blpapi.Names.DATA_LOSS:
                LOG.warning(msg)
                topic = msg.correlationId().value()
                LOG.warning(
                    f"{blpapi.Names.DATA_LOSS} - The application is too slow to "
                    + "process events and the event queue is overflowing. "
                    + f"Data is lost for topic {topic}.\n"
                )

            elif event.eventType() == blpapi.Event.SESSION_STATUS:
                # SESSION_STATUS events can happen at any time and
                # should be handled as the session can be terminated,
                # e.g. session identity can be revoked at a later
                # time, which terminates the session.
                if msg.messageType() == blpapi.Names.SESSION_TERMINATED:
                    LOG.debug("Session terminated")
                    return

    def processEvent(self, event, _session):
        try:
            if event.eventType() == blpapi.Event.SUBSCRIPTION_DATA:
                self.processSubscriptionDataEvent(event)
            elif event.eventType() == blpapi.Event.SUBSCRIPTION_STATUS:
                self.processSubscriptionStatus(event)
            else:
                self.processMiscEvents(event)
        except blpapi.Exception as exception:
            LOG.warning(f"Failed to process event {event}: {exception}")
        self._data_event.set()
        return False


def parseDummyCmdLine(topics, fields, interval):
    """Simulate parsing command line arguments, reuse the Bloomberg sample code."""

    parser = ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="Asynchronous subscription with event handler",
    )
    addConnectionAndAuthOptions(parser)
    addSubscriptionOptions(parser)

    parser.add_argument(
        "-q",
        "--event-queue-size",
        dest="eventQueueSize",
        help="The maximum number of events that is buffered by the session (default: %(default)d)",
        type=int,
        metavar="eventQueueSize",
        default=DEFAULT_QUEUE_SIZE,
    )

    args = []
    if topics:
        for t in topics:
            args.append("-t")
            args.append(t)
    if fields:
        for f in fields:
            args.append("-f")
            args.append(f)

    if interval is not None:
        args.append("-i")
        args.append(str(interval))

    LOG.info(f"args={args}")

    options = parser.parse_args(args)

    return options


def bloomberg_subscribe(
    topics: List[str], fields: List[str], interval: Optional[int] = None
) -> Dict:

    topics = list(topics)
    fields = list(fields)

    LOG.info(f"topics={topics}")
    LOG.info(f"fields={fields}")
    LOG.info(f"interval={interval}")

    options = parseDummyCmdLine(topics, fields, interval)

    sessionOptions = createSessionOptions(options)
    setSubscriptionSessionOptions(sessionOptions, options)
    sessionOptions.setMaxEventQueueSize(options.eventQueueSize)
    handler = SubscriptionEventHandler(topics, fields)
    session = blpapi.Session(sessionOptions, handler.processEvent)

    try:
        if not session.start():
            return "Failed to start session."

        if not session.openService(options.service):
            return "Failed to open the service."

        subscriptions = createSubscriptionList(options)
        session.subscribe(subscriptions)

        while True:
            try:
                handler.wait_for_data_event()
                data = handler.get_data_dict()
                yield data
            finally:
                handler.clear_data_event()

    finally:
        session.stop()


def show_bloomberg_float(d: Dict, topic: str, field: str) -> float:
    return d.get(topic, {}).get(field, 0.0)


def show_bloomberg_date_or_time(d: Dict, topic: str, field: str) -> str:
    """Some fields flip between time and date."""
    field_value = d.get(topic, {}).get(field)
    return field_value.isoformat() if field_value else ""


def show_bloomberg_data(
    d: Dict,
    topics: List[str],
    fields: List[str],
    show_topics: bool = True,
    show_fields: bool = True,
) -> List[Any]:
    rows = []
    if show_fields:
        row = [""]
        row.extend(fields)
        rows.append(row)
    for topic in topics:
        row = []
        if show_topics:
            row.append(topic)
        td = d.get(topic, {})
        for field in fields:
            field_value = td.get(field)
            if isinstance(
                field_value, (datetime.time, datetime.datetime, datetime.date)
            ):
                # To format fields that flip between time and date
                field_value = field_value.isoformat()
            row.append(field_value)
        rows.append(row)

    return rows


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    topics = ["EURUSD Curncy", "XBTUSD BGN Curncy"]
    fields = ["BID", "LAST_UPDATE_BID_RT"]
    interval = 5
    for d in bloomberg_subscribe(topics, fields, interval=10):
        print(show_bloomberg_data(d, topics, fields))

__copyright__ = """
Copyright 2021, Bloomberg Finance L.P.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:  The above
copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
