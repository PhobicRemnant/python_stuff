from debug import Debugger
from os import environ

filepath = environ["HOME"] + "/Videos/aoeo.mp4"
# Instantiate a debugger with default port and host
debugger = Debugger()
# Set debugger as viewer
debugger.streamer(filepath, show=True)