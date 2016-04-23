# -*- coding: utf-8 -*-
# This file is part of Shoop Correios.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from shoop.front.basket.order_creator import BasketOrderCreator

class ShoopBRBasketOrderCreator(BasketOrderCreator):
    """ Processo customizado para criar o pedido.
        Vamos aqui apenas salvar o endereço 'extra' que criamos
    """
    def create_order(self, order_source):
        extra_billing_address = order_source.billing_address.extra if order_source.billing_address and hasattr(order_source.billing_address, 'extra') else None
        extra_shipping_address = order_source.shipping_address.extra if order_source.shipping_address and hasattr(order_source.shipping_address, 'extra') else None

        order = super(ShoopBRBasketOrderCreator, self).create_order(order_source)

        if extra_billing_address and order.billing_address and not hasattr(order.billing_address, 'extra'):
            immutable_extra_billing_address = extra_billing_address.to_immutable()
            immutable_extra_billing_address.address = order.billing_address
            immutable_extra_billing_address.save()

        if extra_shipping_address and order.shipping_address and not hasattr(order.shipping_address, 'extra'):
            immutable_extra_shipping_address = extra_shipping_address.to_immutable()
            immutable_extra_shipping_address.address = order.shipping_address
            immutable_extra_shipping_address.save()

        return order
