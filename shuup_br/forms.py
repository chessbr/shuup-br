# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from datetime import timedelta

from shuup_br.base import CNPJ, CPF
from shuup_br.models import CompanyInfo, PersonInfo, Taxation,\
    ExtraMutableAddress, ESTADOS_CHOICES

from django import forms
from django.utils import formats
from django.utils.functional import lazy
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from shuup.core.models._contacts import Gender
from shuup.core.utils.forms import MutableAddressForm
from shuup.core.models._addresses import MutableAddress
from django.forms.models import model_to_dict


def get_sample_datetime():
    return (now()-timedelta(days=365*30)).strftime(formats.get_format_lazy('DATE_INPUT_FORMATS')[0])


class ShuupBRMutableAddressForm(MutableAddressForm):
    name = forms.CharField(label=_('Destinatário'))
    phone = forms.CharField(label=_('Telefone'), required=True)
    postal_code = forms.CharField(label=_('CEP'), required=True)
    street2 = forms.CharField(label=_('Complemento'), required=False)
    street3 = forms.CharField(label=_('Bairro'), required=True)
    region = forms.ChoiceField(label=_('Estado'), required=True, choices=ESTADOS_CHOICES)
    numero = forms.CharField(label=_('Número'), required=True)
    cel = forms.CharField(label=_('Celular'), required=False)
    ponto_ref = forms.CharField(label=_('Ponto de referência'), required=False)

    class Meta:
        model = MutableAddress
        fields = (
            "name", "postal_code", "street", "numero",
            "street2", "street3", "ponto_ref",
            "city", "region", "country", "phone", "cel"
        )
        widgets = {
            'country': forms.HiddenInput(),
        }

    def __init__(self, instance=None, *args, **kwargs):
        initial = kwargs.pop('initial', {})

        if instance and hasattr(instance, 'extra'):
            initial.update(model_to_dict(instance.extra))

        super(ShuupBRMutableAddressForm, self).__init__(initial=initial,
                                                        instance=instance,
                                                        *args, **kwargs)

    def save(self, commit=True):
        instance = super(ShuupBRMutableAddressForm, self).save(commit)

        if commit:
            extra_addr = ExtraMutableAddress.objects.get_or_create(address=instance)[0]
        else:
            extra_addr = ExtraMutableAddress(address=instance)

        extra_addr.numero = self.cleaned_data['numero']
        extra_addr.cel = self.cleaned_data['cel']
        extra_addr.ponto_ref = self.cleaned_data['ponto_ref']
        extra_addr.full_clean()
        extra_addr.save()

        return instance


class PersonInfoForm(forms.ModelForm):

    class Meta:
        model = PersonInfo
        fields = ['name', 'cpf', 'rg', 'birth_date', 'gender']
        widgets = {
            'birth_date': forms.DateInput(attrs={'placeholder': lazy(get_sample_datetime, str)()}),
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
