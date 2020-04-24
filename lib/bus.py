import can
import asyncio
import time
from datetime import datetime

class Bus():
    def __init__(self, interface="vcan0"):
        self.nodes = []
        self.can_bus = can.ThreadSafeBus(
            bustype="socketcan",
            channel=interface,
            bitrate=500000,
            receive_own_messages=True,
        )
        self.filter_rules = []
        self.loop = None
        self.notifier = None
        self.end = False

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
        # TODO: add date and time of log
        logger = can.Logger(f"log/{datetime.now().isoformat(timespec='seconds')}.log")

        # Set up listeners and add callback functions
        listeners = [
            reader,         # AsyncBufferedReader() listener
            logger          # Regular Listener object
        ]
        listeners.extend(callback)

        self.loop = asyncio.get_event_loop()

        # Create Notifier with an explicit loop to use for scheduling of callbacks
        self.notifier = can.Notifier(
            self.can_bus,
            listeners,
            timeout=1.0,
            loop=self.loop
        )

        while True:
        # Wait for next message from AsyncBufferedReader
            msg = await reader.get_message()

    def start(self, callback):
        asyncio.run(self.listen(callback))

    def stop(self):
        print('>> Exiting...')
        self.notifier.stop()
        self.can_bus.shutdown()
