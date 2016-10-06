# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shuup_br.admin.order_section import ShuupBROrderSection

from shuup.core.models._orders import Order


def test_order_section():
    assert ShuupBROrderSection.visible_for_order(Order())
    ShuupBROrderSection.get_context_data(Order())
