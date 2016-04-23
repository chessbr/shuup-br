# -*- coding: utf-8 -*-
# This file is part of Shoop Correios.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from django import forms
from django.utils.translation import ugettext_lazy as _

from shoop_br.models import CompanyInfo, PersonInfo, Taxation
from shoop_br.base import CNPJ, CPF
from shoop.core.models._contacts import Gender
from django.utils.functional import lazy
from django.utils import formats
from django.utils.timezone import now
from _datetime import timedelta

def get_sample_datetime():
    return (now()-timedelta(days=365*30)).strftime(formats.get_format_lazy('DATE_INPUT_FORMATS')[0])

class PersonInfoForm(forms.ModelForm):

    class Meta:
        model = PersonInfo
        fields = ['name', 'cpf', 'rg', 'birth_date', 'gender']
        widgets = {
            'birth_date': forms.DateInput(attrs={'placeholder':lazy(get_sample_datetime, str)()}),
        }
        localized_fields = ('birth_date',)
        prefix = 'person'

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']

        if not CPF.validate(cpf):
            raise forms.ValidationError(_("CPF inválido"))
        return cpf

    def clean_gender(self):
        gender = self.cleaned_data['gender']

        # Se for do tipo Gender, então pega só o valor
        # e não a classe toda...
        if type(gender) == Gender:
            return gender.value
        return gender

class CompanyInfoForm(forms.ModelForm):
    prefix = 'company'

    class Meta:
        model = CompanyInfo
        fields = ['name', 'cnpj', 'ie', 'im', 'taxation', 'responsible']

    def clean_taxation(self):
        taxation = self.cleaned_data['taxation']

        # Se for do tipo Taxation, então pega só o valor
        # e não a classe toda...
        if type(taxation) == Taxation:
            return taxation.value
        return taxation

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']

        if not CNPJ.validate(cnpj):
            raise forms.ValidationError(_("CNPJ inválido"))
        return cnpj

    def clean(self):
        cleaned_data = super(CompanyInfoForm, self).clean()
        taxation = cleaned_data.get('taxation')

        # quando for contribuinte do ICMS, inscrição estadual é obrigatória
        if taxation == Taxation.ICMS.value and not cleaned_data.get('ie'):
            self.add_error('ie', _("A Inscrição Estadual é obrigatória quando for contribuinte do ICMS."))
        elif taxation == Taxation.ISENTO.value:
            cleaned_data['ie'] = 'ISENTO'
        elif taxation == Taxation.NAO_CONTRIBUINTE.value:
            cleaned_data['ie'] = ''

        return cleaned_data
