import sys
import argparse
from candy.base import Core

def my_print(msg):
    print("CANDY: ", msg)

# Argument parser 
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", help="SocketCAN interface name",)
parser.add_argument("-l", "--log", help="Import log file",)
args = parser.parse_args()

# ----------------------------- MAIN ----------------------------- 

print("\033[31mCANdy - Automated tool for CAN bus message mapping\033[0m")
print("\033[37mVersion: early beta\033[0m")

candy = Core()

if not (args.interface or args.log):
    print(">> Missing arguments")
    sys.exit(1)

if args.interface:
    candy.can_monitor(args.interface, [ my_print ])

if args.log:
    candy.can_offline(args.log)

# Load and run plugin
candy.find_plugin()
candy.run_plugin()

# End application after plugin is done working
if args.interface:
    candy.bus.stop()
