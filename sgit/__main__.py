import sys
import subprocess
import json
from pathlib import Path
import requests

from .utils import trim_indent, call_multiline

def main():
    argv = sys.argv

    if len(argv) <= 1:
        cli_default()
    elif argv[1] == "init":
        cli_init()
    elif argv[1] == "commit":
        try:
            cli_commit(argv[2])
        except IndexError:
            cli_commit(input("Please input your commit message."))
    elif argv[2] == "gi":
        cli_gi()

def cli_default():
    choice = input(trim_indent("""
    What do you want to do?
    1. Initialize Git
    2. Commit your current changes
    3. Generate and commit .gitignore
    4. Push to remote
    Please select [1-4]:
    """))

    if choice == "1":
        cli_init()
    elif choice == "2":
        cli_commit(input("Please input your commit message."))
    elif choice == "3":
        cli_gi()
    elif choice == "4":
        cli_push()

def cli_init():
    cli_gi(_commit=False)
    subprocess.call(["git", "init"])

def cli_commit(s: str):
    call_multiline("""
    git add .
    git commit -m {}
    """.format(json.dumps(s)))

def cli_gi(_commit=True):
    with open(".gitignore", "a") as f:
        f.write("\n")

        matched = {"global"}
        for spec, filetypes in {
            "py": ["py"],
            "jvm": ["java", "kt"],
            "dart": ["dart"]
        }.items():
            for filetype in filetypes:
                try:
                    next(Path(".").glob("**/*.{}".format(filetype)))
                    if spec not in matched:
                        f.write(Path(__file__).parent.joinpath("gitignore/{}.gitignore".format(spec)).read_text())
                    matched.add(spec)
                    matched.add(filetype)
                except StopIteration:
                    pass
        
        if len(matched) > 0:
            r = requests.get("https://www.gitignore.io/api/{}".format(",".join({
                "kt": "kotlin",
                "py": "python"
            }.get(k, k) for k in matched)))
            f.write(r.text)
    
    if _commit:
        call_multiline("""git ls-files -i --exclude-from=.gitignore | xargs git rm --cached""")
        cli_commit(input("Please input your commit message."))

def cli_push():
    subprocess.call(["git", "push", "origin", "master"])
