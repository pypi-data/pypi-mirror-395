import subprocess
from .env_manager import (
    create_env,
    setup_embedded_python_version,
    DEFAULT_VERSION
)

def setup_embedded_python():
    """Setup the embedded Python by downloading and extracting it if necessary."""
    # for backward compatibility, use the default version
    setup_embedded_python_version(DEFAULT_VERSION)

def ensure_virtualenv_installed(python_path):
    """Ensure the 'virtualenv' package is installed in the given Python interpreter."""
    try:
        subprocess.run([str(python_path), "-m", "virtualenv", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"Installing 'virtualenv' in embedded Python at {python_path}...")
        subprocess.run([str(python_path), "-m", "pip", "install", "virtualenv"], check=True)

def create_virtualenv(venv_name):
    """Create a virtual environment using the predefined embedded Python interpreter path."""
    # for backward compatibility, use the default version
    create_env(venv_name, DEFAULT_VERSION)
