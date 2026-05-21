import matplotlib.pyplot as plt

# TODO: Comment on this for an explanation

class Data_Graph():
    def __init__(self):
        self.data = [5,6,7]
        self.fig = None
        self.ax = None
        self.line1 = None
        self.line2 = None

        # Status functions for displaying on the graph
        self.davll_status_function = None

    def create_graph(self, davll_status_function, laser_status_function):
        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(-1, 2048)
        self.line1, = self.ax.plot(self.data)
        self.line2, = self.ax.plot(self.data)

        self.davll_status_function = davll_status_function
        self.laser_status_function = laser_status_function

        # Ramp Controller Display
        self.ramp_text = self.fig.text(0.02, 0.98, self.davll_status_function(), ha='left', va='top')

        # Laser Controller Display
        self.laser_text = self.fig.text(0.98, 0.98, self.laser_status_function(), ha='right', va='top')

        plt.show()

    def update_graph(self, new_data):
        if self.line1 is None:
            return
        self.data = new_data
        self.line1.set_xdata(range(len(new_data[0])))
        self.line1.set_ydata(new_data[0])
        self.line2.set_xdata(range(len(new_data[1])))
        self.line2.set_ydata(new_data[1])

        # Update status
        self.ramp_text.set_text(self.davll_status_function())
        self.laser_text.set_text(self.laser_status_function())


        self.ax.relim()
        self.ax.autoscale_view(scaley=False)
        self.fig.canvas.draw_idle()  # thread-safe redraw request