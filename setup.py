# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sgit']

package_data = \
{'': ['*'], 'sgit': ['gitignore/*']}

install_requires = \
['requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['sgit = sgit.__main__:main']}

setup_kwargs = {
    'name': 'sgit',
    'version': '0.1.0',
    'description': 'An opinionated command line tools to make your life easier with Git and Gitignore',
    'long_description': '# sgit\n\n```\n$ sgit -h\nAcceptable commands:\nsgit init           Initialize new git along with .gitignore\nsgit commit message Commit to git with the following message\nsgit cpush message  Commit and push to git with the following message\nsgit gi             Generate gitignore from files in the directory\nsgit push           Push changes to origin\nsgit                Prompt for choices\n```\n\n```\n$ sgit\nWhat do you want to do?\n1. Initialize Git\n2. Commit your current changes\n3. Generate and commit .gitignore\n4. Push to remote\nPlease select [1-4]:\n```\n',
    'author': 'patarapolw',
    'author_email': 'patarapolw@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
