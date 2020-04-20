import lib.api as candyAPI
import time

# Example ddos module
def run(candy):
    for _ in range(5):
        candy.send_message(1, [1,1,1,1,1,1,1,1])
        time.sleep(2)
        candy.get_messages()
