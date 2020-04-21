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
        self.modules = []
        self.db = Messages()
        self.bus = None
        self.definitions = None

    def can_monitor(self, interface, user_callback):
        print(">> Starting monitoring session")
        callback = [ self.db.save_message ]
        callback.extend(user_callback)
        self.bus = Bus(interface)
        
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
            command = input(">> ")
            if command == "help":
                print("Help:")
                print("\tget")
                print("\tsend")
                print("\tquit")
            elif command == "get":
                candy.get_messages()
            elif command == "send":
                candy.send_message(msg)
            elif command == "quit":
                break
            elif command == "":
                print("use help for commands")
                continue
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
