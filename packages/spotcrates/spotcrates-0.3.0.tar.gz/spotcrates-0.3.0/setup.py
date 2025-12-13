# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotcrates']

package_data = \
{'': ['*'], 'spotcrates': ['templates/*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'flask-session>=0.4.0,<0.5.0',
 'flask>=2.2.2,<3.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'pygtrie>=2.5.0,<3.0.0',
 'spotipy>=2.22.0,<3.0.0',
 'types-appdirs>=1.4.3.1,<2.0.0.0']

entry_points = \
{'console_scripts': ['spotcrates = spotcrates.cli:main']}

setup_kwargs = {
    'name': 'spotcrates',
    'version': '0.3.0',
    'description': '',
    'long_description': '# Spotcrates\n### A set of tools for finding and managing music on Spotify\n\n![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cmayes/3c8214e2bd942821496440b93acd3582/raw/covbadge.json)\n\n# Installation\n\n(TODO: Add detailed instructions once uploaded to PyPI)\n\n# Commands\n\nThe installation script puts the command `spotcrates` in your Python environment\n(e.g. `/.pyenv/shims/spotcrates`). The command `spotcrates commands` lists all of the \ncommands available along with a short description of each.\n\n## daily\n`spotcrates daily` collects the contents of the "Daily Mix" playlists, filters them \nagainst an exclusion list ("Overplayed" by default), and adds them to the end of \na target list ("Now" by default).\n\n## list-playlists\n`spotcrates list-playlists` lists playlists\' name, owner, track count, and description.\nThe command accepts `-f` for filter expressions and `-s` for sort expressions. (TODO: \nadd description of filter and search expressions and link to it here)',
    'author': 'Chris Mayes',
    'author_email': 'cmayes@cmay.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
