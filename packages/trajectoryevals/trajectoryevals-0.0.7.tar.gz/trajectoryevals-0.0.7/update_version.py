import re
import sys

if len(sys.argv) != 2:
    print("Usage: python update_version.py <new_version>")
    sys.exit(1)

new_version = sys.argv[1]
found = False

try:
    with open("pyproject.toml") as f:
        content = f.read()
except OSError as e:
    print(f"Error: Failed to read 'pyproject.toml': {e}")
    sys.exit(1)

# Use regex to find and replace the version line
# Pattern matches: version = "any.version.number"
pattern = r'^version\s*=\s*"[^"]*"'
replacement = f'version = "{new_version}"'

new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

if new_content == content:
    print("Warning: No version line found in pyproject.toml")
    sys.exit(1)

try:
    with open("pyproject.toml", "w") as f:
        f.write(new_content)
    print(f"Successfully updated version to {new_version}")
except OSError as e:
    print(f"Error: Failed to write to 'pyproject.toml': {e}")
    sys.exit(1)
