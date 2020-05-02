import can
import asyncio
import time

from lib.canvas.source import mapper as canvas
from datetime import datetime

class Bus():
    def __init__(self, interface, br):
        self._can_bus = can.ThreadSafeBus(
            bustype="socketcan",
            channel=interface,
            bitrate=br,
            receive_own_messages=True,
        )
        self._filter_rules = []
        self._nodes = []
        self._history = []
        self._loop = None
        self._notifier = None

    @property
    def can_bus(self):
        return self._can_bus

    @property
    def filter_rules(self):
        return self._filter_rules

    @filter_rules.setter
    def filter_rules(self):
        return self._filter_rules

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, value):
        self._history = value

    @property
    def notifier(self):
        return self._notifier

    @notifier.setter
    def notifier(self, value):
        self._notifier = value

    def send_message(self, msg_id, msg_data):
        try:
            msg = can.Message(arbitration_id=msg_id, data=msg_data)
            self.can_bus.send(msg)
            print(">> Message sent on {}".format(self.can_bus.channel_info))
        except can.CanError:
            print(">> Message NOT sent")

    def send_message_periodic(self, msg_id, msg_data, period, limit):
        msg = can.Message(arbitration_id=msg_id, data=msg_data)

        try:
            if limit:
                print("Limit: ", limit)
                task = self.can_bus.send_periodic(msg, period, store_task=True)
                if not isinstance(task, can.LimitedDurationCyclicSendTaskABC):
                    task.stop()
                    return
                time.sleep(limit)
                task.stop()
            else:
                # make asynchronous
                task = self.can_bus.send_periodic(msg, period, store_task=False)
                time.sleep(10)
                task.stop()
        except can.CanError:
            print(">> Message NOT sent")

    async def listen(self, callback):
        reader = can.AsyncBufferedReader()
        logger = can.Logger(f"log/{datetime.now().isoformat(timespec='seconds')}.log")

        # Set up listeners and add callback functions
        listeners = [
            reader,         # AsyncBufferedReader() listener
            logger,         # Regular Listener object
        ]
        listeners.extend(callback)

        loop = asyncio.get_event_loop()

        # Create Notifier with an explicit loop to use for scheduling of callbacks
        self.notifier = can.Notifier(
            self.can_bus,
            listeners,
            timeout=1.0,
            loop=loop
        )

        while True:
        # Wait for next message from AsyncBufferedReader
            msg = await reader.get_message()
            self.history.append(msg)

    def start(self, callback):
        asyncio.run(self.listen(callback))

    def stop(self):
        print('Exiting...')
        self.notifier.stop()
        self.can_bus.shutdown()

    def find_nodes(self, file_name):
        # import from communication
        self.nodes = canvas.mapper(file_name)
        return self.nodes
