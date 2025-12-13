import re
import sys
from pathlib import Path

import toml
from packaging.version import parse

newversion = parse(sys.argv[1])
print("New version provided:", str(newversion))
project_meta = toml.load("pyproject.toml")  # assumes cwd is the project base
oldversion = set()
if len(sys.argv) > 2:
    oldversion.add(str(parse(sys.argv[2])))
print(f"{oldversion=}")
if not len(oldversion):
    print("Looking for previous version in:")
    for entry in project_meta["tool"]["semantic_release"].get("version_variables", []):
        fpath, varname = entry.split(":", maxsplit=1)
        print("    ", f"'{fpath}', '{varname}'")
        text = Path(fpath).read_text()
        match = re.search(f"{varname}" r"\s*=\s*([^\s]+)", text)
        oldversion.add(match[1].strip('"').strip("'") if match and len(match.groups()) else "")
    assert len(oldversion) == 1, "None or more than one previous version number found!"
oldversion = tuple(oldversion)[0]
print("Using previous version:", oldversion)
print("Replacing previous version in:")
for fpath in {
    entry.split(":", maxsplit=1)[0]
    for entry in project_meta["tool"]["semantic_release"].get("version_patterns", [])
}:
    path = Path(fpath)
    print(f"    '{path}' -> ", end="")
    text = path.read_text()
    if text.find(oldversion) < 0:
        print("Not found!")
        continue
    text = text.replace(oldversion, str(newversion))
    path.write_text(text)
    print("Done.")
print("Done replacing version numbers.")
