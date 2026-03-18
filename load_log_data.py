import json

def load_log_data(logfile_name):
    '''
        Load the data from a log. Accesses the set current and thermistor values and
        creates a dictionary where the key is these values. Multiple samples taken
        means an array at these points
    '''
    # Dictionary of thermistor logs where the key is the set current
    current_dictionary = {}
    # Load the file
    current_dictionary[0] = {}
    current_dictionary[0][0] = []

    # Return the thermistor values for graphing
    thermistor_values = []
    current_values = []

    with open(logfile_name, "r") as file:
        current_line = file.readline()
        # Temporarily store the recorded values as you go through each line
        recorded_values = [0,0]
        while current_line != "":
            # If the settings are in the line, assume that these are the settings for the run
            if "Target Current" in current_line:
                # This text extraction is pretty hacky. This could probably be prevented
                # by storing the data within some kind of structure like a .npy or a .pkl file
                

                # Extract the target current from the line
                filtered_line = current_line.split("Target Current: ")
                target_current = float(filtered_line[1])
                # Extract the target resistance from the line
                filtered_line = current_line.split("Target Resistance: ")[1].split()
                target_resistance = float(filtered_line[0])

                recorded_values = [target_current, target_resistance]
                if target_resistance not in thermistor_values:
                    thermistor_values.append(target_resistance)

                if target_current not in current_values:
                    current_values.append(target_current)
                
                if target_current not in current_dictionary:
                    current_dictionary[target_current] = {}
                if target_resistance not in current_dictionary[target_current]:
                    current_dictionary[target_current][target_resistance] = []

            # Grab the data from the line
            if "RAMP START" in current_line:
                filtered_line = current_line.split(",")
                filtered_line = filtered_line[0].split()
                ramp_start = filtered_line[-1]

                filtered_line = current_line.split("DAVLL: ")[1]
                # print(filtered_line)

                # Create an array for the first and second line
                data_lines = []
                # Iterate through each found array
                for data_array in filtered_line[:-2].split("],["):
                    davll_line = []
                    for value in data_array.strip("[]").split(","):
                        if value != '':
                            davll_line.append(float(value))
                    # Append to array
                    data_lines.append(davll_line)
                
                # Append to dictionary. So the dictionary has the 1st and second polarized channel
                current_dictionary[recorded_values[0]][recorded_values[1]].append(data_lines)

            current_line = file.readline()

    return current_dictionary, current_values, thermistor_values
        
   

    # Read each line, determining the type of data stored

    # 

if __name__ == "__main__":
    load_log_data("logs/20260226-172143.log")