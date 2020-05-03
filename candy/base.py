import importlib
import pkgutil
from threading import Thread
from can import CanutilsLogReader

from lib.api import API
from lib.bus import Bus
from lib.message import Messages

class Core:
    def __init__(self):
        self._modules = []
        self._db = Messages()
        self._bus = None

    @property
    def modules(self):
        return self._modules

    @modules.setter
    def modules(self, value):
        self._modules = value

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        self._db = value

    @property
    def bus(self):
        return self._bus

    @bus.setter
    def bus(self, value):
        self._bus = value

    def can_monitor(self, interface, bitrate, user_callback=[]):
        print(f"Starting monitoring session on { interface }")
        callback = [ self.db.save_message ]
        callback.extend(user_callback)
        self.bus = Bus(interface, bitrate)

        # Create CAN bus deamon in a new thread
        worker = Thread(
            target=self.bus.start,
            args=(callback,),
            daemon=True,
        )
        worker.start()

    def can_offline(self, log_file):
        print(">> Importing data")
        log_data = CanutilsLogReader(log_file)

        for msg in log_data:
            self.db.save_message(msg)
        for msg in sorted(self.db.messages):
            print("ID: ", msg)
            for i in self.db.messages[msg]:
                if len(self.db.messages[msg][i]):
                    print(i, self.db.messages[msg][i], "; ", end="")
            print()

        self.db.import_file = log_file

    def find_plugin(self):
        self.modules = [
            name
            for finder, name, ispkg
            in pkgutil.iter_modules(path=["./modules"])
        ]
        return self.modules

    def run_plugin(self, index):
        #try:
        module = importlib.import_module(
            f".{self.modules[index]}",
            package='modules',
        )

        module.run(module.candyAPI.API(self))

        #except Exception as e:
        #    print("Plugin does not work properly:", e)
