# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tlpui', 'tlpui.ui_config_objects']

package_data = \
{'': ['*'],
 'tlpui': ['configschema/*',
           'defaults/*',
           'icons/*',
           'icons/flags/*',
           'icons/themeable/hicolor/128x128/apps/*',
           'icons/themeable/hicolor/16x16/apps/*',
           'icons/themeable/hicolor/256x256/apps/*',
           'icons/themeable/hicolor/32x32/apps/*',
           'icons/themeable/hicolor/48x48/apps/*',
           'icons/themeable/hicolor/64x64/apps/*',
           'icons/themeable/hicolor/96x96/apps/*',
           'icons/themeable/hicolor/scalable/actions/*',
           'icons/themeable/hicolor/scalable/apps/*',
           'lang/de_DE/LC_MESSAGES/*',
           'lang/en_EN/LC_MESSAGES/*',
           'lang/es_ES/LC_MESSAGES/*',
           'lang/fr_FR/LC_MESSAGES/*',
           'lang/hu_HU/LC_MESSAGES/*',
           'lang/id_ID/LC_MESSAGES/*',
           'lang/it_IT/LC_MESSAGES/*',
           'lang/pt_BR/LC_MESSAGES/*',
           'lang/ru_RU/LC_MESSAGES/*',
           'lang/tr_TR/LC_MESSAGES/*',
           'lang/zh_CN/LC_MESSAGES/*',
           'lang/zh_TW/LC_MESSAGES/*']}

install_requires = \
['pygobject>=3.46.0,<4.0.0', 'pyyaml>=6.0.1,<7.0.0']

entry_points = \
{'console_scripts': ['tlpui = tlpui.__main__:main']}

setup_kwargs = {
    'name': 'tlp-ui',
    'version': '1.9.0',
    'description': 'GTK UI for tlp',
    'long_description': '\n<img src="https://raw.githubusercontent.com/d4nj1/TLPUI/master/tlpui/icons/themeable/hicolor/scalable/apps/tlpui.svg" align="left" alt="TLP UI" width="196px">\n\n## TLP UI\n\nThe Python scripts in this project generate a GTK-UI to change [TLP](https://github.com/linrunner/TLP) configuration files easily.\nIt has the aim to protect users from setting bad configuration and to deliver a basic overview of all the valid configuration values.\n\n<img src="https://raw.githubusercontent.com/d4nj1/TLPUI/master/screenshots/tlpui-01.png" alt="Screenshot" vspace="20px">\n\n### Install and run instructions :ledger:\n\n* [PyPI](https://github.com/d4nj1/TLPUI/blob/master/docs/INSTALL.md#pypi)\n* [Poetry](https://github.com/d4nj1/TLPUI/blob/master/docs/INSTALL.md#poetry)\n* [Python 3](https://github.com/d4nj1/TLPUI/blob/master/docs/INSTALL.md#python-3)\n* [Arch Linux](https://github.com/d4nj1/TLPUI/blob/master/docs/INSTALL.md#arch-linux)\n\n<a href=\'https://flathub.org/apps/details/com.github.d4nj1.tlpui\'><img width=\'240\' alt=\'Download on Flathub\' src=\'https://flathub.org/assets/badges/flathub-badge-en.png\'/></a>\n\n### Current status :sunrise_over_mountains:\n\n* Supports TLP versions 1.3-1.9 - _older TLP versions are supported by [1.6.1](https://github.com/d4nj1/TLPUI/releases/tag/tlpui-1.6.1)_\n* Requires Python 3.10 or greater\n* Configuration can be read and displayed\n* Shows information about configuration changes (defaults/unsaved and drop-in/user config)\n* Changes can be saved with user and sudo permissions (/etc/tlp.conf)\n* tlp-stat can be load in ui (simple and complete)\n\n### To be done :building_construction:\n\n* Weblate translations - [#121](https://github.com/d4nj1/TLPUI/issues/121)\n* Mobile UI - [#111](https://github.com/d4nj1/TLPUI/issues/111)\n* Implement package build pipeline - [#90](https://github.com/d4nj1/TLPUI/issues/90)\n',
    'author': 'Daniel Christophis',
    'author_email': 'code@devmind.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/d4nj1/TLPUI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<4.0.0',
}


setup(**setup_kwargs)
