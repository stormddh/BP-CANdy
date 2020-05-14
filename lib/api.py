import lib.canvas.source.mapper

class API:
    def __init__(self, core):
        self._db = core.db
        self._bus = core.bus
        self._online = core.online

        if self.bus:
            self._history_iter = iter(self._bus.history)
        else:
            self._history_iter = None

    @property
    def db(self):
        return self._db

    @property
    def bus(self):
        return self._bus

    @property
    def history_iter(self):
        return self._history_iter

    @history_iter.setter
    def history_iter(self, value):
        self._history_iter = value

    @property
    def online(self):
        return self._online

    def create_data(self, msg):
        split = [msg[i:i+2] for i in range(0, len(msg), 2)]
        return [int(x, 16) for x in split]

    def read(self):
        try:
            msg = next(self.history_iter)
            return msg
        except TypeError:
            print("Bus is not available")
        except:
            print("No new message")

    def get_messages(self, msg_id=None):
        if msg_id:
            try:
                return self.db.messages[msg_id]
            except KeyError:
                return None
        else:
            return self.db.messages

    def get_message_log(self, msg_id, last=None):
        result = []
        #this could be faster
        for m in self._bus.history:
            if m.arbitration_id == msg_id:
                result.append(m)

        if last and last < len(result):
            return result[-last:]
        else:
            return result

    def send_message(self, msg_id, msg_data):
        if not (len(msg_data) <= 16 and msg_id <= 0x7FF):
            print("ID must be max 0x7FF and message can be long at most 8 bytes.")
        elif self.online:
            self.bus.send_message(msg_id, self.create_data(msg_data))
        else:
            print("Cannot send message")

    def send_periodic_time(self, msg_id, msg_data, period, limit=0):
        if not (len(msg_data) <= 16 and msg_id <= 0x7FF):
            print("ID must be max 0x7FF and message can be long at most 8 bytes.")
        elif self.online:
            self.bus.send_message_periodic(msg_id, self.create_data(msg_data), period, limit)
        else:
            print("Cannot send message")

    def send_periodic_count(self, msg_id, msg_data, period, number):
        if not (len(msg_data) <= 16 and msg_id <= 0x7FF):
            print("Highest possible ID is 0x7FF and message can be long at most 8 bytes.")
        elif self.online:
            limit = period * number
            self.bus.send_message_periodic(msg_id, self.create_data(msg_data), period, limit)
        else:
            print("Cannot send message")

    def decode_message(self, msg):
        if self.db.definitions:
            return self.db.decode_message(msg.arbitration_id, msg.data)
        else:
            print("Missing definitions")

    def label_message(self, msg_id, label):
        if msg_id in self.db.messages:
            self.db.messages[msg_id].label = label
        else:
            print("Message not found")

    def set_filter_rule(self, msg_id, mask, extended=False):
        # CAN ID filter - using hexadecimal values
        # http://www.cse.dmu.ac.uk/~eg/tele/CanbusIDandMask.html
        if msg_id <= 0x7FF and mask <= 0x1FFFFFFF:
            rule = { "can_id" : msg_id,
                     "can_mask" : mask,
                     "extended" : extended,
                }
        else:
            print("Invalid argument values")
            return

        if rule not in self.bus.filter_rules:
            self.bus.filter_rules.append(rule)
        self.bus.can_bus.set_filters(self.bus.filter_rules)

        return self.bus.filter_rules

    def reset_filter(self):
        self.bus.can_bus.set_filters(None)
        self.bus.filter_rules.clear()

    def get_nodes(self):
        return self.bus.nodes

    def find_nodes(self):
        if self.bus:
            file_name = "misc/tmp.canvas"
            with open(file_name, "w") as fp:
                out = ""
                for m in self.bus.history:
                    out += f"{m.timestamp} {m.channel} {m.arbitration_id}#\n"
                fp.write(out)
            return self.bus.find_nodes(file_name)
