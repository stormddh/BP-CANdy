import lib.api as candyAPI

# Example ddos module
def run(candy):
    # Periodically send messages to the can bus.
    # These functions will be executed sequentially.
    # frame id, frame data, period [s], number or timeout [s]
    candy.send_periodic_count(0x3, "12345678", 0.1, 5)
    candy.send_periodic_time(0x4, "1234ABCD", 0.5, 5)
