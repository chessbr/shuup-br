# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import shuup_br.models
import enumfields.fields
from django.conf import settings
import django.utils.timezone
import shuup.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShuupBRUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(verbose_name='email address', error_messages={'unique': 'A user with that email already exists.'}, max_length=254, unique=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('person_type', enumfields.fields.EnumField(verbose_name='Tipo de pessoa', default='PF', max_length=2, enum=shuup_br.models.PersonType)),
                ('groups', models.ManyToManyField(verbose_name='groups', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', blank=True, related_query_name='user')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', help_text='Specific permissions for this user.', related_name='user_set', blank=True, related_query_name='user')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', shuup_br.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Razão social', max_length=80)),
                ('cnpj', models.CharField(verbose_name='CNPJ', max_length=18, validators=[shuup_br.models.validate_cnpj])),
                ('ie', models.CharField(null=True, verbose_name='Inscrição estadual', blank=True, max_length=30)),
                ('im', models.CharField(null=True, verbose_name='Inscrição municipal', blank=True, max_length=30)),
                ('taxation', enumfields.fields.EnumField(verbose_name='Tipo de tributação', default='e', max_length=1, enum=shuup_br.models.Taxation)),
                ('responsible', models.CharField(verbose_name='Nome do responsável', max_length=60)),
                ('user', models.OneToOneField(verbose_name='pessoa juridica', to=settings.AUTH_USER_MODEL, related_name='pj_person')),
            ],
            options={
                'verbose_name': 'Pessoa jurídica',
                'verbose_name_plural': 'Pessoas jurídicas',
            },
        ),
        migrations.CreateModel(
            name='ExtraImmutableAddress',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('numero', models.CharField(verbose_name='Número', max_length=20)),
                ('cel', models.CharField(null=True, verbose_name='Telefone celular', blank=True, max_length=40)),
                ('ponto_ref', models.CharField(null=True, verbose_name='Ponto de referência', blank=True, max_length=60)),
            ],
            options={
                'verbose_name': 'Endereço imutável - Informação extra',
                'verbose_name_plural': 'Endereços imutáveis - Informação extra',
            },
        ),
        migrations.CreateModel(
            name='ExtraMutableAddress',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('numero', models.CharField(verbose_name='Número', max_length=20)),
                ('cel', models.CharField(null=True, verbose_name='Telefone celular', blank=True, max_length=40)),
                ('ponto_ref', models.CharField(null=True, verbose_name='Ponto de referência', blank=True, max_length=60)),
            ],
            options={
                'verbose_name': 'Endereço mutável - Informação extra',
                'verbose_name_plural': 'Endereços mutáveis - Informação extra',
            },
        ),
        migrations.CreateModel(
            name='PersonInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Nome completo', max_length=60)),
                ('cpf', models.CharField(verbose_name='CPF', max_length=14, validators=[shuup_br.models.validate_cpf])),
                ('rg', models.CharField(verbose_name='Identidade', max_length=30)),
                ('birth_date', models.DateField(verbose_name='Data de nascimento')),
                ('gender', enumfields.fields.EnumField(verbose_name='Sexo', default='u', max_length=4, enum=shuup.core.models.Gender)),
                ('user', models.OneToOneField(verbose_name='pessoa_fisica', to=settings.AUTH_USER_MODEL, related_name='pf_person')),
            ],
            options={
                'verbose_name': 'Pessoa física',
                'verbose_name_plural': 'Pessoas físicas',
            },
        ),
    ]
