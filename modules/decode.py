import lib.api as candyAPI

# Example ddos module
def run(candy):
    # Periodically send messages to the can bus.
    # These functions will be executed sequentially.
    # frame id, frame data, period [s], number or timeout [s]
    candy.db.import_definitions('./misc/kcd/example.kcd')
    for m in candy.db.definitions.messages:
        print(m)
        for s in m.signals:
            print("\t", s)

    input("Ready?")
    for _ in range(10):
        frame = candy.bus.can_bus.recv()
        print(frame)
        print(candy.decode_message(frame))
