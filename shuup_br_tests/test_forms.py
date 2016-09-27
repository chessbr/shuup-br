# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from shuup_br.forms import CompanyInfoForm, PersonInfoForm
from shuup_br.models import Taxation

from shuup.core.models._contacts import Gender


def test_person_form():
    pif = PersonInfoForm(data={
        'name': "Nombre del Fulano",
        'cpf': '01234567890',
        'rg': '12323213',
        'birth_date': '12/29/1958',
        'gender': Gender.MALE.value
    })

    assert pif.is_valid() == True

def test_company_form_1():
    cif = CompanyInfoForm(data={
        'name': "Nombre del Companya",
        'cnpj': '89139268000112',
        'ie': '431829',
        'im': '4352103521',
        'taxation': Taxation.ICMS.value,
        'responsible': 'meramente resposavel'
    })
    assert cif.is_valid() == True
    assert not cif.cleaned_data['ie'] in ('ISENTO', '')

def test_company_form_2():
    cif = CompanyInfoForm(data={
        'name': "Nombre del Companya",
        'cnpj': '89139268000112',
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
        'cnpj': '89139268000112',
        'ie': '431829',
        'im': '4352103521',
        'taxation': Taxation.NAO_CONTRIBUINTE.value,
        'responsible': 'meramente resposavel'
    })
    assert cif.is_valid() == True
    assert cif.cleaned_data['ie'] == ''
