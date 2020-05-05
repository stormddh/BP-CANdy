import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style as mplstyle
mplstyle.use('fast')

import lib.api as candyAPI

# Example plot module
def run(candy):
    user_input = input("Message ID: ")
    msg_id = int(user_input, 16)
    if msg_id and msg_id in candy.get_messages():
        idx = input("Signal field(0-7): ")
        # Create figure for plotting
        fig, ax = plt.subplots()
        xs = []
        ys = []

        def init():
            ax.tick_params(axis='x', which='both', length=0, labelbottom=False, labeltop=False, labelleft=False, labelright=False)

        # This function is called periodically from FuncAnimation
        def animate(i, xs, ys):
            # Read last 500 messages
            # This could be faster
            history = candy.get_message_log(msg_id, last=500)
            count = candy.get_messages(msg_id)['count']

            xs.clear()
            ys.clear()

            for m in history:
                xs.append(m.timestamp)
                ys.append(m.data[int(idx)])

            ax.clear()
            ax.plot(xs, ys)

            # Format plot
            ax.set_title(f"Message { msg_id } ({ count })")
            ax.set_xlabel(f"{ xs[-1] }")
            ax.set_ylabel("data")

        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=200, init_func=init)
        plt.show()
