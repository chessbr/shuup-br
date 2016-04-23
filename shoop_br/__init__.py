# -*- coding: utf-8 -*-
# This file is part of Shoop Correios.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

import shoop.apps
import django.conf

class ShoopBRAppConfig(shoop.apps.AppConfig):
    name = __name__
    verbose_name = "Shoop BR store"
    label = "shoop_br"

    required_installed_apps = {
        "registration": "django-registration-redux is required for user registration and activation"
    }

    provides = {
        "front_urls": [
            __name__ + ".urls:urlpatterns"
        ],
    }

default_app_config = __name__ + ".ShoopBRAppConfig"
