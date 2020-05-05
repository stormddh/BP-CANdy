import lib.api as candyAPI
import time

# Filter module - run with verbose
def run(candy):
    # CAN ID filter - using hexadecimal values
    # http://www.cse.dmu.ac.uk/~eg/tele/CanbusIDandMask.html

    # print only messages with ID 10 (HEX)
    filter_id = 0x10
    filter_mask = 0xFFFFF
    candy.set_filter_rule(filter_id, filter_mask)

    while True:
        filter_id = input("Set message ID filter (hex): ")
        candy.set_filter_rule(int(filter_id, 16), filter_mask)
        print("Filter:", filter_id, filter_mask)
        user = input("end or reset? ")
        if user == "end":
            break
        else:
            candy.reset_filter()
