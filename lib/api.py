class API:

    def __init__(self, messages, bus):
        self._db = messages
        self._bus = bus

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        self._db = value

    @property
    def bus(self):
        return self._bus

    @bus.setter
    def bus(self, value):
        self._bus = value

    def create_data(self, msg):
        return [int(x, 16) for x in msg]

    def get_messages(self, msg_id=None):
        if msg_id:
            print(self.db.messages[msg_id])
            return self.db.messages[msg_id]
        else:
            for msg in self.db.messages:
                print("ID:", hex(msg))
            return self.db.messages

    def send_message(self, msg_id, msg_data):
        self.bus.send_message(msg_id, self.create_data(msg_data))

    def send_periodic_time(self, msg_id, msg_data, period, limit=0):
        self.bus.send_message_periodic(msg_id, self.create_data(msg_data), period, limit)

    def send_periodic_count(self, msg_id, msg_data, period, number):
        limit = period * number
        self.bus.send_message_periodic(msg_id, self.create_data(msg_data), period, limit)

    def set_filter_rule(self, msg_id, mask, extended=False):
        rule = { "can_id" : msg_id,
                 "can_mask" : mask,
                 "extended" : extended,
            }
        self.bus.filter_rules.append(rule)
        self.bus.can_bus.set_filters(self.bus.filter_rules)

    def reset_filter(self):
        self.bus.can_bus.set_filters(None)

# TODO: finish API methods
