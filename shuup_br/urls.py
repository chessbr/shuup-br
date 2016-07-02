# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from shuup_br.registration import registration_complete, RegistrationView

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^register/complete/$', registration_complete, name='registration_complete')
)
