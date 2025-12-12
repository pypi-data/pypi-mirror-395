import os, sys

def run_driver():
    argv = [sys.executable, os.path.join(os.path.dirname(__file__), "..", "bin", "salome", "driver"), *sys.argv[1:]]
    if os.name == 'posix':
        os.execv(argv[0], argv)
    else:
        import subprocess; sys.exit(subprocess.call(argv))
