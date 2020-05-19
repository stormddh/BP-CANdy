import can
import cantools

from copy import deepcopy

class Message:
    def __init__(self):
        self._count = 0
        self._data = []
        self._label = ""
        self._last = None
        self._changed = False
        self._periodic = 0

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, value):
        self._last = value

    @property
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, value):
        self._changed = value

    @property
    def periodic(self):
        return self._periodic

    @periodic.setter
    def periodic(self, value):
        self._periodic = value

    def update_signals(self, data):
        old_data = deepcopy(self.data)

        for i in range(len(data)):
            self.data[i].add(data[i])

        if old_data == self.data:
            self.changed = False
        else:
            self.changed = True

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
        self._import_file = value

    def save_message(self, msg):
        if msg.arbitration_id not in self.messages:
            self.messages[msg.arbitration_id] = Message()
            for i in range(len(msg.data)):
                self.messages[msg.arbitration_id].data.append(set())

        message = self.messages[msg.arbitration_id]

        if len(msg.data) > len(message.data):
            for i in range(len(msg.data)-len(message.data)):
                message.data.append(set())

        if message.last:
            new = msg.timestamp - message.last.timestamp
            message.periodic = (message.periodic * message.count + new) / (message.count + 1)

        message.last = msg
        message.count += 1
        message.update_signals(bytes(msg.data))

    def import_messages(self, filename):
        for msg in can.CanutilsLogReader(filename):
            save_message(msg)

    def import_definitions(self, filename):
        try:
            self.definitions = cantools.database.load_file(filename)
        except Exception as e:
            print(f"Could not import definitions: { e }")

    def decode_message(self, msg_id, msg_data):
        return self.definitions.decode_message(msg_id, msg_data)

    def export_messages():
        pass

# TODO: finish Message methods
