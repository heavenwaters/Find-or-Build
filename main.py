import os
import sys
import subprocess
import pkg_resources

#Install Required Libraries
required = {"pillow", "tk", "pygame"}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    python = sys.executable
    subprocess.check_call(
        [python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

os.startfile("makecode.py")
