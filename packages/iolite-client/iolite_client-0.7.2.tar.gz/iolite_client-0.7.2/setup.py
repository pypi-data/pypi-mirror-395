# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iolite_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'requests', 'single-source>=0.2,<0.4', 'websockets']

setup_kwargs = {
    'name': 'iolite-client',
    'version': '0.7.2',
    'description': "API client for interacting with IOLite's remote API",
    'long_description': '# Python IOLite Client\n\n![CI](https://github.com/inverse/python-iolite-client/workflows/CI/badge.svg)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a38c5dbfc12247c893b4f39db4fac2b2)](https://www.codacy.com/manual/inverse/python-iolite-client?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=inverse/python-iolite-client&amp;utm_campaign=Badge_Grade)\n[![codecov](https://codecov.io/gh/inverse/python-iolite-client/branch/master/graph/badge.svg?token=26LC98A22C)](https://codecov.io/gh/inverse/python-iolite-client)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI version](https://badge.fury.io/py/iolite-client.svg)](https://badge.fury.io/py/iolite-client)\n![PyPI downloads](https://img.shields.io/pypi/dm/iolite-client?label=pypi%20downloads)\n[![License](https://img.shields.io/github/license/inverse/python-iolite-client.svg)](LICENSE)\n\n\nPython client for [IOLite\'s][0] remote API.\n\nThe client has basic functionality such as the authentication layer, some basic command models, and a client to change the\nheating intervals are available.\n\nBuild by reverse engineering the [Deutsche Wohnen][2] [MIA Android App][1] and subsequently their remote API.\n\nRead the following [short post][3] on how that was achieved.\n\nUsed in making the [IOLite Custom Component](https://github.com/inverse/home-assistant-iolite-component) for Home Assistant.\n\n## Requirements\n\n-   Python 3.7+\n-   [Poetry][4]\n\n## Getting credentials\n\nOpen your Deutsche Wohnen tablet and begin pairing device process. Scan the QR code with your QR-Scanner and instead of\nopening the QR code in your browser, copy it\'s content. You\'ll get the following payload:\n\n```json\n{\n  "webApp": "/ui/",\n  "code": "<redacted>",\n  "basicAuth": "<redacted>"\n}\n```\n\n-   `basicAuth` contains base64 encoded HTTP basic username and password. Decode this to get the `:` separated `user:pass`.\n-   `code` is the pairing code\n\nYou can decode the credentials using the `scripts/get_credentials.py` script. e.g.\n\n```bash\n python scripts/get_credentials.py \'{"webApp":"/ui/","code":"<redacted>","basicAuth":"<redacted>"}\'\n```\n\n## Development\n\n-   Init your virtualenv environment (`poetry install`)\n-   Copy `.env.example` to `.env`\n-   Decode credentials (`poetry run python scripts/get_credentials.py <basic-auth-value>`)\n-   Add your credentials to `.env` following the above process\n\nThe [pre-commit][5] framework is used enforce some linting and style compliance on CI.\n\nTo get the same behaviour locally you can run `pre-commit install` within your activated venv.\n\nAlternatively to run manually you can run `pre-commit run -a`.\n\n## Access remote UI\n\nRun `poetry run python scripts/example.py` and copy the URL to your browser of choice.\n\nYou will need the HTTP basic credentials you defined earlier within the `.env` file.\n\nBe sure to run `poetry install -E dev` to get the required dependencies for this.\n\n## Usage example\n\nA jupyter notebook showcasing the heating interval scheduler can be found in `notebooks/Heating Scheduler.ipynb`. To\naccess the notebook install [jupyter notebook or jupyter lab](https://jupyter.org/install.html) into the virtual environment and run the notebook:\n\n```sh\npoetry shell\npip install notebook\njupyter notebook\n```\n\nIf running the notebook gives you a `ModuleNotFoundError`, you may fix this issue by changing the notebook\'s kernel (following [this StackOverflow post](https://stackoverflow.com/a/47296960/50913)):\n\n```sh\npoetry shell\npython -m ipykernel install --user --name=`basename $VIRTUAL_ENV`\n```\n\nThen switch the kernel in the notebook\'s top menu under: _Kernel > Change Kernel_.\n\n## Licence\n\nMIT\n\n[0]: https://iolite.de/\n\n[1]: https://play.google.com/store/apps/details?id=de.iolite.client.android.mia\n\n[2]: https://deutsche-wohnen.com/\n\n[3]: https://www.malachisoord.com/2020/08/06/reverse-engineering-iolite-remote-api/\n\n[4]: https://python-poetry.org/\n\n[5]: https://pre-commit.com/\n',
    'author': 'Malachi Soord',
    'author_email': 'me@malachisoord.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/inverse/python-iolite-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
