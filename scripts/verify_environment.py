"""Confirm that the project's core Python packages can be imported."""

import importlib
import sys

PACKAGES = {
    "pandas": "pandas",
    "numpy": "numpy",
    "scikit-learn": "sklearn",
    "joblib": "joblib",
}

def main() -> None:
    """Import every required package and print its installed version."""
    print(f"Python {sys.version.split()[0]}")
    print("Checking core dependencies...")
    for display_name, import_name in PACKAGES.items():
        package = importlib.import_module(import_name)
        print(f"  OK  {display_name} {package.__version__}")
    print("All core dependencies are installed and import correctly.")

if __name__ == "__main__":
    main()
