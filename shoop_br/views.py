# -*- coding: utf-8 -*-
# This file is part of Shoop Correios.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from shoop.front.views.checkout import DefaultCheckoutView

class ShoopBRCheckoutView(DefaultCheckoutView):
    """
    View de checkout que precisa de um usuário
    registrado antes de iniciar o processo de checkout.
    A fase de endereço é levemente diferente do original.
    """

    phase_specs = [
        "shoop_br.checkout.addresses:AddressesPhase",
        "shoop.front.checkout.methods:MethodsPhase",
        "shoop.front.checkout.methods:ShippingMethodPhase",
        "shoop.front.checkout.methods:PaymentMethodPhase",
        "shoop.front.checkout.confirm:ConfirmPhase",
    ]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() and not settings.SHOOP_ALLOW_ANONYMOUS_ORDERS:
            # FIXME: Django 1.9:
            # return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
            return redirect_to_login(self.request.get_full_path())

        return super(ShoopBRCheckoutView, self).dispatch(request, *args, **kwargs)
