import can
import cantools

class Messages:
    def __init__(self):
        self._messages = {}
        self._definitions = None
        self._import_file = None

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

    @property
    def import_file(self):
        return self._import_file

    @import_file.setter
    def import_file(self, value):
        self.self._import_file = value

    def save_message(self, msg):
        if msg.arbitration_id not in self.messages:
            self.messages[msg.arbitration_id] = dict()
            self.messages[msg.arbitration_id]['data'] = []
            self.messages[msg.arbitration_id]['count'] = 0
            for i in range(len(msg.data)):
                self.messages[msg.arbitration_id]['data'].append(set())

        self.messages[msg.arbitration_id]['count'] += 1
        data = bytes(msg.data)
        for i in range(len(data)):
            self.messages[msg.arbitration_id]['data'][i].add(data[i])

    def import_messages(self, filename):
        for msg in can.CanutilsLogReader(filename):
            save_message(msg)

    def import_definitions(self, filename):
        self.definitions = cantools.database.load_file(filename)

    def decode_message(self, msg_id, msg_data):
        return self.definitions.decode_message(msg_id, msg_data)

    def export_messages():
        pass

# TODO: finish Message methods
