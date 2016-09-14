# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.test.utils import override_settings
from shuup_br.models import ExtraMutableAddress
import pytest
from shuup.core.models._addresses import MutableAddress
from shuup.testing.factories import get_default_shop
from shuup.xtheme._theme import set_current_theme
from shuup.utils.importing import clear_load_cache


@pytest.mark.django_db
def test_format_address():
    get_default_shop()
    set_current_theme('shuup.themes.classic_gray')
    clear_load_cache()

    with override_settings(
        SHUUP_ADDRESS_FORMATTER_SPEC='shuup_br.formatters:ShuupBRAddressFormatter'
    ):
        addr = MutableAddress.from_data({
            'name': 'name',
            'street': 'street',
            'street2': 'street2',
            'postal_code': 'postal_code',
            'city': 'city',
            'region': 'region'
        })
        addr.save()

        extra_addr = ExtraMutableAddress.from_data({
            'numero': '321',
            'ponto_ref': 'ref1'
        })

        extra_addr.address = addr
        extra_addr.save()

        addr_str_list = addr.as_string_list()

        assert addr_str_list == [
            addr.full_name,
            "{0}, {1}".format(addr.street, addr.extra.numero),
            addr.street2,
            addr.extra.ponto_ref,
            addr.postal_code,
            "{0} {1}".format(addr.city, addr.region or addr.region_code)
        ]
