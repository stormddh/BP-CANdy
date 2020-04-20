import can
import asyncio

class Bus():
    def __init__(self, interface="vcan0"):
        self.nodes = []
        self.can_bus = can.ThreadSafeBus(
            bustype="socketcan", 
            channel=interface, 
            bitrate=500000,
            receive_own_messages=True,
        )
        self.loop = None
        self.notifier = None
        self.end = False

    def send_message(self, msg):
        try:
            self.can_bus.send(can.Message(data=msg))
            print(">> Message sent on {}".format(self.can_bus.channel_info))
        except can.CanError:
            print(">> Message NOT sent")

    async def listen(self, callback):
        reader = can.AsyncBufferedReader()
        # TODO: add date and time of log
        logger = can.Logger('log/can.log')

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
        print('>> Done!')
        self.notifier.stop()
        self.can_bus.shutdown()
