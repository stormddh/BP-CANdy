class API:

    def __init__(self, messages, bus):
        self.db = messages
        self.bus = bus
    
    def get_messages(self, msg_id=None):
        if msg_id:
            print(self.db.messages[msg_id])
            return self.db.messages[msg_id]
        else:
            for msg in self.db.messages:
                print(msg, self.db.messages[msg])
            return self.db.messages

    def send_message(self, msg_id, data):
        self.bus.send_message(data)

# TODO: finish API methods
