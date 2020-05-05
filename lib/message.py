import can
import cantools

class Message:
    def __init__(self):
        self._count = 0
        self._data = []
        self._label = ""

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

        if len(msg.data) > len(self.messages[msg.arbitration_id].data):
            for i in range(len(msg.data)-len(self.messages[msg.arbitration_id].data)):
                self.messages[msg.arbitration_id].data.append(set())

        self.messages[msg.arbitration_id].count += 1
        data = bytes(msg.data)
        for i in range(len(data)):
            self.messages[msg.arbitration_id].data[i].add(data[i])

    def import_messages(self, filename):
        for msg in can.CanutilsLogReader(filename):
            save_message(msg)

    def import_definitions(self, filename):
        try:
            self.definitions = cantools.database.load_file(filename)
        except UnsupportedDatabaseFormatError:
            print("Unsupported database error")
        except:
            print("Could not import definitions")

    def decode_message(self, msg_id, msg_data):
        return self.definitions.decode_message(msg_id, msg_data)

    def export_messages():
        pass

# TODO: finish Message methods
