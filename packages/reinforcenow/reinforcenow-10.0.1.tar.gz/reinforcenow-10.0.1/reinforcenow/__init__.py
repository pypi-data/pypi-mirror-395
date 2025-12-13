import sys

def main():
    print("\033[91m" + """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   This package has been renamed to 'rnow'                  ║
║                                                            ║
║   Please run:                                              ║
║     pip uninstall reinforcenow                             ║
║     pip install rnow                                       ║
║                                                            ║
║   Then use 'rnow' instead of 'reinforcenow'                ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""" + "\033[0m")
    sys.exit(1)

if __name__ == "__main__":
    main()
