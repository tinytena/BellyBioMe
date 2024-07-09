import os
import sys
from pathlib import Path

# Determine the base directory (assuming this script is run from the project root)
BASE_DIR = Path(__file__).resolve().parent

# Determine the config directory
config_dir = BASE_DIR / "config"

# Determine the wsgi.py file path
wsgi_file = config_dir / "wsgi.py"

# Check if the paths exist
print(f"Base Directory: {BASE_DIR}")
print(f"Config Directory: {config_dir} - Exists: {config_dir.exists()}")
print(f"WSGI File: {wsgi_file} - Exists: {wsgi_file.exists()}")

# Check if the application callable is defined in wsgi.py
if wsgi_file.exists():
    with open(wsgi_file) as file:
        content = file.read()
        if "application = get_wsgi_application()" in content:
            print("WSGI application callable is correctly defined.")
        else:
            print("WSGI application callable is missing or incorrectly defined.")
else:
    print("WSGI file does not exist.")

# Check the DJANGO_SETTINGS_MODULE environment variable
django_settings_module = os.getenv("DJANGO_SETTINGS_MODULE")
print(f"DJANGO_SETTINGS_MODULE: {django_settings_module}")

# Check the Python path
print("Python Path:")
for path in sys.path:
    print(path)

# Try importing the application
try:
    print("WSGI application imported successfully.")
except Exception as e:
    print(f"WSGI application import error: {e}")
