# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shuup.core.formatters import BaseAddressFormatter
from shuup.core.models._addresses import Address
from shuup.utils.i18n import get_current_babel_locale
from django.utils.encoding import force_text


class ShuupBRAddressFormatter(BaseAddressFormatter):

    def address_as_string_list(self, address, locale=None):
        assert issubclass(type(address), Address)

        locale = locale or get_current_babel_locale()
        country = address.country.code.upper()

        base_lines = [
            address.company_name,
            address.full_name,
            address.name_ext,
            address.street,
            address.extra.numero,
            address.street2,
            address.street3,
            address.extra.ponto_ref,
            "%s %s %s" % (address.region_code, address.postal_code, address.city),
            address.region,
            locale.territories.get(country, country) if not address.is_home else None
        ]

        stripped_lines = [force_text(line).strip() for line in base_lines if line]
        return [s for s in stripped_lines if (s and len(s) > 1)]
