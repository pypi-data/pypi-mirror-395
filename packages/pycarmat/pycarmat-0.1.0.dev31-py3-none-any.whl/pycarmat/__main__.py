import subprocess
import sys

from pycarmat.gui import main

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if 'detached' in sys.argv[1]:
            main()
        else:
            app = sys.argv[1]
            subprocess.Popen([sys.executable, '-m', f'pycarmat.GUI.{app}', 'detached'])
    else:
        subprocess.Popen([sys.executable, '-m', 'pycarmat', 'detached'])
        exit(0)
