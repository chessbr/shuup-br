# -*- coding: utf-8 -*-
# This file is part of Shoop BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from django.conf.urls import patterns, url
from shoop_br.registration import RegistrationView, registration_complete

urlpatterns = patterns(
    '',
    url(r'^register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^register/complete/$', registration_complete, name='registration_complete')
)
