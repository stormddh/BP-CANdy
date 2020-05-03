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
            msg = self.candy_API.get_messages(int(arg, 16))
            if msg:
                print(f"ID: { int(arg, 16) }")
                print(f"Count: { msg['count'] }")
                print("Signals:")
                for num, field in enumerate(msg['data']):
                    print(f"{ num }: { sorted(field) }")
            else:
                print("Message not found")
        else:
            messages = self.candy_API.get_messages()
            for m in messages.keys():
                #print(messages[m])
                print(f"ID: { hex(m) } ({ messages[m]['count'] })")
            print("=================")
            print(f"{ len(messages.keys()) } unique IDs")

    def do_send(self, arg):
        """send <id> <data> - Send a CAN message (use HEX values)"""
        args = parse(arg)
        if not args:
            print("Missing arguments")
            return
        self.candy_API.send_message(int(args[0], 16), args[1])

    def do_filter(self, arg):
        """filter <id> <mask> or 'reset' - Set filter (use HEX values, default mask is xFFFFF)"""
        args = parse(arg)
        if not args:
            for f in self.candy_API.bus.filter_rules:
                print(f"CAN ID: { hex(f['can_id']) }, MASK: { hex(f['can_mask']) }")
        elif args[0] == "reset":
            self.candy_API.reset_filter()
        else:
            if len(args) > 1:
                mask = int(args[1], 16)
            else:
                mask = 0xFFFFF
            self.candy_API.set_filter_rule(int(args[0], 16), mask)

    def do_import(self, arg):
        """import <file> - Import CAN message definitions"""
        args = parse(arg)
        if not args:
            print("Missing arguments")
            return
        self.candy_core.db.import_definitions(args[0])

    def do_mod(self, arg):
        """mod <name:optional>- Run user module or list available modules"""
        if not arg:
            print("Modules:")
            for number, name in enumerate(self.candy_core.modules, 1):
                print(f"\t{ number } { name }")
            index = input("Choose module #: ")
        elif arg in self.candy_core.modules:
            self.candy_core.run_plugin(self.candy_core.modules.index(arg))
            return
        else:
            print(f"Module '{arg}' does not exist")
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

# Helper functions
def parse(arg):
    "Convert a series of zero or more numbers to an argument tuple"
    return tuple(arg.split())

def my_print(msg):
    print("CANDY: ", msg)
