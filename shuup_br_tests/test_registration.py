# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

import pytest

from shuup_br.models import PersonType, Taxation

from shuup.core.models._contacts import Gender
from shuup.testing.factories import get_default_shop
from shuup.xtheme._theme import set_current_theme

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.utils import override_settings


@pytest.mark.django_db
def test_registration_PF(client):
    get_default_shop()
    set_current_theme('shuup.themes.classic_gray')

    with override_settings(
        AUTH_USER_MODEL = 'shuup_br.ShuupBRUser',
        SHOOP_REGISTRATION_REQUIRES_ACTIVATION = False,
        SHOOP_CHECKOUT_VIEW_SPEC = "shuup_br.views:ShuupBRCheckoutView",
        PARLER_DEFAULT_LANGUAGE_CODE = 'pt-br',
        SHOOP_ADDRESS_HOME_COUNTRY = 'BR'
    ):
        EMAIL = "email@emailzzzzzzzz.com"
        NAME = "NOME DA PESSOA"
        CPF = "01234567890"
        RG = "123456SC"
        BIRTH_DATE = "03/28/1954"
        GENDER = Gender.MALE.value

        client.post(reverse("shuup:registration_register"), data={
            "email": EMAIL,
            "password1": "password",
            "password2": "password",
            "person_type": PersonType.FISICA.value,
            "PF-name": NAME,
            "PF-cpf": CPF,
            "PF-rg": RG,
            "PF-birth_date": BIRTH_DATE,
            "PF-gender": GENDER
        })

        user = get_user_model().objects.get(email=EMAIL)
        assert user.is_active
        assert user.pf_person.name == NAME
        assert user.pf_person.cpf == CPF
        assert user.pf_person.rg == RG
        assert user.pf_person.birth_date.day == 28
        assert user.pf_person.birth_date.month == 3
        assert user.pf_person.birth_date.year == 1954
        assert user.pf_person.gender.value == GENDER


@pytest.mark.django_db
def test_registration_PJ1(client):
    get_default_shop()
    set_current_theme('shuup.themes.classic_gray')

    with override_settings(
        AUTH_USER_MODEL = 'shuup_br.ShuupBRUser',
        SHOOP_REGISTRATION_REQUIRES_ACTIVATION = False,
        SHOOP_CHECKOUT_VIEW_SPEC = "shuup_br.views:ShuupBRCheckoutView",
        PARLER_DEFAULT_LANGUAGE_CODE = 'pt-br',
        SHOOP_ADDRESS_HOME_COUNTRY = 'BR'
    ):
        EMAIL = "email@emailzzzzzzzz.com"
        NAME = "empresa muito legal"
        CNPJ = "66873247000120"
        IE = "378217321"
        IM = "0321033218372183721"
        TAXATION = Taxation.ICMS.value
        RESPONSIBLE = "Matheus Responsavel"

        client.post(reverse("shuup:registration_register"), data={
            "email": EMAIL,
            "password1": "password",
            "password2": "password",
            "person_type": PersonType.JURIDICA.value,
            "PJ-name": NAME,
            "PJ-cnpj": CNPJ,
            "PJ-ie": IE,
            "PJ-im": IM,
            "PJ-taxation": TAXATION,
            "PJ-responsible": RESPONSIBLE
        })

        user = get_user_model().objects.get(email=EMAIL)
        assert user.is_active
        assert user.pj_person.name == NAME
        assert user.pj_person.cnpj == CNPJ
        assert user.pj_person.ie == IE
        assert user.pj_person.im == IM
        assert user.pj_person.taxation.value == TAXATION
        assert user.pj_person.responsible == RESPONSIBLE


@pytest.mark.django_db
def test_registration_PJ2(client):
    get_default_shop()
    set_current_theme('shuup.themes.classic_gray')

    with override_settings(
        AUTH_USER_MODEL = 'shuup_br.ShuupBRUser',
        SHOOP_REGISTRATION_REQUIRES_ACTIVATION = False,
        SHOOP_CHECKOUT_VIEW_SPEC = "shuup_br.views:ShuupBRCheckoutView",
        PARLER_DEFAULT_LANGUAGE_CODE = 'pt-br',
        SHOOP_ADDRESS_HOME_COUNTRY = 'BR'
    ):
        EMAIL = "email@emailzzzzzzzz.com"
        NAME = "empresa muito legal 2"
        CNPJ = "66873247000120"
        TAXATION = Taxation.ISENTO.value
        RESPONSIBLE = "Jorge Responsavel"

        client.post(reverse("shuup:registration_register"), data={
            "email": EMAIL,
            "password1": "password",
            "password2": "password",
            "person_type": PersonType.JURIDICA.value,
            "PJ-name": NAME,
            "PJ-cnpj": CNPJ,
            "PJ-taxation": TAXATION,
            "PJ-responsible": RESPONSIBLE
        })

        user = get_user_model().objects.get(email=EMAIL)
        assert user.is_active
        assert user.pj_person.name == NAME
        assert user.pj_person.cnpj == CNPJ
        assert user.pj_person.ie == 'ISENTO'
        assert user.pj_person.im == ''
        assert user.pj_person.taxation.value == TAXATION
        assert user.pj_person.responsible == RESPONSIBLE


@pytest.mark.django_db
def test_registration_PJ3(client):
    get_default_shop()
    set_current_theme('shuup.themes.classic_gray')

    with override_settings(
        AUTH_USER_MODEL = 'shuup_br.ShuupBRUser',
        SHOOP_REGISTRATION_REQUIRES_ACTIVATION = False,
        SHOOP_CHECKOUT_VIEW_SPEC = "shuup_br.views:ShuupBRCheckoutView",
        PARLER_DEFAULT_LANGUAGE_CODE = 'pt-br',
        SHOOP_ADDRESS_HOME_COUNTRY = 'BR'
    ):
        EMAIL = "email@emailzzzzzzzz.com"
        NAME = "empresa muito legal 2"
        CNPJ = "66873247000120"
        TAXATION = Taxation.NAO_CONTRIBUINTE.value
        RESPONSIBLE = "Jorge Responsavel"

        client.post(reverse("shuup:registration_register"), data={
            "email": EMAIL,
            "password1": "password",
            "password2": "password",
            "person_type": PersonType.JURIDICA.value,
            "PJ-name": NAME,
            "PJ-cnpj": CNPJ,
            "PJ-taxation": TAXATION,
            "PJ-responsible": RESPONSIBLE
        })

        user = get_user_model().objects.get(email=EMAIL)
        assert user.is_active
        assert user.pj_person.name == NAME
        assert user.pj_person.cnpj == CNPJ
        assert user.pj_person.ie == ''
        assert user.pj_person.im == ''
        assert user.pj_person.taxation.value == TAXATION
        assert user.pj_person.responsible == RESPONSIBLE
