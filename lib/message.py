import can
import cantools

class Messages:

    def __init__(self):
        self._messages = {}
        self._definitions = None

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, value):
        self._messages = value

    @property
    def definitions(self):
        return self._definitions

    @definitions.setter
    def definitions(self, value):
        self._definitions = value

    def save_message(self, msg):
        if msg.arbitration_id not in self.messages:
            self.messages[msg.arbitration_id] = dict()
            for i in range(8):
                # not really memory efficient
                self.messages[msg.arbitration_id][i] = set()
        data = bytes(msg.data)
        for i in range(len(data)):
            self.messages[msg.arbitration_id][i].add(data[i])

    def import_messages(self, filename):
        for msg in can.CanutilsLogReader(filename):
            save_message(msg)

    def import_definitions(self, filename):
        self.definitions = cantools.database.load_file(filename)

    def export_messages():
        pass

# TODO: finish Message methods
