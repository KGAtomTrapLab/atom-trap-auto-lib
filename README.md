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
lab_python_env/bin/pip install -r dependencies.txt
```

**Update Dependencies file**
Warning, running this command will overwrite the current dependencies file with EVERY python package found in the current running python enviornment. Make sure the correct virtual enviornment is setup before updating.
```
lab_python_env/bin/pip freeeze > dependencies.txt
```

- Python 3.8+
- Visa Backend
   - NI - VISA
   - PyVisa-Py
- USB → GPIB Driver
   - Keysight Connection Expert
 
**If python modules can't be found when running**
Instead of messing with which path to use, run a virtual environment:
1. Make sure a virtual environment exists in the directory(should be called "lab_python_env" or something similar)
   - See "Activate the Virtual Environment" above.
2. Make sure VS Code knows which interpreter to use:
   - Open the command pallete(ctrl+shift+P)
   - Type "Python: Select Interpreter" and choose that option
   - At the bottom should be the venv for this environment. Choose that.
3. Activate the environment in the command line(optional)
   - On the command line, type in the command
```
source lab_python_env/bin/activate
```
   - Prompts on the command should now start with `(lab_python_env)`
4. Commands need to be run from the "virtual" python.
   - To run python commands, run
```
lab_python_env\bin\python
```
   - To install modules with pip, run
```
lab_python_env\bin\pip
```
