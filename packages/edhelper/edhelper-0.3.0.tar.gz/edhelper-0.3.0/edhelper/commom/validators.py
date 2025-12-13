import os
import re


def validate_path(path, extension=None):
    if not os.path.exists(path):
        print(f"File {path} not found")
        return False
    if extension is not None:
        if not path.lower().endswith(extension.lower()):
            print(f"File {path} must have extension {extension}")
            return False
        if not os.access(path, os.R_OK):
            print(f"File {path} not readable")
            return False
        if not os.access(path, os.W_OK):
            print(f"File {path} not writable")
            return False
    else:
        if not os.path.isdir(path):
            print(f"File {path} must be a directory")
            return False
        if not os.access(path, os.R_OK):
            print(f"Directory {path} not readable")
            return False
        if not os.access(path, os.W_OK):
            print(f"Directory {path} not writable")
            return False
    return True


def validate_txt(path):
    with open(path, "r") as f:
        content = f.readlines()
        cards = []
        pattern = re.compile(r"^(\d+) (.+)$")
        errors = []
        for line in content:
            line = line.strip()
            if line.startswith("//"):
                continue
            if not line:
                continue
            match = pattern.match(line)
            if not match:
                errors.append(line)
                continue
            cards.append(match.groups())
        return cards, errors
