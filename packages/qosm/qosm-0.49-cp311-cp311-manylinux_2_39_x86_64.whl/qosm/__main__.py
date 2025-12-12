import subprocess
import sys

if __name__ == "__main__":
    from qosm.gui.gui import gui

    if len(sys.argv) == 2:
        if 'detached' in sys.argv[1]:
            gui(sys.argv)
    else:
        subprocess.Popen([sys.executable, '-m', 'qosm', 'detached'])
        exit(0)