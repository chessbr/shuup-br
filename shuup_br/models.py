# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import unicode_literals

from enumfields import Enum, EnumField

from shuup_br.base import CNPJ, CPF

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from shuup.core.models._addresses import ImmutableAddress, MutableAddress
from shuup.core.models._contacts import Gender


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


class PersonType(Enum):
    FISICA = 'PF'
    JURIDICA = 'PJ'

    class Labels:
        FISICA = _("Pessoa física")
        JURIDICA = _("Pessoa jurídica")


PERSON_TYPE_CHOICES = (
    (PersonType.FISICA.value, PersonType.FISICA.label),
    (PersonType.JURIDICA.value, PersonType.JURIDICA.label),
)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff,
                     is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class ShuupBRUser(AbstractBaseUser, PermissionsMixin):
    """
    An user witch username is the email itself
    """

    email = models.EmailField(_('email address'),
                              blank=False,
                              unique=True,
                              error_messages={
                                  'unique': _("A user with that email already exists."),
                              })

    is_staff = models.BooleanField(_('staff status'),
                                   default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    person_type = EnumField(PersonType,
                            default=PersonType.FISICA,
                            max_length=2,
                            verbose_name=_('Tipo de pessoa'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        if self.person_type == PersonType.FISICA:
            if hasattr(self, 'pf_person'):
                return self.pf_person.name
        else:
            if hasattr(self, 'pj_person'):
                return self.pj_person.name

        return self.email.strip()

    def get_short_name(self):
        return self.get_full_name()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Taxation(Enum):
    ICMS = 'i'
    ISENTO = 'e'
    NAO_CONTRIBUINTE = 'n'

    class Labels:
        ICMS = _("ICMS")
        ISENTO = _("Isento")
        NAO_CONTRIBUINTE = _("Não contribuinte")


def validate_cpf(value):
    """ Validador de CPF para models """
    if not CPF.validate(value):
        raise ValidationError(
            _('%(value)s is not a valid CPF'),
            params={'value': value},
        )


def validate_cnpj(value):
    """ Validador de CNPJ para models """
    if not CNPJ.validate(value):
        raise ValidationError(
            _('%(value)s is not a valid CNPJ'),
            params={'value': value},
        )


class PersonInfo(models.Model):
    """ Pessoa física """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='pf_person',
                                verbose_name=_('pessoa_fisica'))
    name = models.CharField(verbose_name=_("Nome completo"), max_length=60)
    cpf = models.CharField(verbose_name=_("CPF"), max_length=14, validators=[validate_cpf])
    rg = models.CharField(verbose_name=_("Identidade"), max_length=30)
    birth_date = models.DateField(verbose_name=_('Data de nascimento'))
    gender = EnumField(Gender, default=Gender.UNDISCLOSED, max_length=4, verbose_name=_('Sexo'))

    class Meta:
        verbose_name = _('Pessoa física')
        verbose_name_plural = _('Pessoas físicas')

    def __str__(self):
        return "Pessoa fisica: {0}".format(self.name)

    def clean(self):
        self.cpf = "".join([d for d in self.cpf if d.isdigit()])


class CompanyInfo(models.Model):
    """ Pessoa jurídica """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='pj_person',
                                verbose_name=_('pessoa juridica'))

    # pessoa jurídica
    name = models.CharField(verbose_name=_("Razão social"), max_length=80)
    cnpj = models.CharField(verbose_name=_("CNPJ"), max_length=18, validators=[validate_cnpj])
    ie = models.CharField(verbose_name=_("Inscrição estadual"), max_length=30, blank=True, null=True)
    im = models.CharField(verbose_name=_("Inscrição municipal"), max_length=30, blank=True, null=True)
    taxation = EnumField(Taxation, default=Taxation.ISENTO, max_length=1, verbose_name=_('Tipo de tributação'))
    responsible = models.CharField(verbose_name=_("Nome do responsável"), max_length=60)

    class Meta:
        verbose_name = _('Pessoa jurídica')
        verbose_name_plural = _('Pessoas jurídicas')

    def __str__(self):
        return "Pessoa juridica: {0}".format(self.name)

    def clean(self):
        self.cnpj = "".join([d for d in self.cnpj if d.isdigit()])


class ExtraAddress(models.Model):
    """ Dados adicionais para modelos Address do Shuup """
    numero = models.CharField(verbose_name=_("Número"), max_length=20)
    cel = models.CharField(verbose_name=_("Telefone celular"), max_length=40, blank=True, null=True)
    ponto_ref = models.CharField(verbose_name=_("Ponto de referência"), max_length=60, blank=True, null=True)

    class Meta:
        abstract = True


class ExtraMutableAddress(ExtraAddress):
    """ Dados adicionais para modelos MutableAddress do Shuup """
    address = models.OneToOneField(MutableAddress, related_name="extra", default=None)

    class Meta:
        verbose_name = _('Endereço mutável - Informação extra')
        verbose_name_plural = _('Endereços mutáveis - Informação extra')

    def __str__(self):
        return "Extra mutable address information for {0}".format(getattr(self, 'address', None))

    def to_immutable(self):
        """
        Create saved ExtraImmutableAddress from self.

        :rtype: ExtraImmutableAddress
        :return: Saved ExtraImmutableAddress with same data as self.
        """
        return ExtraImmutableAddress.from_data({
            'numero': self.numero,
            'cel': self.cel,
            'ponto_ref': self.ponto_ref
        })

    @classmethod
    def from_data(cls, data):
        """
        Construct mutable address from a data dictionary.

        :param data: data for address
        :type data: dict[str,str]
        :return: Unsaved extra mutable address
        :rtype: ExtraMutableAddress
        """
        return cls(**data)


class ExtraImmutableAddress(ExtraAddress):
    """ Dados adicionais para modelos ImmutableAddres do Shuup """
    address = models.OneToOneField(ImmutableAddress, related_name="extra", default=None)

    class Meta:
        verbose_name = _('Endereço imutável - Informação extra')
        verbose_name_plural = _('Endereços imutáveis - Informação extra')

    def __str__(self):
        return "Extra immutable address information for {0}".format(getattr(self, 'address', None))

    @classmethod
    def from_data(cls, data):
        """
        Create extra immutable address with given data.

        :param data: data for extra address
        :type data: dict[str,str]
        :return: Saved extra immutable address
        :rtype: ExtraImmutableAddress
        """
        # Populate all known address fields even if not originally in `data`
        return cls(**data)
