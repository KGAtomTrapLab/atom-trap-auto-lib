# Example of using this library with a simple CMD 
from DataLogger import DataLogger
from DIgitalDavll import Digital_DAVLL
from LaserControlCalibrator import LaserControlCalibrator
from test_devices import Test_DAVLL, Test_LaserControlCalibrator
from logview import graph_log

import pathlib
import cmd2
from cmd2 import (
    Color,
    stylize,
)
from rich.style import Style
from laser_controller.LaserController import LaserController
import warnings

# Ignore the background thread warning
warnings.filterwarnings(
    "ignore",
    message="Starting a Matplotlib GUI outside of the main thread will likely fail."
)



class LabControlCLI(cmd2.Cmd):
    """Cmd2 application to demonstrate many common features."""

    def __init__(self) -> None:
        """Initialize the CLI."""
        # Startup script that defines a couple aliases for running shell commands
        alias_script = pathlib.Path(__file__).absolute().parent / '.cmd2rc'

        # Create a shortcut for one of our commands
        shortcuts = cmd2.DEFAULT_SHORTCUTS
        shortcuts.update({'&': 'intro'})
        super().__init__(
            include_ipy=True,
            multiline_commands=['echo'],
            persistent_history_file='cmd2_history.dat',
            shortcuts=shortcuts,
            startup_script=str(alias_script),
        )

        # Prints an intro banner once upon application startup
        self.intro = (
            stylize(
                'Welcome to the lab control CLI. Type help or ? to list commands.\n',
                style=Style(color=Color.GREEN1, bold=True),
            )
        )

        # Show this as the prompt when asking for input
        self.prompt = '|QC-atom-lab|> '

        # Used as prompt for multiline commands after the first line
        self.continuation_prompt = '... '

        # Allow access to your application in py and ipy via self
        self.self_in_py = True

        # Set the default category name
        self.default_category = 'General Commands'

        # Color to output text in with echo command
        self.foreground_color = Color.CYAN.value

        # Make echo_fg settable at runtime
        fg_colors = [c.value for c in Color]
        self.add_settable(
            cmd2.Settable(
                'foreground_color',
                str,
                'Foreground color to use with echo command',
                self,
                choices=fg_colors,
            )
        )
        # Collection Loop on or off
        self.collection_loop_running = False

    def preloop(self) -> None:
        # Initiate the log at the beginning of each run
        self.data_logger = DataLogger("./logs")
        print(f"Log created at {self.data_logger.filename}")

    
    RAMP_CATEGORY = "Ramp Commands"

    # INITIALIZATION METHODS
    connect_parser = cmd2.Cmd2ArgumentParser()
    connect_parser.add_argument("--port", type=str, default="COM4")
    connect_parser.add_argument("--baud", type=int, default=115200)
    connect_parser.add_argument('-t', '--test', action='store_true', help='Run in test mode(not connected to arduino)')

    # TODO: Add the ability to run this command multiple times without an error occuring
    @cmd2.with_argparser(connect_parser)
    def do_connect(self, args):
        """Connect to the ramp and laser controller"""
        # Create fake ramp if in test mode
        if args.test:
            print("Creating TEST mode.")
            self.davll = Test_DAVLL(self.data_logger, args.port, args.baud)
            self.davll.connect()

            self.control_calibrator = Test_LaserControlCalibrator()
            self.control_calibrator.connect_laser_controller()
            return
        self.davll = Digital_DAVLL(self.data_logger, args.port, args.baud)
        if self.davll.connect() < 0: self.perror("Ramp Error. Check log for more info.")

        try:
            self.control_calibrator = LaserControlCalibrator()
            self.control_calibrator.connect_laser_controller()
        except Exception as e:
            self.perror("Laser Controller Error.")
            self.perror(e)


    def do_graph(self, args):
        'View the live graph of data coming from the ramp'
        # self.davll.print = not self.davll.print
        self.davll.display_graph(self.control_calibrator.get_status)
        # print(self.davll.ramp_controller.print)


    def do_record(self, args):
        'Records all data from the ramp. Every ramp signal received is stored in the logfile.'
        result = self.davll.toggle_record()
        if result: print("Recording started")
        else: print("Recording stopped")

    # Ramp commands

    period_parser = cmd2.Cmd2ArgumentParser()
    period_parser.add_argument("time", type=int)

    @cmd2.with_argparser(period_parser)
    def do_period(self, args):
        'Set the period of the ramp (must be greater than 0)'
        self.davll.ramp_controller.set_period(args.time)
        print(f"Set period to {args.time}")
        

    pot_parser = cmd2.Cmd2ArgumentParser()
    pot_parser.add_argument("wiper", type=int)

    @cmd2.with_argparser(pot_parser)
    def do_pot(self, args):
        # TODO: Implement
        'Set the wiper position of the ramp  (0-127)'
        self.davll.ramp_controller.set_wiper(args.wiper)
        print(f"Set wiper to {args.wiper}")

    laser_parser = cmd2.Cmd2ArgumentParser()
    laser_parser.add_argument('state', choices=['on', 'off'], help='Turn laser on or off')

    @cmd2.with_argparser(laser_parser)
    def do_laser(self, args):
        'Toggle the laser'
        if args.state == "on":
            self.control_calibrator.laser_controller.laser_on()
            self.control_calibrator.laser_controller.tec_on()
        elif args.state == "off":
            self.control_calibrator.laser_controller.laser_off()
            self.control_calibrator.laser_controller.tec_off()
        else: self.perror("Provide a --pwr setting.")
    # TODO: Commands 


    def do_collect(self, args):
        'Collect data from the laser.'
        if self.collection_loop_running:
            self.perror("Collection loop already started. Stop the program and try again.")
            return
        try:
            response = self.read_input("Start collection loop. Are you sure? [y/n]")
        except EOFError:
            response = "n"
        if response !=  "y":
            return
        self.collection_loop_running = True
        print("Starting the collection loop...")
        self.control_calibrator.gather_data(13800, 14000, 200, 95, 125, 1, self.davll, self.data_logger)
        print("Collection loop finished.")


    file_parser = cmd2.Cmd2ArgumentParser()
    file_parser.add_argument('filepath')
    
    @cmd2.with_argparser(file_parser)
    def do_logview(self, args):
        'Load a log file into a graph for viewing'
        graph_log(args.filepath)
    
    complete_logview = cmd2.Cmd.path_complete
    # def do_set(self, args):
    #     'Set the current of the laser: set_current <current>'
    #     # laser_controller = LaserController()
    #     # laser_controller.set_current(float(arg))
    #     print("Not actually setting the current just printing")

    # def do_get(self, args):

    # def do_get_current(self, arg):
    #     'Get the current of the laser: get_current'
    #     laser_controller = LaserController()
    #     print(laser_controller.get_current())
    
    #Ramp control commands
    ramp_control_parser = cmd2.Cmd2ArgumentParser()
    ramp_control_parser.add_argument("--start", type=int)
    ramp_control_parser.add_argument("--end", type=int)
    @cmd2.with_argparser(ramp_control_parser)
    def do_ramp(self, args):
        if args.start != None:
            self.davll.ramp_controller.set_start(args.start)
            print("Set ramp start position to ", args.start)
        if args.end != None:
            self.davll.ramp_controller.set_end(args.end)
            print("Set ramp end position to ", args.end)

    # Set current and resistance
    value_parser = cmd2.Cmd2ArgumentParser()
    value_parser.add_argument("--set", type=float)
    value_parser.add_argument("--increase", type=float)
    value_parser.add_argument("--lower", type=float)

    @cmd2.with_argparser(value_parser)
    def do_current(self, args):
        if (args.set):
            print(f"Setting current to {args.set}...")
            self.control_calibrator.laser_controller.set_current(args.set)
            return
        if args.increase :
            print(f"Raising current by {args.increase}...")
            self.control_calibrator.laser_controller.raise_current(args.increase)
            return
        if args.lower :
            print(f"Lowering current by {args.lower}...")
            self.control_calibrator.laser_controller.lower_current(args.lower)
            return
        
    # Called "thm" and not "res" due to reducing confusion with pot command
    @cmd2.with_argparser(value_parser)
    def do_thm(self, args):
        'Sets the resistance of the temperature control.'
        if (args.set):
            print(f"Setting resistance to {args.set}...")
            self.control_calibrator.laser_controller.set_thm_res(args.set)
            return
        if args.increase :
            print(f"Raising resistance by {args.increase}...")
            self.control_calibrator.laser_controller.raise_thm_res(args.increase)
            return
        if args.lower :
            print(f"Lowering resistance by {args.lower}...")
            self.control_calibrator.laser_controller.lower_thm_res(args.lower)
            return

    
    
    def do_quit(self, arg):
        'Exit the CLI'
        self.data_logger.close_log()  # flushes buffer and closes file
        print("Log saved.")
        return True

if __name__ == '__main__':
    LabControlCLI().cmdloop()
 
