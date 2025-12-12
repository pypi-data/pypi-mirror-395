# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['immunopipe', 'immunopipe.cli_utils', 'immunopipe.mcp']

package_data = \
{'': ['*'], 'immunopipe': ['reports/*', 'scripts/*']}

install_requires = \
['biopipen>=0.34.30,<0.35.0']

extras_require = \
{'cli-gbatch': ['pipen-cli-gbatch>=0.1,<0.2'],
 'diagram': ['pipen-diagram>=0.13,<0.14'],
 'dry': ['pipen-dry>=0.12,<0.13'],
 'runinfo': ['pipen-runinfo>=0.9,<0.10']}

entry_points = \
{'console_scripts': ['immunopipe = immunopipe.router:run']}

setup_kwargs = {
    'name': 'immunopipe',
    'version': '2.2.1',
    'description': 'A pipeline for integrative analysis for scRNA-seq and scTCR-/scBCR-seq data',
    'long_description': '<p align="center">\n  <img height="120" style="height: 120px" src="https://github.com/pwwang/immunopipe/blob/dev/docs/logo.png?raw=true" />\n</p>\n<p align="center">Integrative analysis for single-cell RNA sequencing and single-cell TCR/BCR sequencing data</p>\n<hr />\n\n`immunopipe` is a pipeline based on [`pipen`](https://github.com/pwwang/pipen) framework. It includes a set of processes for scRNA-seq and scTCR-/scBCR-seq data analysis in `R`, `python` and `bash`. The pipeline is designed to be flexible and configurable.\n\n<p align="center">\n  <img src="https://github.com/pwwang/immunopipe/blob/dev/docs/immunopipe.ms.png?raw=true" />\n</p>\n\nSee a more detailed flowchart [here](https://github.com/pwwang/immunopipe/blob/dev/docs/immunopipe.flowchart.png?raw=true).\n\n## Documentaion\n\n[https://pwwang.github.io/immunopipe](https://pwwang.github.io/immunopipe)\n\n## Proposing more analyses\n\nIf you have any suggestions for more analyses, please feel free to open an issue [here](https://github.com/pwwang/immunopipe/issues/new)\n\n## Example\n\n[https://github.com/pwwang/immunopipe-example](https://github.com/pwwang/immunopipe-example)\n\n## Gallery\n\nThere are some datasets with both scRNA-seq and scTCR-/scBCR-seq data available in the publications. The data were reanalyzed using `immunopipe` with the configurations provided in each repository, where the results are also available.\n\nCheck out the [gallery](https://pwwang.github.io/immunopipe/gallery) for more details.\n\n## Citation\n\nIf you use `immunopipe` in your research, please cite the following paper:\n\n- [Wang, P., Yu, Y., Dong, H., Zhang, S., Sun, Z., Zeng, H., ... & Li, Y. (2025). Immunopipe: a comprehensive and flexible scRNA-seq and scTCR-seq data analysis pipeline. NAR Genomics and Bioinformatics, 7(2), lqaf063.](https://academic.oup.com/nargab/article/7/2/lqaf063/8136476)\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pwwang/immunopipe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
