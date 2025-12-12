# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['es_translator',
 'es_translator.interpreters',
 'es_translator.interpreters.apertium',
 'es_translator.interpreters.argos']

package_data = \
{'': ['*']}

install_requires = \
['argostranslate>=1.9.6,<2.0.0',
 'celery[redis]>=5.3.1,<6.0.0',
 'click>=8,<9',
 'coloredlogs',
 'deb-pkg-tools>=8.4,<9.0',
 'elasticsearch-dsl>=7,<8.0.0',
 'elasticsearch>=7.10,<7.18',
 'filelock>=3.12.2,<4.0.0',
 'numpy>=1.26.0',
 'pycountry>=22.3,<23.0',
 'rich>=13,<14',
 'sh>=1.14,<2.0',
 'torch>=2.3,<2.4',
 'urllib3>=1.26,<2.0']

entry_points = \
{'console_scripts': ['es-translator = es_translator.cli:translate',
                     'es-translator-pairs = es_translator.cli:pairs',
                     'es-translator-tasks = es_translator.cli:tasks']}

setup_kwargs = {
    'name': 'es-translator',
    'version': '1.10.0',
    'description': 'A lazy yet bulletproof machine translation tool for Elasticsearch.',
    'long_description': "# ES Translator [![](https://img.shields.io/github/actions/workflow/status/icij/es-translator/main.yml)](https://github.com/ICIJ/es-translator/actions) [![](https://img.shields.io/pypi/pyversions/es-translator)](https://pypi.org/project/es-translator/) \n\nA lazy yet bulletproof machine translation tool for Elasticsearch.\n\n## Installation (Ubuntu)\n\nInstall Apertium:\n\n```bash\nwget https://apertium.projectjj.com/apt/install-nightly.sh -O - | sudo bash\nsudo apt install apertium-all-dev\n```\n\nThen install es-translator with pip:\n\n```bash\npython3 -m pip install --user es-translator\n```\n\n## Installation (Docker)\n\nNothing to do as long as you have Docker on your system:\n\n```\ndocker run -it icij/es-translator es-translator --help\n```\n\n## Usage\n\nThe primary command from EsTranslator to translate documents is `es-translator`:\n\n\n```\nUsage: es-translator [OPTIONS]\n\nOptions:\n  -u, --url TEXT                  Elasticsearch URL\n  -i, --index TEXT                Elasticsearch Index\n  -r, --interpreter TEXT          Interpreter to use to perform the\n                                  translation\n  -s, --source-language TEXT      Source language to translate from\n                                  [required]\n  -t, --target-language TEXT      Target language to translate to  [required]\n  --intermediary-language TEXT    An intermediary language to use when no\n                                  translation is available between the source\n                                  and the target. If none is provided this\n                                  will be calculated automatically.\n  --source-field TEXT             Document field to translate\n  --target-field TEXT             Document field where the translations are\n                                  stored\n  -q, --query-string TEXT         Search query string to filter result\n  -d, --data-dir PATH             Path to the directory where the language\n                                  model will be downloaded\n  --scan-scroll TEXT              Scroll duration (set to higher value if\n                                  you're processing a lot of documents)\n  --dry-run                       Don't save anything in Elasticsearch\n  -f, --force                     Override existing translation in\n                                  Elasticsearch\n  --pool-size INTEGER             Number of parallel processes to start\n  --pool-timeout INTEGER          Timeout to add a translation\n  --throttle INTEGER              Throttle between each translation (in ms)\n  --syslog-address TEXT           Syslog address\n  --syslog-port INTEGER           Syslog port\n  --syslog-facility TEXT          Syslog facility\n  --stdout-loglevel TEXT          Change the default log level for stdout\n                                  error handler\n  --progressbar / --no-progressbar\n                                  Display a progressbar\n  --plan                          Plan translations into a queue instead of\n                                  processing them now\n  --broker-url TEXT               Celery broker URL (only needed when planning\n                                  translation)\n  --max-content-length TEXT       Max translated content length\n                                  (<[0-9]+[KMG]?>) to avoid highlight\n                                  errors(see http://github.com/ICIJ/datashare/\n                                  issues/1184)\n  --help                          Show this message and exit.\n```\n\nLearn more about how to use this command in the [Usage Documentation](https://icij.github.io/es-translator/usage/).\n\n## API\n\nYou can explore the [API Documentation](https://icij.github.io/es-translator/api/) for more information.\n\n\n## Releasing a New Version\n\nThis section describes how to release a new version of es-translator. Only maintainers with publish access can perform releases.\n\n### Prerequisites\n\n* Push access to the GitHub repository\n* PyPI credentials configured for Poetry (`poetry config pypi-token.pypi <your-token>`)\n* Docker Hub credentials (for Docker image publishing)\n\n### Release Process\n\n#### 1. Ensure All Tests Pass\n\nBefore releasing, make sure all tests and linting checks pass:\n\n```shell\nmake lint\nmake test\n```\n\n#### 2. Bump the Version\n\nUse one of the semantic versioning targets to bump the version:\n\n```shell\n# For bug fixes (1.0.0 -> 1.0.1)\nmake patch\n\n# For new features (1.0.0 -> 1.1.0)\nmake minor\n\n# For breaking changes (1.0.0 -> 2.0.0)\nmake major\n```\n\nThis will:\n\n* Update the version in `pyproject.toml`\n* Create a git commit with the message `build: bump to <version>`\n* Create a git tag with the new version\n\nAlternatively, set a specific version:\n\n```shell\nmake set-version CURRENT_VERSION=1.2.3\n```\n\n#### 3. Push Changes and Tags\n\nPush the commit and tag to GitHub:\n\n```shell\ngit push origin master\ngit push origin --tags\n```\n\n#### 4. Publish to PyPI\n\nPublish the package to PyPI:\n\n```shell\nmake distribute\n```\n\nThis builds the package and uploads it to PyPI using Poetry.\n\n#### 5. Publish Docker Image (Optional)\n\nTo publish a new Docker image:\n\n```shell\n# First-time setup for multi-arch builds\nmake docker-setup-multiarch\n\n# Build and push the Docker image\nmake docker-publish\n```\n\nThis will build and push the image with both the version tag and `latest` tag to Docker Hub.\n\n#### 6. Update Documentation\n\nIf documentation has changed, publish the updated docs:\n\n```shell\nmake publish-doc\n```\n\n### Version Numbering\n\nWe follow [Semantic Versioning](https://semver.org/):\n\n* **MAJOR** version for incompatible API changes\n* **MINOR** version for new functionality in a backwards compatible manner\n* **PATCH** version for backwards compatible bug fixes\n\n### Makefile Targets Reference\n\n| Target                                   | Description                          |\n| ---------------------------------------- | ------------------------------------ |\n| `make patch`                             | Bump patch version (x.x.X)           |\n| `make minor`                             | Bump minor version (x.X.0)           |\n| `make major`                             | Bump major version (X.0.0)           |\n| `make set-version CURRENT_VERSION=x.x.x` | Set specific version                 |\n| `make distribute`                        | Build and publish to PyPI            |\n| `make docker-publish`                    | Build and push Docker image          |\n| `make publish-doc`                       | Deploy documentation to GitHub Pages |\n\n## Contributing\n\nContributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/icij/es-translator). If you're willing to help, check the page about [how to contribute](https://icij.github.io/es-translator/contributing/) to this project.\n\n## License\n\nThis project is licensed under the MIT License. See the [LICENSE](https://github.com/icij/es-translator/blob/main/LICENSE.md) file for more details.\n\n",
    'author': 'ICIJ',
    'author_email': 'engineering@icij.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
