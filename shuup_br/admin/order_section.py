# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from shuup_br.models import PersonType

from shuup.admin.base import OrderSection

from django.utils.translation import ugettext_lazy as _


class ShuupBROrderSection(OrderSection):
    identifier = 'br'
    name = _('Dados pessoais')
    icon = 'fa-user'
    template = 'shuup_br/admin/order_section.jinja'
    order = -5

    @staticmethod
    def visible_for_order(order):
        return True

    @staticmethod
    def get_context_data(order):
        return {
            "PersonType": PersonType
        }
