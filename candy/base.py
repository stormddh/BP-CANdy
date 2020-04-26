import importlib
import pkgutil
from threading import Thread
from can import CanutilsLogReader

from lib.api import API
from lib.bus import Bus
from lib.message import Messages
#from lib.definitions import Definition

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
        print(">> Starting monitoring session")
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
        for msg in self.db.messages:
            print("ID: ", msg, self.db.messages[msg])

    def console(self):
        candy = API(self.db, self.bus)

        while True:
            user = input("candy> ").split()
            if len(user) == 0:
                print("use help for commands")
                continue

            command = user.pop(0)
            if command == "help":
                sep = '\t'
                print("Commands:")
                print(f"\tget{3*sep}- get received all messages")
                print(f"\tsend <id> <data>{sep}- send message (use HEX values)")
                print(f"\tfilter <id> <mask>{sep}- set filter (use HEX values)")
                print(f"\tquit{3*sep}- exit application")
            elif command == "get":
                candy.get_messages()
            elif command == "send":
                candy.send_message(int(user[0], 16), user[1])
            elif command == "filter":
                candy.set_filter_rule(int(user[0], 16), int(user[1], 16))
            elif command == "quit":
                break
            else:
                print("Invalid input")

    def find_plugin(self):
        self.modules = [
            name
            for finder, name, ispkg
            in pkgutil.iter_modules(path=["./modules"])
        ]

        print(">> Found modules:")
        for number, name in enumerate(self.modules, 1):
            print(number, name)
        print("0 default console mode")

    def run_plugin(self):
        while(1):
            try:
                index = int(input(">> Choose module: "))
                if index - 1 in range(0, len(self.modules)) or not index:
                    break
                else:
                    print("Number out of range")
            except ValueError:
                print("Invalid input")

        #try:
        #except Exception as e:
        #    print("Plugin does not work properly")
        #    print(e)

        # INSECURE STUFF
        if index != 0:
            module = importlib.import_module(
                f".{self.modules[index - 1]}",
                package='modules',
            )

            module.run(module.candyAPI.API(self.db, self.bus))
        else:
            self.console()
