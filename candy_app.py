import sys
import argparse
from candy.base import Core

def my_print(msg):
    print("CANDY: ", msg)

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", help="SocketCAN interface name",)
parser.add_argument("-l", "--log", help="Import log file",)
parser.add_argument("-q", "--quiet", help="Hide incoming messages", action="store_true")
parser.add_argument("-b", "--bitrate", help="CAN bus channel bitrate (default 500000",)
args = parser.parse_args()

# ----------------------------- MAIN -----------------------------

print("\033[31mCANdy - Automated tool for CAN bus message mapping\033[0m")
print("\033[37mVersion: early beta\033[0m")

candy = Core()

if not (args.interface or args.log):
    print(">> Missing arguments")
    sys.exit(1)

if args.interface:

    if args.bitrate:
        bitrate = args.bitrate
    else:
        bitrate = 500000

    if not args.quiet:
        candy.can_monitor(args.interface, bitrate, [ my_print ])
    else:
        candy.can_monitor(args.interface, bitrate)

if args.log:
    candy.can_offline(args.log)

# Load and run plugin
candy.find_plugin()
candy.run_plugin()

# End application after plugin is done working
if args.interface:
    candy.bus.stop()
