# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import absolute_import

from registration import signals
from registration.forms import RegistrationFormUniqueEmail
from registration.views import RegistrationView

from shuup_br.forms import CompanyInfoForm, PersonInfoForm
from shuup_br.models import PERSON_TYPE_CHOICES, PersonType, ShuupBRUser

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from shuup.front.apps.registration.views import RegistrationViewMixin


class ShuupBRRegistrationForm(RegistrationFormUniqueEmail):
    person_type = forms.ChoiceField(label=_('Tipo de pessoa'), choices=PERSON_TYPE_CHOICES)

    class Meta:
        model = ShuupBRUser
        fields = ("email", "person_type")

    def clean_person_type(self):
        person_type = self.cleaned_data['person_type']

        # Se for do tipo PersonType, então pega só o valor
        # e não a classe toda...
        if type(person_type) == PersonType:
            return person_type.value

        return person_type


def registration_complete(request):
    messages.success(request, _("Registration completed. Welcome!"))
    return redirect(settings.LOGIN_REDIRECT_URL)


class RegistrationView(RegistrationViewMixin, RegistrationView):
    """
    View para registro de usuário contendo mais de um Form.
    Retorna apenas os forms necessários.
    """

    form_class = ShuupBRRegistrationForm
    template_name = "shuup_br/registration/register.jinja"

    def register(self, form):
        new_user = form.save()

        # verifica se é uma pessoa fisica ou juridica e cria o registro
        # contendo os dados adicionais conforme o tipo da pessoa
        if new_user.person_type == PersonType.JURIDICA:
            company_info_form = CompanyInfoForm(self.request.POST,
                                                prefix=PersonType.JURIDICA.value)
            company_info = company_info_form.save(commit=False)
            company_info.user = new_user
            company_info.save()
        else:
            person_info_form = PersonInfoForm(self.request.POST,
                                              prefix=PersonType.FISICA.value)
            person_info = person_info_form.save(commit=False)
            person_info.user = new_user
            person_info.save()

        username_field = getattr(new_user, 'USERNAME_FIELD', 'username')
        new_user = authenticate(
            username=getattr(new_user, username_field),
            password=form.cleaned_data['password1']
        )

        login(self.request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user

    def get(self, request, *args, **kwargs):
        # cria os forms adicionais
        person_info_form = PersonInfoForm(prefix=PersonType.FISICA.value)
        company_info_form = CompanyInfoForm(prefix=PersonType.JURIDICA.value)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form,
                                                             person_info_form=person_info_form,
                                                             company_info_form=company_info_form))

    def post(self, request, *args, **kwargs):
        person_info_form = PersonInfoForm(request.POST, prefix=PersonType.FISICA.value)
        company_info_form = CompanyInfoForm(request.POST, prefix=PersonType.JURIDICA.value)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            person_type = form.cleaned_data['person_type']

            if person_type == PersonType.JURIDICA.value:
                person_info_form = PersonInfoForm(prefix=PersonType.FISICA.value)
                company_info_form = CompanyInfoForm(request.POST, prefix=PersonType.JURIDICA.value)

                if not company_info_form.is_valid():
                    return self.form_invalid(form, person_info_form, company_info_form)

            else:
                person_info_form = PersonInfoForm(request.POST, prefix=PersonType.FISICA.value)
                company_info_form = CompanyInfoForm(prefix=PersonType.JURIDICA.value)

                if not person_info_form.is_valid():
                    return self.form_invalid(form, person_info_form, company_info_form)

            return self.form_valid(form)
        else:
            # valida todos os forms na marra
            person_info_form.is_valid()
            company_info_form.is_valid()

            return self.form_invalid(form,
                                     person_info_form=person_info_form,
                                     company_info_form=company_info_form)

    def form_invalid(self, form, person_info_form=None, company_info_form=None):
        return self.render_to_response(self.get_context_data(form=form,
                                                             person_info_form=person_info_form,
                                                             company_info_form=company_info_form))

    def get_context_data(self, **kwargs):
        # util para utilizar os valores do ENUM no template
        kwargs['PersonType'] = PersonType

        # sempre deve ter os formulários com as informações
        # da pessoa se não for informado anteriormente
        if not kwargs.get('person_info_form'):
            kwargs['person_info_form'] = PersonInfoForm(prefix=PersonType.FISICA.value)

        if not kwargs.get('company_info_form'):
            kwargs['company_info_form'] = CompanyInfoForm(prefix=PersonType.JURIDICA.value)

        return super(RegistrationView, self).get_context_data(**kwargs)

    def registration_allowed(self):
        return True
