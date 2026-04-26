import matplotlib.pyplot as plt

# TODO: Comment on this for an explanation

class Data_Graph():
    def __init__(self):
        self.data = [5,6,7]
        self.fig = None
        self.ax = None
        self.line1 = None
        self.line2 = None

    def create_graph(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(-2048, 2048)
        self.line1, = self.ax.plot(self.data)
        self.line2, = self.ax.plot(self.data)
        plt.show()

    def update_graph(self, new_data):
        if self.line1 is None:
            return
        self.data = new_data
        self.line1.set_xdata(range(len(new_data[0])))
        self.line1.set_ydata(new_data[0])
        self.line2.set_xdata(range(len(new_data[1])))
        self.line2.set_ydata(new_data[1])
        self.ax.relim()
        self.ax.autoscale_view(scaley=False)
        self.fig.canvas.draw_idle()  # thread-safe redraw request