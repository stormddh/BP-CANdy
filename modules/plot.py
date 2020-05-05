import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
mplstyle.use('fast')

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

        fig, ax = plt.subplots()
        lines = []

        for i in range(len(plot_data["data"][0])):
            lines.extend(ax.plot(plot_data["time"], [row[i] for row in plot_data["data"]], label=i))

        ax.set_title(f"Message { hex(msg_id) }")
        ax.minorticks_off()
        leg = ax.legend()
        leg.get_frame().set_alpha(0.8)
        ax.set_xlabel("time")
        ax.set_ylabel("data")

        # Source https://matplotlib.org/examples/event_handling/legend_picking.html
        # we will set up a dict mapping legend line to orig line, and enable
        # picking on the legend line
        lined = dict()
        for legline, origline in zip(leg.get_lines(), lines):
            legline.set_picker(5)  # 5 pts tolerance
            lined[legline] = origline

        def onpick(event):
            # on the pick event, find the orig line corresponding to the
            # legend proxy line, and toggle the visibility
            legline = event.artist
            origline = lined[legline]
            vis = not origline.get_visible()
            origline.set_visible(vis)
            # Change the alpha on the line in the legend so we can see what lines
            # have been toggled
            if vis:
                legline.set_alpha(1.0)
            else:
                legline.set_alpha(0.2)
            fig.canvas.draw()

        fig.canvas.mpl_connect('pick_event', onpick)
        plt.show()

    else:
        print("Unknown message")
