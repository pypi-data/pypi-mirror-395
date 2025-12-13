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
 'spotipy>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['spotcrates = spotcrates.cli:main']}

setup_kwargs = {
    'name': 'spotcrates',
    'version': '0.1.3',
    'description': '',
    'long_description': '# spotcrates\n\nTools for finding and sharing Spotify tracks.',
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
