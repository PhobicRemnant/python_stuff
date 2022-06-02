from debug import Debugger
from os import environ

file_path = environ['HOME'] + "/Videos/aoeo.mp4"

# Instantiate debugger with default port and host
debugger = Debugger()
# Set dubugger as server
debugger.viewer()
