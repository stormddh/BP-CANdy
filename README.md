### CANdy - Automated tool for CAN bus message mapping

Initialize project with setup.sh

Setup CAN interface with SocketCAN
  1. `dmesg` - to check presence of the CAN device in the computer
  2. `sudo ip link set can0 type can bitrate 500000` - configure high-speed CAN (500kbps) or low-speed CAN (125kbps)
  3. `sudo ip link set up can0` - enable the interface
  4. `ip link show can0` - check the status of the interface
  5. `candump can0` - test communication with SocketCAN user-space application candump
