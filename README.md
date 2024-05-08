# QC Atom Trap Lab Automation Library
Python based Hardware Abstraction Layer for interfacing with Lab Equipment


# PyVisa Setup on Windows

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
pip install -r requirements.txt
```


- Python 3.8+
- Visa Backend
   - NI - VISA
   - PyVisa-Py
- USB → GPIB Driver
   - Keysight Connection Expert
