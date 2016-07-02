# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import unicode_literals

from shuup_br.models import ExtraMutableAddress, PersonType

from shuup.core.models import MutableAddress
from shuup.front.checkout import CheckoutPhaseViewMixin
from shuup.utils.form_group import FormGroup

from django import forms
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

ESTADOS_CHOICES = (
    ('AC', _('Acre')),
    ('AL', _('Alagoas')),
    ('AP', _('Amapá')),
    ('AM', _('Amazonas')),
    ('BA', _('Bahia')),
    ('CE', _('Ceará')),
    ('DF', _('Distrito Federal')),
    ('ES', _('Espírito Santo')),
    ('GO', _('Goiás')),
    ('MA', _('Maranhão')),
    ('MT', _('Mato Grosso')),
    ('MS', _('Mato Grosso do Sul')),
    ('MG', _('Minas Gerais')),
    ('PA', _('Pará')),
    ('PB', _('Paraíba')),
    ('PR', _('Paraná')),
    ('PE', _('Pernambuco')),
    ('PI', _('Piauí')),
    ('RJ', _('Rio de Janeiro')),
    ('RN', _('Rio Grande do Norte')),
    ('RS', _('Rio Grande do Sul')),
    ('RO', _('Rondônia')),
    ('RR', _('Roraima')),
    ('SC', _('Santa Catarina')),
    ('SP', _('São Paulo')),
    ('SE', _('Sergipe')),
    ('TO', _('Tocantins')),
)


class AddressForm(forms.ModelForm):
    name = forms.CharField(label=_('Destinatário'))
    phone = forms.CharField(label=_('Telefone'), required=True)
    postal_code = forms.CharField(label=_('CEP'), required=True)
    street2 = forms.CharField(label=_('Complemento'), required=False)
    street3 = forms.CharField(label=_('Bairro'), required=True)
    region = forms.ChoiceField(label=_('Estado'), required=True, choices=ESTADOS_CHOICES)

    class Meta:
        model = MutableAddress
        fields = ("name", "phone", "postal_code", "street", "street2", "street3", "city", "region", "country")
        widgets = {
            'country': forms.HiddenInput(),
        }

    def __init__(self, **kwargs):
        super(AddressForm, self).__init__(**kwargs)
        if not kwargs.get("instance"):
            # Set default country
            self.fields["country"].initial = settings.SHUUP_ADDRESS_HOME_COUNTRY


class ExtraMutableAddressForm(forms.ModelForm):
    class Meta:
        model = ExtraMutableAddress
        fields = ("numero", "cel", "ponto_ref")


class AddressesPhase(CheckoutPhaseViewMixin, FormView):
    identifier = "addresses"
    title = _(u"Addresses")
    template_name = "shuup_br/checkout/addresses.jinja"

    address_kinds = ("shipping", "shipping_extra", "billing", "billing_extra")

    address_form_class = AddressForm
    address_form_classes = {"shipping_extra": ExtraMutableAddressForm, "billing_extra": ExtraMutableAddressForm}

    def get_context_data(self, **kwargs):
        # adiciona no contexto do render do template se foi processado o form ao menos uma vez
        kwargs['processed_once'] = self.storage.get('processed_once', False)
        return super(AddressesPhase, self).get_context_data(**kwargs)

    def get_form(self, form_class):
        fg = FormGroup(**self.get_form_kwargs())
        for kind in self.address_kinds:
            fg.add_form_def(kind, form_class=self.address_form_classes.get(kind, self.address_form_class))
        return fg

    def get_initial(self):
        initial = super(AddressesPhase, self).get_initial()
        for address_kind in self.address_kinds:
            if self.storage.get(address_kind):
                for key, value in model_to_dict(self.storage[address_kind]).items():
                    initial["%s-%s" % (address_kind, key)] = value

            # Coloca o nome da PF ou da PJ nos campos Destinatário dos forms
            elif address_kind in ('shipping', 'billing'):
                if self.request.user.person_type == PersonType.JURIDICA:
                    if hasattr(self.request.user, 'pj_person'):
                        initial["{0}-name".format(address_kind)] = self.request.user.pj_person.name
                else:
                    if hasattr(self.request.user, 'pf_person'):
                        initial["{0}-name".format(address_kind)] = self.request.user.pf_person.name

        return initial

    def is_valid(self):
        return self.storage.has_all(self.address_kinds)

    def form_valid(self, form):

        for key in self.address_kinds:
            # não salva diretamente os endereços EXTRA
            if key.endswith("extra"):
                continue

            extra_address_key = "{0}_extra".format(key)
            self.storage[key] = form.forms[key].save()
            self.storage[extra_address_key] = form.forms[extra_address_key].save(commit=False)

            # amarra os endereços, atribuindo o OneToOneField
            self.storage[extra_address_key].address = self.storage[key]
            self.storage[extra_address_key].save()

        # indica que o form foi processado uma vez com sucesso
        self.storage['processed_once'] = True

        return super(AddressesPhase, self).form_valid(form)

    def _process_addresses(self, basket):
        for kind in self.address_kinds:
            setattr(basket, "%s_address" % kind, self.storage.get(kind))

    def process(self):
        basket = self.request.basket
        self._process_addresses(basket)
