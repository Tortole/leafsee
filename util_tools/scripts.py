"""
Project scripts for run through Poetry
"""
import argparse
import subprocess
from pathlib import Path


def full_migrate():
    subprocess.run(
        ["poetry", "run", "python", "manage.py", "makemigrations"], check=False
    )
    subprocess.run(["poetry", "run", "python", "manage.py", "migrate"], check=False)


def init():
    # Catch prod argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--prod", dest="prod", action="store_true", default=False)
    args = parser.parse_args()

    # Actions in product and development project
    full_migrate()

    if args.prod:
        # Actions in product project
        pass
    else:
        # Actions in development project
        subprocess.run(["poetry", "run", "pre-commit", "install"], check=False)


def runserver():
    subprocess.run(["poetry", "run", "python", "manage.py", "runserver"], check=False)


def flake8():
    subprocess.run(["poetry", "run", "flake8", "."], check=False)


def black():
    subprocess.run(["poetry", "run", "black", "."], check=False)
    flake8()


def tailwind():
    # Transmits argument --watch if it was transmitted
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", dest="watch", action="store_true", default=False)
    args = parser.parse_args()

    subprocess.run(
        (
            "npx tailwindcss"
            + f" -i {Path('static/base/css/input.css')}"
            + f" -o {Path('static/base/css/out.css')}"
            + (" --watch" if args.watch else "")
        ),
        shell=True,
        check=False,
    )
