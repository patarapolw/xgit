# xgit

An opinionated command line tools to make your life easier with Git and Gitignore

## Installation

Install as global from pip.

```
pip3 install xgit
```

Or clone the repo, and install from the clone (and you may also edit as you wish).

```
git clone https://github.com/patarapolw/xgit.git
pip3 install -e xgit
```

## Usage

```
$ xgit -h
Acceptable commands:
xgit init           Initialize new git along with .gitignore
xgit commit message Commit to git with the following message
xgit cpush message  Commit and push to git with the following message
xgit gi             Generate gitignore from files in the directory
xgit push           Push changes to origin
xgit                Prompt for choices
```

```
$ xgit
What do you want to do?
1. Initialize Git
2. Commit current changes
3. Commit current changes and push to remote
4. Generate and commit .gitignore
5. Push to remote
Please select [1-5]:
```

## Note

- `.gitignore` is generated from <https://www.gitignore.io/>, but this project also allows me to generate a custom `.gitignore` based on [/xgit/gitignore/](/xgit/gitignore/).
- To learn more about my experience with Git, see <https://github.com/patarapolw/SimpleGit>
