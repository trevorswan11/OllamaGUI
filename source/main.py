from window import launch
import sys, os

# Get the location of the executable
exe_full_path = sys.executable

# file of the executable
exe_file = os.path.basename(exe_full_path)

# directory of the executable
exe_directory = os.path.dirname(exe_full_path)

# Set the working directory to the location of the executable
os.chdir(exe_directory)

# create a logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

if __name__ == "__main__":
    launch(exe_location=exe_directory)