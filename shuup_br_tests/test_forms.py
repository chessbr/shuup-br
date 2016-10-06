# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

import pytest

from shuup_br.forms import CompanyInfoForm, PersonInfoForm
from shuup_br.models import Taxation, ShuupBRUser

from shuup.core.models._contacts import Gender
from django.test.utils import override_settings

@override_settings(AUTH_USER_MODEL='shuup_br.ShuupBRUser')
@pytest.mark.django_db
def test_person_form():
    pif = PersonInfoForm(data={
        'name': "Nombre del Fulano",
        'cpf': '012.345.678-90',
        'rg': '12323213',
        'birth_date': '12/29/1958',
        'gender': Gender.MALE.value
    })

    assert pif.is_valid() == True

    # verifica se ao salvar os caracteres especiais são removidos
    pi = pif.save(commit=False)
    pi.user = ShuupBRUser.objects.create_user(email='admin123@adminzzzz.com', password='admin')
    pi.save()
    assert pi.cpf == '01234567890'


@pytest.mark.django_db
def test_company_form_1():
    cif = CompanyInfoForm(data={
        'name': "Nombre del Companya",
        'cnpj': '89.139.268/0001-12',
        'ie': '431829',
        'im': '4352103521',
        'taxation': Taxation.ICMS.value,
        'responsible': 'meramente resposavel'
    })
    assert cif.is_valid() == True
    assert not cif.cleaned_data['ie'] in ('ISENTO', '')

    # verifica se ao salvar os caracteres especiais são removidos
    ci = cif.save(commit=False)
    ci.user = ShuupBRUser.objects.create_user(email='admin123@adminzzzz.com', password='admin')
    ci.save()
    assert ci.cnpj == '89139268000112'


def test_company_form_2():
    cif = CompanyInfoForm(data={
        'name': "Nombre del Companya",
        'cnpj': '89.139.268/0001-12',
        'ie': '431829',
        'im': '4352103521',
        'taxation': Taxation.ISENTO.value,
        'responsible': 'meramente resposavel'
    })
    assert cif.is_valid() == True
    assert cif.cleaned_data['ie'] == 'ISENTO'

def test_company_form_3():
    cif = CompanyInfoForm(data={
        'name': "Nombre del Companya",
        'cnpj': '89.139.268/0001-12',
        'ie': '431829',
        'im': '4352103521',
        'taxation': Taxation.NAO_CONTRIBUINTE.value,
        'responsible': 'meramente resposavel'
    })
    assert cif.is_valid() == True
    assert cif.cleaned_data['ie'] == ''
