# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from datetime import timedelta

from django.utils import formats
from django.utils.timezone import now


def get_sample_datetime():
    return (now()-timedelta(days=365*30)).strftime(formats.get_format_lazy('DATE_INPUT_FORMATS')[0])


def get_only_digits(value):
    return "".join([c for c in value if c.isdigit()])
