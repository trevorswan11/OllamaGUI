import os
print(os.getcwd())
print(os.path.expanduser("~"))
import sys

exe_directory = os.path.dirname(sys.executable)
print(exe_directory)