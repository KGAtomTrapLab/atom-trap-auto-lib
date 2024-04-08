import cmd
from LaserController import LaserController

class LabControlCLI(cmd.Cmd):
    intro = 'Welcome to the lab control CLI. Type help or ? to list commands.\n'
    prompt = '|QC-atom-lab|> '

    def __init(self):
        super().__init__()
        self.connected_instrements = {}

    def do_set_current(self, arg):
        'Set the current of the laser: set_current <current>'
        # laser_controller = LaserController()
        # laser_controller.set_current(float(arg))
        print("doing something")

    # def do_get_current(self, arg):
    #     'Get the current of the laser: get_current'
    #     laser_controller = LaserController()
    #     print(laser_controller.get_current())

    def do_exit(self, arg):
        'Exit the CLI'
        return True

if __name__ == '__main__':
    LabControlCLI().cmdloop()

