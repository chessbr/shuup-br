# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

import shuup.apps


class ShuupBRAppConfig(shuup.apps.AppConfig):
    name = __name__
    verbose_name = "Shuup BR"
    label = "shuup_br"

    required_installed_apps = {
        "registration": "django-registration-redux is required for user registration and activation"
    }

    provides = {
        "front_urls_pre": [
            __name__ + ".urls:urlpatterns"
        ],
        "admin_order_section": [
             "shuup_br.admin.order_section:ShuupBROrderSection"
        ]
    }

default_app_config = __name__ + ".ShuupBRAppConfig"

__version__ = "1.0.0.post0"
