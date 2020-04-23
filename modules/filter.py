import lib.api as candyAPI
import time

# Filter module - run with verbose
def run(candy):
    # CAN ID filter - using hexadecimal values
    # http://www.cse.dmu.ac.uk/~eg/tele/CanbusIDandMask.html

    # print only messages with ID 10 (HEX)
    candy.set_filter_rule(0x10,0xFF)
    while True:
        user = input("end or reset? ")
        if user == "end":
            break
        else:
            candy.reset_filter()
