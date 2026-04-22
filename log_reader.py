import matplotlib.pyplot as plt
import numpy as np

from load_log_data import load_log_data

from matplotlib.widgets import Button, Slider


# The parametrized function to be plotted
def f(t, therm_val, current_val, channel = 0):
    return file_values[float(current_val)][float(therm_val)][0][channel]

# t = 

def make_3d(current_values, therm_value):
    # Build the Z grid by collecting all results
    Z = []
    for current_value in current_values:
        result = f(0, therm_value, current_value, 0)
        Z.append(result)

    Z = np.array(Z)  # shape: (len(current_values), len(result))

    # Build X and Y grids
    y_points = np.linspace(0, len(Z[0]), len(Z[0]))
    X, Y = np.meshgrid(current_values, y_points)

    return X, Y, Z

# Grab the dictionary
file_values, current_values, thermistor_values = load_log_data("logs/20260421-183026.log")

# print(len(file_values[80.0][13050.0]))

# Define initial parameters
init_therm = thermistor_values[2]
init_current = current_values[2]

# Create the figure and the line that we will manipulate
# fig, ax = plt.subplots()
fig = plt.figure()
ax = plt.axes(projection='3d')
i = 0

# for current_value in current_values:
#     result = f(0, init_amplitude, current_value, 0)
#     chnl1, = ax.plot3D(i, np.linspace(0, len(result), len(result)), result, lw=2)
    
#     i += 1


X, Y, Z = make_3d(current_values, init_therm)

# Plot the surface (note the transpose)
ax.plot_surface(X, Y, Z.T, cmap='viridis')




# chnl2, = ax.plot(f(0, init_amplitude, init_frequency, 1), lw=2)
ax.set_xlabel('Current [mA]')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='Current',
    valmin=min(current_values),
    valmax=max(current_values),
    valinit=init_current,
    valstep=current_values,
)

# Make a vertically oriented slider to control the amplitude
axamp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
amp_slider = Slider(
    ax=axamp,
    label="Resistance",
    valmin=min(thermistor_values),
    valmax=max(thermistor_values),
    valinit=init_therm,
    valstep=thermistor_values,
    orientation="vertical"
)


# The function to be called anytime a slider's value changes
def update(val):
    chnl1values = f(0, amp_slider.val, freq_slider.val, 0)
    x = np.arange(len(chnl1values))
    chnl1.set_data(x, chnl1values)

    chnl2values = f(0, amp_slider.val, freq_slider.val, 1)
    x = np.arange(len(chnl2values))
    chnl2.set_data(x, chnl2values)

    X, Y, Z = make_3d(current_values, init_therm)

    # Plot the surface (note the transpose)
    ax.plot_surface(X, Y, Z.T, cmap='viridis')


    
    ax.relim()
    ax.set_xlim([0, len(chnl1values)])

    # print(list(range(0, len(values))))
    # line.set_xdata(list(range(0, len(values))))
    fig.canvas.draw_idle()

    

# register the update function with each slider
freq_slider.on_changed(update)
amp_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    freq_slider.reset()
    amp_slider.reset()
button.on_clicked(reset)

ax.set_ylim([0, 4096])

plt.show()