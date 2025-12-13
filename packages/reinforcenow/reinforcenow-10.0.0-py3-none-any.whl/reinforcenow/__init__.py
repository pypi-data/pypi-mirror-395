import warnings

warnings.warn(
    "\n\n"
    "========================================\n"
    "  The 'reinforcenow' package has been\n"
    "  renamed to 'rnow'.\n"
    "\n"
    "  Please install 'rnow' instead:\n"
    "    pip uninstall reinforcenow\n"
    "    pip install rnow\n"
    "========================================\n",
    DeprecationWarning,
    stacklevel=2
)

def main():
    print("""
========================================
  The 'reinforcenow' package has been
  renamed to 'rnow'.

  Please run:
    pip uninstall reinforcenow
    pip install rnow

  Then use 'rnow' commands instead.
========================================
""")

if __name__ == "__main__":
    main()
