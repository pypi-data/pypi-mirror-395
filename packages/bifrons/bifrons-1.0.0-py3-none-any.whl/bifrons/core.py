import os

def normalize_version(v: str) -> str:
    v = v.strip()
    if v.startswith("v"):
        v = v[1:]
    parts = v.split(".")
    while len(parts) < 3:
        parts.append("0")
    try:
        major, minor, patch = map(int, parts[:3])
    except:
        major, minor, patch = 0, 0, 0
    return f"{major}.{minor}.{patch}"

def classify(title: str):
    title = (title or "").lower().strip()

    if title.startswith("fix"):
        return "patch"

    if title.startswith(("feat", "feature")):
        return "minor"

    if title.startswith(("breaking", "major")) or "breaking change" in title:
        return "major"

    raise ValueError("Título inválido! Use fix/feat/major")

def increment(version: str, level: str) -> str:
    major, minor, patch = map(int, version.split("."))

    if level == "patch":
        patch += 1
    elif level == "minor":
        minor += 1
        patch = 0
    elif level == "major":
        major += 1
        minor = 0
        patch = 0

    return f"{major}.{minor}.{patch}"

def read_version():
    if not os.path.exists("version.txt"):
        with open("version.txt", "w") as f:
            f.write("0.0.0")
        print("[bifrons] versão inicial criada: 0.0.0")
        return "0.0.0"

    with open("version.txt") as f:
        return f.read().strip()

def write_version(version: str):
    with open("version.txt", "w") as f:
        f.write(version)

def process(title: str):
    current = read_version()
    current = normalize_version(current)

    level = classify(title)
    newv = increment(current, level)

    write_version(newv)

    print(f"[bifrons] versão anterior: {current}")
    print(f"[bifrons] nova versão: {newv}")

    return newv
