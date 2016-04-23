# -*- coding: utf-8 -*-
# This file is part of Shoop Correios.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from registration.backends.simple import views as simple_views
from registration import signals
from registration.forms import RegistrationFormUniqueEmail

from shoop.front.apps.registration.views import RegistrationViewMixin

from shoop_br.models import PersonType, ShoopBRUser, PERSON_TYPE_CHOICES
from shoop_br.forms import PersonInfoForm, CompanyInfoForm
from django import forms

class ShoopBRRegistrationForm(RegistrationFormUniqueEmail):
    person_type = forms.ChoiceField(label=_('Tipo de pessoa'), choices=PERSON_TYPE_CHOICES)

    class Meta:
        model = ShoopBRUser
        fields = ("email", "person_type")

    def clean_person_type(self):
        person_type = self.cleaned_data['person_type']

        # Se for do tipo PersonType, então pega só o valor
        # e não a classe toda...
        if type(person_type) == PersonType:
            return person_type.value

        return person_type

def registration_complete(request):
    messages.success(request, _("Registration complete. Welcome!"))
    return redirect(settings.LOGIN_REDIRECT_URL)

class RegistrationView(RegistrationViewMixin, simple_views.RegistrationView):
    """
    View para registro de usuário contendo mais de um Form.
    Retorna apenas os forms necessários.
    """

    form_class = ShoopBRRegistrationForm
    template_name = "shoop_br/registration/register.jinja"

    def register(self, request, form):
        new_user = form.save()

        # verifica se é uma pessoa fisica ou juridica e cria o registro
        # contendo os dados adicionais conforme o tipo da pessoa
        if new_user.person_type == PersonType.JURIDICA:
            company_info_form = CompanyInfoForm(request.POST, prefix=PersonType.JURIDICA.value)
            company_info = company_info_form.save(commit=False)
            company_info.user = new_user
            company_info.save()
        else:
            person_info_form = PersonInfoForm(request.POST, prefix=PersonType.FISICA.value)
            person_info = person_info_form.save(commit=False)
            person_info.user = new_user
            person_info.save()

        username_field = getattr(new_user, 'USERNAME_FIELD', 'username')
        new_user = authenticate(
            username=getattr(new_user, username_field),
            password=form.cleaned_data['password1']
        )

        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get(self, request, *args, **kwargs):
        # cria os forms adicionais
        person_info_form = PersonInfoForm(prefix=PersonType.FISICA.value)
        company_info_form = CompanyInfoForm(prefix=PersonType.JURIDICA.value)

        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form, 
                                                             person_info_form=person_info_form,
                                                             company_info_form=company_info_form))

    def post(self, request, *args, **kwargs):
        person_info_form = PersonInfoForm(request.POST, prefix=PersonType.FISICA.value)
        company_info_form = CompanyInfoForm(request.POST, prefix=PersonType.JURIDICA.value)

        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
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

            # Pass request to form_valid.
            return self.form_valid(request, form)
        else:
            # valida todos os forms na marra
            person_info_form.is_valid()
            company_info_form.is_valid()

            return self.form_invalid(form, person_info_form, company_info_form)

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

    def registration_allowed(self, request):
        return True
