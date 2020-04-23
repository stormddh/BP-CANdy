import lib.api as candyAPI

# Example ddos module
def run(candy):
    # Periodically send messages to the can bus.
    # These functions will be executed sequentially.
    # frame id, frame data, period [s], number or timeout [s]
    candy.send_periodic_count(3, [1,2,3,4,5,6,7,8], 0.1, 5)
    candy.send_periodic_time(4, [1,2,3,4,1,2,3,4], 0.5, 5)
