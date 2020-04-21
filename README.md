## CANdy - Automated tool for CAN bus message mapping
Last edit: 04-20-2020

### Install and run app with virtual CAN interface
```sh
$ ./setup.sh                    # Initialize project with setup.sh
$ sudo ./setup_vcan.sh          # Initialize vcan interface
$ source __venv/bin/activate    # Activate Python virtual environment
$ python3 ./candy_app           # Run application
```

In different terminal, you can use `cansend` utility to send messages to vcan0 interface to as an external message source.

### Modules
You can write your own modules using framework API. Store modules in *modules/* directory to be loaded by the main application. There is template in *misc/* directory for you to use.  

### Setup CAN interface manually with SocketCAN
  1. `dmesg` - to check presence of the CAN device in the computer
  2. `sudo ip link set can0 type can bitrate 500000` - configure high-speed CAN (500kbps) or low-speed CAN (125kbps)
  3. `sudo ip link set up can0` - enable the interface
  4. `ip link show can0` - check the status of the interface
  5. `candump can0` - test communication with SocketCAN user-space application candump
