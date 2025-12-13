import argparse
from .core import process

def main():
    parser = argparse.ArgumentParser(description="Bifrons - SemVer CLI")
    parser.add_argument("--title", required=True, help="Título da PR/commit")
    args = parser.parse_args()

    try:
        process(args.title)
    except ValueError as e:
        print(f"Erro: {e}")
        return 1