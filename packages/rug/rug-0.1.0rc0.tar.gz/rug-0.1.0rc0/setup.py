# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rug']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'rug',
    'version': '0.1.0rc0',
    'description': 'Library for fetching various stock data from the internet (official and unofficial APIs).',
    'long_description': '# Rug\n\n* [PyPI](https://pypi.org/project/rug/)\n* [documentation](https://rug.readthedocs.io/en/latest/)\n',
    'author': 'Pavel Hrdina, Patrick Roach',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/im-n1/rug',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
