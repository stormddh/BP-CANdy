import can

class Messages:

    def __init__(self):
        self.messages = {}

    def save_message(self, msg):
        if msg.arbitration_id not in self.messages:
            self.messages[msg.arbitration_id] = set()
        self.messages[msg.arbitration_id].add(bytes(msg.data))
    
    def import_messages(self, filename):
        for msg in can.CanutilsLogReader(filename):
            save_message(msg)
         
    def export_messages():
        pass
            
# TODO: finish Message methods
