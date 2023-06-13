import os
import subprocess


def shutdown_windows():
    subprocess.run(f'{os.getcwd()}\\utils\\shutdown.bat', shell=False)
