import os
import sys
import zipfile
import urllib.request
import subprocess
from pathlib import Path
import platform

# default Python version
DEFAULT_VERSION = '3.10.9'

# base directory for all portableenv files
APPDATA_DIR = Path(os.getenv('LOCALAPPDATA') if platform.system() == "Windows" else Path.home())
DOWNLOAD_DIR = APPDATA_DIR / 'portableenv'

# create the download directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_python_embed_url(version, arch=None):
    """Generate the URL for the embedded Python zip file."""
    if arch is None:
        arch = 'amd64' if platform.architecture()[0] == '64bit' else 'win32'

    # use python.org
    return f"https://www.python.org/ftp/python/{version}/python-{version}-embed-{arch}.zip"

def get_paths_for_version(version):
    """Generate the paths for a specific Python version."""
    zip_name = f"python_embedded_{version}.zip"
    zip_file = DOWNLOAD_DIR / zip_name
    extract_dir = DOWNLOAD_DIR / f"embedded_python_{version}"
    return zip_file, extract_dir

# check if the extracted file is there
def check_extracted(extract_dir):
    """Check if the embedded Python directory exists."""
    return extract_dir.exists() and (extract_dir / 'python.exe').exists()

# download the zip file if not already downloaded
def download_zip(url, zip_file):
    """Download the embedded Python zip file to the designated directory."""
    if not zip_file.exists():
        print(f"Downloading {zip_file.name} from {url}...")
        urllib.request.urlretrieve(url, zip_file)
        print("Download complete.")
    else:
        print(f"{zip_file.name} already exists in {zip_file.parent}. Skipping download.")

# extract the zip file to the specified directory
def extract_zip(zip_file, extract_to):
    """Extract the zip file to the target directory."""
    print(f"Extracting {zip_file} to {extract_to}...")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete.")

# delete the zip file after extraction
def cleanup(zip_file):
    """Delete the zip file after extraction."""
    if zip_file.exists():
        os.remove(zip_file)
        print(f"{zip_file.name} has been deleted.")

def fix_embedded_python(extract_dir, version):
    """Apply fixes to the embedded Python to make it work properly."""
    # check if the embedded Python has the necessary files
    major, minor = version.split('.')[:2]
    python_zip = extract_dir / f"python{major}{minor}.zip"

    if not python_zip.exists():
        print(f"Error: {python_zip.name} not found. The embedded Python distribution may be incomplete.")
        return False

    # check for DLLs
    python_dll = extract_dir / f"python{major}{minor}.dll"
    if not python_dll.exists():
        print(f"Error: {python_dll.name} not found. The embedded Python distribution may be incomplete.")
        return False

    # 1. Fix the python3X._pth file to enable site-packages
    pth_file = extract_dir / f"python{major}{minor}._pth"

    if pth_file.exists():
        print(f"Fixing {pth_file.name} to enable site-packages...")
        # read the current content
        with open(pth_file, 'r') as f:
            lines = f.readlines()

        # create a new content list
        new_lines = []
        site_packages_added = False
        import_site_added = False

        for line in lines:
            line = line.strip()
            # skip empty lines
            if not line:
                continue

            # handle the import site line
            if line == '#import site':
                new_lines.append('import site')
                import_site_added = True
            elif line == 'import site':
                new_lines.append(line)
                import_site_added = True
            # handle the Lib/site-packages line
            elif line == 'Lib/site-packages':
                new_lines.append(line)
                site_packages_added = True
            # add other lines as is
            else:
                new_lines.append(line)

        # add Lib/site-packages if not already there
        if not site_packages_added:
            new_lines.append('Lib/site-packages')

        # add import site if not already there
        if not import_site_added:
            new_lines.append('import site')

        # write the modified content back
        with open(pth_file, 'w') as f:
            f.write('\n'.join(new_lines))

    # 2. Create Lib/site-packages directory if it doesn't exist
    site_packages_dir = extract_dir / 'Lib' / 'site-packages'
    os.makedirs(site_packages_dir, exist_ok=True)

    # 3. Download and run get-pip.py
    get_pip_path = extract_dir / 'get-pip.py'
    if not get_pip_path.exists():
        print(f"Downloading get-pip.py...")
        try:
            urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip_path)
        except Exception as e:
            print(f"Error downloading get-pip.py: {e}")
            return False

    print(f"Installing pip in the embedded Python...")
    try:
        # run with more detailed output
        result = subprocess.run(
            [str(extract_dir / 'python.exe'), str(get_pip_path)],
            check=True,
            capture_output=True,
            text=True
        )
        print("Pip installation complete.")
        if result.stdout:
            print(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error installing pip: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

    # 4. Verify pip installation
    try:
        result = subprocess.run(
            [str(extract_dir / 'python.exe'), "-m", "pip", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Pip installation verified: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Warning: Pip installation verification failed: {e}")
        print(f"Error output: {e.stderr if hasattr(e, 'stderr') else 'No error output'}")
        return False

def setup_embedded_python_version(version):
    """Setup the embedded Python for the specified version."""
    # generate paths based on version
    zip_file, extract_dir = get_paths_for_version(version)

    if check_extracted(extract_dir):
        print(f"Embedded Python {version} already exists at {extract_dir}.")
        return extract_dir

    print(f"Embedded Python {version} not found. Attempting to download and extract.")

    try:
        url = get_python_embed_url(version)
        download_zip(url, zip_file)
        extract_zip(zip_file, extract_dir)
        success = fix_embedded_python(extract_dir, version)  # apply fixes after extraction
        cleanup(zip_file)

        if not success:
            print(f"Error: There were issues setting up Python {version}.")

            # if the directory exists but setup failed, remove it
            if extract_dir.exists():
                import shutil
                print(f"Removing incomplete Python {version} installation...")
                shutil.rmtree(extract_dir, ignore_errors=True)
            return None
    except Exception as e:
        print(f"Error downloading/extracting Python {version}: {e}")
        return None

    return extract_dir

def ensure_virtualenv_installed(python_path):
    """Ensure the 'virtualenv' package is installed in the given Python interpreter."""
    try:
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "virtualenv"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Virtualenv installation complete.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing virtualenv: {e}")
        print(f"Error output: {e.stderr if hasattr(e, 'stderr') else 'No error output'}")
        return False

def create_env(env_name, version=DEFAULT_VERSION):
    """Create a virtual environment using the specified embedded Python version."""
    # setup the embedded Python for the specified version
    extract_dir = setup_embedded_python_version(version)

    # if setup failed completely
    if extract_dir is None:
        print(f"Failed to set up Python {version}. Falling back to system Python.")
        python_exe = Path(sys.executable)
    else:
        python_exe = extract_dir / 'python.exe'

        if python_exe.exists():
            print(f"Embedded Python {version} found at: {python_exe}")
        else:
            # fallback to system Python if embedded Python is not found
            print(f"Embedded Python {version} executable not found. Using the current Python interpreter.")
            python_exe = Path(sys.executable)

    if os.path.exists(env_name):
        print(f"Virtual environment '{env_name}' already exists.")
        return

    # ensure virtualenv is installed
    if not ensure_virtualenv_installed(python_exe):
        print("Failed to install virtualenv. This might be due to issues with the embedded Python.")
        print("Falling back to system Python...")
        python_exe = Path(sys.executable)

        # try again with system Python
        if not ensure_virtualenv_installed(python_exe):
            print("Failed to install virtualenv with system Python as well. Aborting.")
            return

    # create the virtual environment
    print(f"Creating virtual environment '{env_name}' using {python_exe}...")
    try:
        subprocess.run([str(python_exe), "-m", "virtualenv", env_name], check=True)
        print(f"Virtual environment '{env_name}' created successfully.")

        # update pip in the virtual environment
        print("Updating pip in the virtual environment...")

        # determine the path to the Python executable in the virtual environment
        if platform.system() == "Windows":
            python_venv_path = Path(env_name) / "Scripts" / "python.exe"
        else:
            python_venv_path = Path(env_name) / "bin" / "python"

        if python_venv_path.exists():
            try:
                # use the Python executable from the virtual environment to update pip
                update_result = subprocess.run(
                    [str(python_venv_path), "-m", "pip", "install", "--upgrade", "pip"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("Pip in virtual environment updated successfully.")
                if update_result.stdout and "Successfully installed pip" in update_result.stdout:
                    print(f"Pip updated to the latest version.")
            except subprocess.CalledProcessError as pip_error:
                print(f"Warning: Failed to update pip in the virtual environment: {pip_error}")
                if hasattr(pip_error, 'stderr') and pip_error.stderr:
                    print(f"Error output: {pip_error.stderr}")
        else:
            print(f"Warning: Could not find Python executable at {python_venv_path} to update pip.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create virtual environment '{env_name}': {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error output: {e.stderr}")
