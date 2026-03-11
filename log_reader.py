'''

Access previous laser runs to view data

'''
import plotly.graph_objects as go
import numpy as np

dataset = []

def load_log_data(filename):
    
    with open(filename) as log_file:
        file_line = log_file.readline()
        while file_line != "":
            # Switch case for various options
            if ("RAMP START" in file_line):
                line_components = file_line.split("[")
                first_set = line_components[1]
                numbers = first_set.split(",")
                current_numbers = []
                for value in numbers:
                    try:
                        current_numbers.append(float(value))
                    except:
                        print("bad number")
                dataset.append(current_numbers)
                second_set = line_components[2]
            file_line = log_file.readline()

def create_graph():
    # Create figure
    fig = go.Figure()

    # Add traces, one for each slider step
    for step in dataset:
        fig.add_trace(
            go.Scatter(
                visible=False,
                line=dict(color="#00CED1", width=6),
                name="value",
                x=np.arange(0, len(step), 1),
                y=step))

    # Make 10th trace visible
    fig.data[10].visible = True

    # Create and add slider
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                {"title": "Slider switched to step: " + str(i)}],  # layout attribute
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=10,
        currentvalue={"prefix": "Frequency: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders,
    )

    fig.show()

load_log_data("logs/20260226-172143.log")
create_graph()