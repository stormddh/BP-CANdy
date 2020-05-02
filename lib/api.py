import lib.canvas.source.mapper

class API:

    def __init__(self, core):
        self._db = core.db
        self._bus = core.bus

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

    def create_data(self, msg):
        return [int(x, 16) for x in msg]

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
            for msg in sorted(self.db.messages):
                print("ID:", hex(msg))
            return self.db.messages

    def send_message(self, msg_id, msg_data):
        self.bus.send_message(msg_id, self.create_data(msg_data))

    def send_periodic_time(self, msg_id, msg_data, period, limit=0):
        self.bus.send_message_periodic(msg_id, self.create_data(msg_data), period, limit)

    def send_periodic_count(self, msg_id, msg_data, period, number):
        limit = period * number
        self.bus.send_message_periodic(msg_id, self.create_data(msg_data), period, limit)

    def decode_message(self, msg):
        if self.db.definitions:
            return self.db.decode_message(msg.arbitration_id, msg.data)
        else:
            print("Missing definitions")

    def set_filter_rule(self, msg_id, mask, extended=False):
        rule = { "can_id" : msg_id,
                 "can_mask" : mask,
                 "extended" : extended,
            }
        self.bus.filter_rules.append(rule)
        self.bus.can_bus.set_filters(self.bus.filter_rules)

    def reset_filter(self):
        self.bus.can_bus.set_filters(None)

    def get_nodes(self):
        return self.bus.nodes()

    def find_nodes(self):
        if self.bus:
            file_name = "misc/tmp.canvas"
            with open(file_name, "w") as fp:
                out = ""
                for m in self.bus.history:
                    out += f"{m.timestamp} {m.channel} {m.arbitration_id}#\n"
                fp.write(out)
            return self.bus.find_nodes(file_name)

# TODO: finish API methods
