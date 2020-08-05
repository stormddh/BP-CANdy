## CANdy - Automated tool for CAN bus message mapping
Last edit: 08-05-2020

### Introduction
This tool was created for a [bachelors thesis](https://dspace.cvut.cz/bitstream/handle/10467/88148/F8-BP-2020-Do-Duc%20Huy-thesis.pdf) at CTU Prague. During my research and development I was supervised by people from [Auxilium Cyber Security](https://www.auxiliumcybersec.com), who also gave me the idea for the project. Its main purpose is to make mapping of the CAN messages an easier and more automated task. Unlike other alternatives, we aimed for a simple, lightweight and open-source solution available to everyone interested in analyzing the CAN bus and its messages. Regarding the other CAN bus tools, there are lots of different applications or libraries and this is my attempt to combine them together into an extensive framework with all necessary capabilities.

This tool uses [python-can](https://github.com/hardbyte/python-can) to establish and maintain connection to the CAN bus.

Requirements:
  - Python 3
  - Qt5 (Debian: qt5-default) 
  - Python venv (Debian: python-virtualenv)
  
At this moment, we do not support Windows platform, therefore all instructions are meant for Linux based systems. Install these packages to your system before running CANdy install script.

### Install and run app with virtual CAN interface
```sh
$ ./setup.sh                      # Initialize project with setup.sh
$ sudo ./setup_vcan.sh            # Initialize vcan interface
$ source __venv/bin/activate      # Activate Python virtual environment
$ pip install -r requirements.txt # Install Python dependencies
$ python3 ./candy_app             # Run the CLI application
```
In different terminal, you can use `cansend` utility to send messages to vcan0 interface as an external message source. For more information, enter `help` command to show basic functions provided in the application. 

### When pulling a new version, be sure that all Python requirements are installed.
```sh
$ source __venv/bin/activate    # Activate Python virtual environment
$ pip install -r requirements.txt
```

### Modules
You can write your own modules using framework API. Store modules in *modules/* directory to be loaded by the main application. There is template in *misc/* directory for you to use. Please write your functionality in the `run` function using *candy* API object to call framework API methods.

### API
Parameters marked with * are optional, message IDs message data and filters use hexadecimal values
- `candy.read()` return one message from the message queue (FIFO)
- `candy.get_messages(msg_id*)` return a single message by its ID or a list of all unique messages 
- `candy.get_message_log(msg_id, n*)` return all or *n* last received messages with a certain id
- `candy.send_message(msg_id, msg_data)` send a CAN message
- `candy.send_periodic_time(msg_id, msg_data, period, limit*)` periodically send CAN messages for a specified time limit
- `candy.send_periodic_count(msg_id, msg_data, period, number)` periodically send a specified number of CAN messages
- `candy.decode_message(msg)` decode message using imported DBC/KCD definitions
- `candy.label_message(msg_id, label)` set a label for a message ID
- `candy.set_filter_rule(msg_id, mask)` set a filter for CAN messages and return existing filter rules
- `candy.reset_filter()` reset a filter for CAN messages
- `candy.find_nodes()` detect nodes using CANvas module
- `candy.get_nodes()` returns detected nodes

### Setup CAN interface manually with SocketCAN
  1. `dmesg` - to check presence of the CAN device in the computer
  2. `sudo ip link set can0 type can bitrate 500000` - configure high-speed CAN (500kbps) or low-speed CAN (125kbps)
  3. `sudo ip link set up can0` - enable the interface
  4. `ip link show can0` - check the status of the interface
  5. `candump can0` - test communication with SocketCAN user-space application candump
  
### Testing
In order to try out our tool, there is a candump log file from a real ride of Toyota Auris 2016 in misc/test directory including a DBC definitions file of Toyota Corolla 2017. Although not all messages have matched, we took the advantage of similarities between these two car models as they might use same components.
```sh
# activate python virtual environment and enable vcan0 interface
$ canplayer vcan0=can0 -I misc/test/auris_dump.log    # replay the log file
$ python3 ./candy_app.py -i vcan0                     # launch CANdy
>> import misc/test/corolla_2017.dbc                  # import DBC definitions
>> monitor                                            # monitor messages on vcan0
```

Another way to experiment with CANdy is to use [ICSim](https://github.com/zombieCraig/ICSim) simulator. Please follow usage instructions in the link.

[DEMO](https://drive.google.com/file/d/1UDNLDrn9iLWXE1vykkcJvWqIhud5XX5X/view?usp=sharing) with ICSim

### Contribution
Please share your modules or CAN logs from you car with us! Create a pull request to collaborate on the tool, so that others can benefit from our findings and efforts. Thank you!
