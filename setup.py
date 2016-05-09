# -*- coding: utf-8 -*-
# This file is part of Shoop BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

import setuptools

NAME = 'shoop-br'
VERSION = '1.0.0'
DESCRIPTION = 'A Shoop add-on for custom Brazilian e-commerce'
AUTHOR = 'Rockho Team'
AUTHOR_EMAIL = 'rockho@rockho.com.br'
URL = 'http://www.rockho.com.br/'
LICENSE = 'AGPL-3.0'  # https://spdx.org/licenses/

if __name__ == '__main__':
    setuptools.setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        url=URL,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        packages=["shoop_br"],
        include_package_data=True,
        entry_points={"shoop.addon": "shoop_br=shoop_br"}
    )
