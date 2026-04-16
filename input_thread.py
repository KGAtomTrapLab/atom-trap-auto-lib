import threading
import queue
from devices import Ramp_Controller
from font_colors import color_yellow

class InputThread():
    def __init__(self):
        self.cmd_queue = queue.Queue()

    def input_thread(self):
        while True:
            cmd = input()
            self.cmd_queue.put(cmd)

    def check_queue(self):
        while not self.cmd_queue.empty():
            cmd = self.cmd_queue.get()
            print("Command", cmd)

    def start(self):
        threading.Thread(target=self.input_thread, daemon=True).start()

class RampCMDHandler(InputThread):
    def __init__(self, ramp: Ramp_Controller):
        super().__init__()
        self.ramp = ramp

    def check_queue(self):
        while not self.cmd_queue.empty():
            cmd = self.cmd_queue.get()
            # Handle command
            self.handle_ramp_cmd(cmd)
    
    def handle_ramp_cmd(self, cmd: str):
        '''
        Takes in the command and parses it
        
        :param cmd: The command string
        '''
        cmds_list = ["period", "pot", "status", "help"]
        split_cmd = cmd.split()
        entered_command = split_cmd[0]
        if entered_command not in cmds_list:
            print("Please enter a valid command")
            return
        if entered_command == "period" and self.check_cmd(split_cmd, 1):
            self.ramp.set_period(int(split_cmd[1]))
            return
        if entered_command == "pot" and self.check_cmd(split_cmd, 1):
            self.ramp.set_wiper(int(split_cmd[1]))
            return
        if entered_command == "status" and self.check_cmd(split_cmd, 0):
            result = self.ramp.get_status()
            print(f"Current period (ms): {color_yellow(result[0])}")
            print(f"Current Potentiometer Value: {color_yellow(result[1])}")
            return
        if entered_command == "help" and self.check_cmd(split_cmd, 0):
            print("Available Commands: ")
            print("period [value] - Enter the period in ms")
            print("pot [value] - Enter a value for the wiper between 0 and 128")
            print("status - Get the status of the ramp")
            return
        return

    def check_cmd(self, split_cmd, num_args):
        if (len(split_cmd)-1) != num_args:
            print(f"Please enter {num_args} argument")
            return False
        return True

