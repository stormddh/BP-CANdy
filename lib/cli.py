import cmd

from candy.base import Core
from lib.api import API

class CandyCLI(cmd.Cmd):
    intro = "Use 'help' for commands or 'mod' for modules"
    prompt = "\033[31m>>\033[0m "

    def __init__(self, args):
        super().__init__()

        self._candy_core = Core()
        if args.interface:
            if args.bitrate:
                bitrate = args.bitrate
            else:
                bitrate = 500000

            if not args.quiet:
                self.candy_core.can_monitor(args.interface, bitrate, [ my_print ])
            else:
                self.candy_core.can_monitor(args.interface, bitrate)

            self.interface = True

        if args.log:
            self.candy_core.can_offline(args.log)

        # Load and run plugin
        self.candy_core.find_plugin()
        print("Loaded modules:", " ".join(self.candy_core.modules))

        self._candy_API = API(self._candy_core)
        self._interface = False

    @property
    def candy_core(self):
        return self._candy_core

    @property
    def candy_API(self):
        return self._candy_API

    @candy_API.setter
    def candy_API(self, value):
        print("I was set!")
        self._candy_API = value

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, value):
        self._interface = value

    # ----- basic commands -----
    def emptyline(self):
        pass

    def do_get(self, arg):
        """get <id:optional> - List all received messages or one message with details"""
        if arg:
            msg = candyAPI.get_messages(int(arg[0], 16))
            print(f"ID: { user[0] }")
            print("Signals:")
            for field in msg:
                print(f"{ field }: { sorted(msg[field]) }")
        else:
            for msg in sorted(candyAPI.get_messages()):
                print("ID:", hex(msg))

    def do_send(self, arg):
        """send <id> <data> - Send a CAN message (use HEX values)"""
        args = parse(arg)
        self.candy_API.send_message(int(args[0], 16), args[1])

    def do_filter(self, arg):
        """filter <id> <mask> - Set filter (use HEX values)"""
        args = parse(arg)
        self.candy_API.set_filter_rule(int(args[0], 16), int(args[1], 16))

    def do_import(self, arg):
        """import <file> - Import CAN message definitions"""
        self.candy_core.db.import_definitions(user[0])

    def do_mod(self, arg):
        """mod <name:optional>- Run user module or list available modules"""
        if not arg:
            print("Modules:")
            for number, name in enumerate(self.candy_core.modules, 1):
                print(f"\t{ number } { name }")
            index = input("Choose module: ")
        elif arg in self.candy_core.modules:
            self.candy_core.run_plugin(self.candy_core.modules.index(arg))
            return

        try:
            if int(index)-1 in range(0, len(self.candy_core.modules)):
                self.candy_core.run_plugin(int(index)-1)
            else:
                print("Number out of range")
        except ValueError:
            print("No module selected")

    def do_quit(self, arg):
        "Stop recording and close the candy CLI"
        if self.interface:
            self.candy_core.bus.stop()
        return True

    # ----- cmd methods -----

# Helper functions
def parse(arg):
    "Convert a series of zero or more numbers to an argument tuple"
    return tuple(arg.split())

def my_print(msg):
    print("CANDY: ", msg)
