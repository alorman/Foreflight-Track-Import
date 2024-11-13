import os
import subprocess
import sys

def install_requirements():
    """
    Install the required packages from requirements.txt.
    """
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-deps', '-r', 'requirements.txt'])
        print("All required packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing packages: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("requirements.txt file not found. Please ensure it is present in the current directory.")
        sys.exit(1)

    # Install requirements
    install_requirements()
