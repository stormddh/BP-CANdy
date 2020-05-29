import cmd
import re

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
        self._candy_API = value

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, value):
        self._interface = value

    def check_arg(self, args):
        regex_hex = re.compile("^[a-fA-F\d]+$")
        for arg in args:
            if not regex_hex.match(arg):
                print("Argument has invalid value")
                return False

        return True

    # ----- basic commands -----
    def emptyline(self):
        pass

    def do_monitor(self, arg):
        """Print out messages received from the CAN interface"""
        input("Press 'Enter' to start, then write 'q' to quit")
        self.candy_core.verbose = True
        print("\033[2J\033[;H")
        while True:
            command = input()
            if command == "q":
                self.candy_core.verbose = False
                break

    def do_get(self, arg):
        """get <id:optional> - List all received messages or one message with details"""
        if arg:
            if not self.check_arg([arg]):
                return

            msg_id = int(arg, 16)
            msg = self.candy_API.get_messages(msg_id)

            if msg:
                print(f"ID: {msg_id:x}")
                if msg.label:
                    print(f"Label: {msg.label}")
                print(f"Count: {msg.count}")
                print("Recorded signals:")

                for num, field in enumerate(msg.data):
                    print(f"{num}: {sorted(field)}")

                if self.candy_API.db.definitions:
                    try:
                        msg_def = self.candy_API.db.definitions.get_message_by_frame_id(msg_id)
                        print(f"Name: {msg_def.name}")
                        print("Signals:")
                        print("=====================================")
                        for s in msg_def.signals:
                            print(f"{s.name:<20} [{s.minimum}|{s.maximum}]\t{s.unit}")
                        print("=====================================")
                        print(msg_def.layout_string())
                    except:
                        pass
            else:
                print("Message not found")
        else:
            messages = self.candy_API.get_messages()
            print("  ID|\t count|\tperiod|label\t|name")
            print("==========================================================")

            for m_id, m_val in sorted(messages.items()):
                period = "N" if m_val.periodic == 0 else int(m_val.periodic * 1000)
                name = ""
                if self.candy_API.db.definitions:
                    try:
                        name = self.candy_API.db.definitions.get_message_by_frame_id(m_id).name
                    except:
                        pass
                print(f"{m_id:>4x}\t{m_val.count:>6}{period:>8}\t\t{m_val.label}\t{name}")

            print("==========================================================")
            print(f"{len(messages.keys())} unique IDs")

    def do_send(self, arg):
        """send <id> <data> - Send a CAN message (use HEX values)"""
        args = parse(arg)

        if len(args) != 2:
            print("Missing arguments")
            return
        elif not self.check_arg(args):
            return

        self.candy_API.send_message(int(args[0], 16), args[1])

    def do_filter(self, arg):
        """filter <id> <mask> or 'reset' - Set filter (use HEX values, default mask is xFFFFF)"""
        args = parse(arg)
        if not args:
            for f in self.candy_API.bus.filter_rules:
                print(f"CAN ID: {f['can_id']:x}, MASK: {f['can_mask']:x}")
        elif args[0] == "reset":
            self.candy_API.reset_filter()
        elif self.check_arg(args):
            if len(args) > 1:
                mask = int(args[1], 16)
            else:
                mask = 0xFFFFF
            self.candy_API.set_filter_rule(int(args[0], 16), mask)

    def do_import(self, arg):
        """import <file> - Import CAN message definitions"""
        if not arg:
            print("Missing argument")
            return

        try:
            self.candy_core.db.import_definitions(arg)

            if self.candy_core.db.definitions:
                print(f"Imported {len(self.candy_core.db.definitions.messages)} definitions")
        except Exception as e:
            print("Import was not successful", e)

    def do_mod(self, arg):
        """mod <name:optional> - Run user module or list available modules"""
        if not arg:
            print("Modules:")
            for number, name in enumerate(self.candy_core.modules, 1):
                print(f"\t{number} {name}")
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

    def do_label(self, arg):
        """label <id> <label> - Set label for a message"""
        args = parse(arg)
        if len(args) == 2:
            self.candy_API.label_message(int(args[0], 16), args[1])

    def do_nodes(self, arg):
        """nodes 'find':optional - Find and list nodes using CANvas"""
        if arg == "find":
            nodes = self.candy_API.find_nodes()
        else:
            nodes = self.candy_API.get_nodes()
            for n, val in enumerate(nodes):
                print(f"{n}:")
                for i in val:
                    msg_id = int(i)
                    if self.candy_core.db.definitions:
                        msg = get_message_by_frame_id(frame_id)
                        if msg:
                            name = msg.name
                    print(f"\t{msg_id:x} {name}")

        if not len(nodes):
            print("No nodes have been found yet")

    def do_quit(self, arg):
        "Stop recording and close the candy CLI"
        if self.interface:
            self.candy_core.bus.stop()
        return True

# Helper functions
def parse(arg):
    "Convert a series of zero or more numbers to an argument tuple"
    return tuple(arg.split())
