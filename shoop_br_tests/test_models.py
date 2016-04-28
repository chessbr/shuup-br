# -*- coding: utf-8 -*-
# This file is part of Shoop BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import unicode_literals
from django.test import override_settings

import pytest
from django.core.exceptions import ValidationError

from shoop_br.models import ShoopBRUser, validate_cpf, validate_cnpj, \
    PersonInfo, CompanyInfo, ExtraMutableAddress, ExtraImmutableAddress


@pytest.mark.django_db
def test_extra_immutable_address():
    addr = ExtraImmutableAddress.from_data({
        'numero': '321',
        'cel': '1234567890',
        'ponto_ref': 'ref1'
    })

    assert addr.numero == '321'
    assert addr.cel == '1234567890'
    assert addr.ponto_ref == 'ref1'
    s = str(addr)


@pytest.mark.django_db
def test_extra_mutable_address():
    addr = ExtraMutableAddress.from_data({
        'numero': '321',
        'cel': '1234567890',
        'ponto_ref': 'ref1'
    })

    assert addr.numero == '321'
    assert addr.cel == '1234567890'
    assert addr.ponto_ref == 'ref1'
    s = str(addr)

    immut_addr = addr.to_immutable()
    s = str(immut_addr)
    assert isinstance(immut_addr, ExtraImmutableAddress)
    assert immut_addr.numero == '321'
    assert immut_addr.cel == '1234567890'
    assert immut_addr.ponto_ref == 'ref1'


def test_validate_cpf():
    with pytest.raises(ValidationError):
        validate_cpf("01234567899")
    validate_cpf("01234567890")

def test_validate_cnpj():
    with pytest.raises(ValidationError):
        validate_cnpj("33659232000104")
    validate_cnpj("33659232000105")

@override_settings(AUTH_USER_MODEL='shoop_br.ShoopBRUser')
@pytest.mark.django_db
def test_validade_auth_user():
    from django.contrib.auth import get_user_model
    assert get_user_model() == ShoopBRUser

    su1 = ShoopBRUser.objects.create_superuser(email='admin123@adminzzzzzzzzzzzzzz.com',
                                               password='admin')
    assert su1.is_staff == True
    assert su1.is_active == True
    assert su1.get_full_name() == su1.email
    assert su1.get_short_name() == su1.email
    su1.email_user("test", "my message")

    u1 = ShoopBRUser.objects.create_user(email='user123@adminzzzzzzzzzzzzz.com',
                                         password='admin')
    assert u1.is_staff == False
    assert u1.is_active == True
    u1.email_user("test", "my message")

