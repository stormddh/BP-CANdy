import sys
import argparse

from lib.cli import CandyCLI

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", help="SocketCAN interface name")
parser.add_argument("-l", "--log", help="Import log file")
parser.add_argument("-o", "--out", help="Log CAN messages from the session", action="store_true")
parser.add_argument("-b", "--bitrate", help="CAN bus channel bitrate (default 500000")
args = parser.parse_args()

# ----------------------------- MAIN -----------------------------

print("\033[31mCANdy - Automated tool for CAN bus message mapping\033[0m")
print("\033[37;2mVersion: early beta\033[0m")

if not (args.interface or args.log):
    print("Missing arguments")
    sys.exit(1)

# Run CLI application
try:
    CandyCLI(args).cmdloop()
except KeyboardInterrupt:
    print("Quitting CANdy")
    sys.exit(1)
except OSError as o:
    print("Cannot start CANdy:", o)
    sys.exit(1)
