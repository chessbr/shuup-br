# -*- coding: utf-8 -*-
# This file is part of Shoop BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

import pytest

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from shoop.core.models._contacts import Gender
from shoop.core.defaults.order_statuses import create_default_order_statuses
from shoop.xtheme._theme import set_current_theme
from shoop_tests.utils import SmartClient

from shoop.testing.mock_population import populate_if_required
from shoop.testing.factories import get_default_shop, get_default_supplier,\
    get_default_product
from shoop.testing.soup_utils import extract_form_fields

from shoop_br.models import PersonType

@pytest.mark.django_db
def test_checkout_with_success():
    get_default_shop()
    set_current_theme('shoop.themes.classic_gray')
    create_default_order_statuses()
    populate_if_required()

    client = SmartClient()

    # first step - register user
    person_data = {
        "email": "email@emailsshaushduas.com",
        "password1": "password",
        "password2": "password",
        "person_type": PersonType.FISICA.value,
        "PF-name": "NOME DA PESSOA",
        "PF-cpf": "01234567890",
        "PF-rg": "312321",
        "PF-birth_date": "03/28/1954",
        "PF-gender": Gender.MALE.value
    }

    result = client.post(reverse("shoop:registration_register"), data=person_data)
    assert not result is None
    user = get_user_model().objects.get(email=person_data['email'])
    assert user.is_active


    # second step -add something into the basket
    default_product = get_default_product()

    basket_path = reverse("shoop:basket")
    add_to_basket_resp = client.post(basket_path, data={
        "command": "add",
        "product_id": default_product.pk,
        "quantity": 1,
        "supplier": get_default_supplier().pk
    })
    assert add_to_basket_resp.status_code < 400


    # third step - go to checkout and set the addresses
    addresses_path = reverse("shoop:checkout", kwargs={"phase": "addresses"})
    addresses_data = {
        'billing-name': 'maria da silva',
        'billing-street': 'rua billing',
        'billing-street2': 'apto',
        'billing-street3': 'bairro outrem',
        'billing-postal_code': '89090200',
        'billing-city': 'plumenau',
        'billing-region': 'PR',
        'billing-country': 'BR',
        'billing-phone': '13323332',
        'billing_extra-numero': '563',
        'billing_extra-cel': '8431-4345',
        'billing_extra-ponto_ref': 'longe de tudo',

        'shipping-name': 'joao da silva',
        'shipping-street': 'rua shipping',
        'shipping-street2': 'complemento',
        'shipping-street3': 'bairro',
        'shipping-postal_code': '89050120',
        'shipping-city': 'indaial',
        'shipping-region': 'SC',
        'shipping-country': 'BR',
        'shipping-phone': '99992332',
        'shipping_extra-numero': '323',
        'shipping_extra-cel': '4444-3333',
        'shipping_extra-ponto_ref': 'proximo posto',
    }

    response = client.post(addresses_path, data=addresses_data)
    print (response.content)
    assert response.status_code == 302  # Should redirect forth


    # Set the payment and shipping methods
    methods_path = reverse("shoop:checkout", kwargs={"phase": "methods"})
    methods_soup = client.soup(methods_path)
    assert client.post(methods_path, data=extract_form_fields(methods_soup)).status_code == 302  # Should redirect forth


    # Confirm the order
    confirm_path = reverse("shoop:checkout", kwargs={"phase": "confirm"})
    confirm_soup = client.soup(confirm_path)
    assert client.post(confirm_path, data=extract_form_fields(confirm_soup)).status_code == 302  # Should redirect forth

