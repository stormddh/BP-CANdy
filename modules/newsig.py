import lib.api as candyAPI
import time

# Example ddos module
def run(candy):
    # Periodically send messages to the can bus.
    # These functions will be executed sequentially.
    # frame id, frame data, period [s], number or timeout [s]
    duration = input("How long should I run? ")
    changed = []
    end = 0
    while end < int(duration):
        messages = candy.get_messages()
        for m, val in messages.items():
            if m not in changed and val.changed:
                print(f"{m:x}")
                changed.append(m)
        time.sleep(0.01)
        end += 0.01
    #print(candy.db.messages)
    #print(candy.get_messages())
