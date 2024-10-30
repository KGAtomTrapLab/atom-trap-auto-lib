# QC Atom Trap Lab Automation Library
Python based Hardware Abstraction Library for interfacing with Lab Equipment and custom devices


# PyVisa Setup on Windows

PyVisa requires a backend VISA manager / library to perform VISA commands. By default this limits the library to be run on a windows machine and for the the NI VISA library and to be configured correctly.

Keysight connection expert provides a Windows driver for our GPIB -> USB adapters necessary to communicate with our laser controller.

PyVisa offers a pure python based backend that has not been extensivly tested with this library but may prove effective going forward.


*~todo*

## Dependencies

This project was designed to use a virtual environment to manage dependencies.
First, ensure the latest python is installed on your system.

To install the dependencies, you can use the following commands:

**Create a virtual environment**
```
python -m venv lab_python_env
```
**Activate the virtual environment**

This can differ depending on OS and terminal / shell.

The following command will work for a Windows OS and Powershell terminal:

```
source lab_python_env/bin/Activate.ps1
```
**Install the dependencies**
```
pip install -r dependencies.txt
```

**Update Dependencies file**
Warning, running this command will overwrite the current dependencies file with EVERY python package found in the current running python enviornment. Make sure the correct virtual enviornment is setup before updating.
```
pip freeeze > dependencies.txt
```



- Python 3.8+
- Visa Backend
   - NI - VISA
   - PyVisa-Py
- USB → GPIB Driver
   - Keysight Connection Expert
