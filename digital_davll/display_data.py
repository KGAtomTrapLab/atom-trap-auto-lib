import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys, time
import struct
from input_thread import RampCMDHandler

from devices import Ramp_Controller, PD_Reader

# Default xView - adapts with the number of samples
xView = 800

ADC_RESOLUTION = 4096
ADC_SUPPLY_VOLTAGE = 5

def process_data(ramp: Ramp_Controller, davll: PD_Reader, logger):
    global i
    '''
    The primary control loop for getting data from the DAVLL.

    This method waits for a peak signal from the ramp.
    Upon receiving the signal, it collects all data from the DAVLL waiting
    in the buffer and processes it. It then returns that data so it can be graphed.

    :param ramp: A Ramp_Controller object so the signal can be awaited
    :param davll: A DAVLL object to gather the data from

    '''
    # The array where each output from the DAVLL will be stored.
    output_data_lines = []
    # add each channel
    for channel in range(0, davll.channel_mode):
        output_data_lines.append([])
    # The index into output_data where the ramp changed directions from low to high
    valley_position = 0
    # Wait for peak signal, assigns the value to signal so it can be used for logic
    while (signal := ramp.check_for_peak_valley()) != 1:
        # Grab the latest signal from the davll. 
        data_points = davll.get_short()
        # Calibrate the voltage based on the ADC settings
        if len(data_points) == davll.channel_mode:

            for channel in range(0, davll.channel_mode):
                calibrated_data_point = (data_points[channel] / ADC_RESOLUTION) * ADC_SUPPLY_VOLTAGE
                output_data_lines[channel].append(calibrated_data_point)

            # If the signal is a 2(indicating valley), mark its position so it can be graphed
            if signal == 2:
                valley_position = len(output_data_lines[0]) - 1
    logger.write_dataline(output_data_lines, valley_position)
    # output_data.append(struct.unpack("<h", receivedNumber)[0])

    return output_data_lines[0], valley_position

def graph_data(ramp: Ramp_Controller, davll: PD_Reader, logger):

    fig, ax = plt.subplots()
    response_signal, = ax.plot([], [])   # a line object
    rampline, = ax.plot([0, 20], [-100, 2000])

    # Start up command parser
    cmd_parser = RampCMDHandler(ramp)
    cmd_parser.start()


    # Set the area of the graph. Could be done better
    ax.set(xlim=(0, xView), ylim=(-1 * ADC_SUPPLY_VOLTAGE, ADC_SUPPLY_VOLTAGE * 2))

    def update(frame):
        global xView
        ydata, valley_position = process_data(ramp, davll, logger)
        xdata = range(len(ydata))
        response_signal.set_data(xdata, ydata)

        # Ramp signal simulated points - start, valley, end
        ramp_x_data = [0, valley_position, len(ydata)]
        ramp_y_data = [ADC_SUPPLY_VOLTAGE, -1, ADC_SUPPLY_VOLTAGE]
        rampline.set_data(ramp_x_data, ramp_y_data)

        # Change the frame if drastic data difference
        if abs(len(ydata) - xView) > (len(ydata) / 10):
            xView = len(ydata)
            ax.set(xlim=(0, xView), ylim=(-1 * ADC_SUPPLY_VOLTAGE, ADC_SUPPLY_VOLTAGE * 2))

        cmd_parser.check_queue()
        return response_signal, rampline

    ani = animation.FuncAnimation(fig, update, frames=1000, interval=90, blit=True)
    plt.show()