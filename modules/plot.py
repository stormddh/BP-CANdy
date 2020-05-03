import sys
import matplotlib.pyplot as plt

import lib.api as candyAPI

# Example plot module
def run(candy):
    msg_id = input("Message ID: ")
    if msg_id and int(msg_id, 16) in candy.get_messages():
        # Collect data
        history = candy.get_message_log(int(msg_id, 16))

        plot_data = dict()
        plot_data["time"] = []
        plot_data["data"] = []

        for m in history:
            # SocketCAN candump log format
            plot_data["time"].append(m.timestamp)
            plot_data["data"].append(m.data)

        # Draw graph
        fig = plt.figure()

        for i in range(len(plot_data["data"][0])):
            plt.plot(plot_data["time"], [row[i] for row in plot_data["data"]], label=i)
        plt.minorticks_off()

        plt.title(f"Message { msg_id }")
        plt.xlabel("time")
        plt.ylabel("data")
        plt.legend()
        plt.show()

    else:
        print("Unknown message")
