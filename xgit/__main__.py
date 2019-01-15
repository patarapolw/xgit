import sys
import subprocess
import shlex
from pathlib import Path
import requests

from .utils import trim_indent, call_multiline

def main():
    argv = sys.argv

    if len(argv) <= 1:
        cli_default()
    elif argv[1] == "init":
        cli_init()
    elif argv[1] in {"commit", "cpush"}:
        try:
            cli_commit(argv[2])
        except IndexError:
            cli_commit(input("Please input your commit message: "))
        if argv[1] == "cpush":
            cli_push()

    elif argv[1] == "gi":
        cli_gi()
    elif argv[1] == "push":
        cli_push()
    elif argv[1] in {"-h", "--help", "help"}:
        print(trim_indent("""
        Acceptable commands:
        xgit init           Initialize new git along with .gitignore
        xgit commit message Commit to git with the following message
        xgit cpush message  Commit and push to git with the following message
        xgit gi             Generate gitignore from files in the directory
        xgit push           Push changes to origin
        xgit                Prompt for choices
        """))

def cli_default():
    choice = input(trim_indent("""
    What do you want to do?
    1. Initialize Git
    2. Commit current changes
    3. Commit current changes and push to remote
    4. Generate and commit .gitignore
    5. Push to remote
    Please select [1-5]: 
    """))

    if choice == "1":
        cli_init()
    elif choice in {"2", "3"}:
        cli_commit(input("Please input your commit message: "))
        if choice == "3":
            cli_push()
    elif choice == "4":
        cli_gi()
    elif choice == "5":
        cli_push()

def cli_init():
    cli_gi(_commit=False)
    subprocess.call(["git", "init"])

def cli_commit(s: str):
    call_multiline("""
    git add .
    git commit -m {}
    """.format(shlex.quote(s)))

def cli_gi(_commit=True):
    old_gitignore_rows = Path(".gitignore").read_text().split("\n")

    with open(".gitignore", "w+") as f:
        f.write(Path(__file__).parent.joinpath("gitignore/{}.gitignore".format("global")).read_text())

        matched = set()
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
        
        f.seek(0)
        new_gitignore_rows = f.read().strip().split()
        for row in old_gitignore_rows:
            if row not in new_gitignore_rows:
                f.write(row + "\n")
    
    if _commit:
        subprocess.call(["sh", "-c", "git ls-files -i --exclude-from=.gitignore | xargs git rm --cached"])
        cli_commit(input("Please input your commit message."))

def cli_push():
    if not subprocess.check_output(["git", "config", "remote.origin.url"]):
        subprocess.call(["git", "remote", "add", "origin", shlex.quote(input("Please input the Git origin: "))])

    subprocess.call(["git", "push", "origin", "master"])
