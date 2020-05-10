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
        self._online = False
        self._verbose = False

    # verbose switch on/offs

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

    @property
    def online(self):
        return self._online

    @online.setter
    def online(self, value):
        self._online = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

    def my_print(self, msg):
        if self.verbose:
            if self.db.definitions:
                try:
                    decoded = self.db.decode_message(msg.arbitration_id, msg.data)
                    print(f"CANDY: T: { msg.timestamp } { hex(msg.arbitration_id) } { decoded }")
                except:
                    print(f"CANDY: { msg }")
            else:
                print(f"CANDY: { msg }")

    def can_monitor(self, interface, bitrate, user_callback=[]):
        print(f"Starting monitoring session on { interface }")
        callback = [ self.db.save_message, self.my_print ]
        callback.extend(user_callback)
        self.bus = Bus(interface, bitrate)

        # Create CAN bus deamon in a new thread
        worker = Thread(
            target=self.bus.start,
            args=(callback,),
            daemon=True,
        )
        worker.start()

        self.online = True

    def can_offline(self, log_file):
        print("Importing data")

        try:
            log_data = CanutilsLogReader(log_file)
            self.bus = Bus(None, 0)
            self.bus.history = log_data

            for msg in log_data:
                self.db.save_message(msg)

            self.db.import_file = log_file
        except Exception as e:
            print(f"Import was not successful: { e }")

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
