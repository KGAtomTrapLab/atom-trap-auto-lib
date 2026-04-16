from LaserControlCalibrator import LaserControlCalibrator
from digital_davll.digital_davll import Digital_DAVLL
from log_data import DataLogger
from LabControlCLI import LabControlCLI

if __name__ == "__main__":
    # data_logger = DataLogger("./logs")
    # control_calibrator = LaserControlCalibrator()
    # control_calibrator.connect_laser_controller()
    # digital_davll = Digital_DAVLL(data_logger)
    # digital_davll.connect()

    # control_calibrator.gather_data(12950, 14500, 100, 80, 120, 1, digital_davll, data_logger)
    # while True:
    #     print(digital_davll.get_data_line())
    # control_calibrator.gather_data(0, 100, 1, 80, 120, 1)
    LabControlCLI().cmdloop()
