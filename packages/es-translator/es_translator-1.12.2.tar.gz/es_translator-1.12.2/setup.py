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
 'plotext>=5.3.2,<6.0.0',
 'pycountry>=24,<25',
 'rich>=13,<14',
 'sh>=1.14,<2.0',
 'torch>=2.3,<2.4',
 'urllib3>=1.26,<2.0']

entry_points = \
{'console_scripts': ['es-translator = es_translator.cli:translate',
                     'es-translator-monitor = es_translator.cli:monitor',
                     'es-translator-pairs = es_translator.cli:pairs',
                     'es-translator-tasks = es_translator.cli:tasks']}

setup_kwargs = {
    'name': 'es-translator',
    'version': '1.12.2',
    'description': 'A lazy yet bulletproof machine translation tool for Elasticsearch.',
    'long_description': '# ES Translator [![](https://img.shields.io/github/actions/workflow/status/icij/es-translator/main.yml)](https://github.com/ICIJ/es-translator/actions) [![](https://img.shields.io/pypi/pyversions/es-translator)](https://pypi.org/project/es-translator/)\n\nA lazy yet bulletproof machine translation tool for Elasticsearch.\n\n## Installation\n\n### pip\n\n```bash\npip install es-translator\n```\n\n### Docker\n\n```bash\ndocker run -it icij/es-translator es-translator --help\n```\n\n## Quick Start\n\nTranslate documents from French to English:\n\n```bash\nes-translator \\\n  --url "http://localhost:9200" \\\n  --index my-index \\\n  --source-language fr \\\n  --target-language en\n```\n\n## Features\n\n- **Two translation engines**: Argos (neural MT) and Apertium (rule-based MT)\n- **Distributed processing**: Scale across multiple servers with Celery/Redis\n- **Elasticsearch integration**: Direct read/write with scroll API support\n- **Flexible filtering**: Translate specific documents using query strings\n- **Incremental translation**: Skip already-translated documents\n\n## Documentation\n\n- [Usage Guide](https://icij.github.io/es-translator/usage/) - Complete usage instructions\n- [Configuration](https://icij.github.io/es-translator/configuration/) - All options and environment variables\n- [Datashare Integration](https://icij.github.io/es-translator/datashare/) - Using with ICIJ\'s Datashare\n- [Architecture](https://icij.github.io/es-translator/architecture/) - How es-translator works\n- [API Reference](https://icij.github.io/es-translator/api/) - Python API documentation\n\n## Contributing\n\nContributions are welcome! See our [Contributing Guide](https://icij.github.io/es-translator/contributing/) for details.\n\n## License\n\nThis project is licensed under the MIT License. See [LICENSE](LICENSE.md) for details.\n',
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
