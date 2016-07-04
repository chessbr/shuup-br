# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import shuup_br.models
import django.utils.timezone
from django.conf import settings
import enumfields.fields
import shuup.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShuupBRUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address', error_messages={'unique': 'A user with that email already exists.'})),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('person_type', enumfields.fields.EnumField(default='PF', max_length=2, verbose_name='Tipo de pessoa', enum=shuup_br.models.PersonType)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='Raz\xe3o social')),
                ('cnpj', models.CharField(max_length=18, verbose_name='CNPJ', validators=[shuup_br.models.validate_cnpj])),
                ('ie', models.CharField(max_length=30, null=True, verbose_name='Inscri\xe7\xe3o estadual', blank=True)),
                ('im', models.CharField(max_length=30, null=True, verbose_name='Inscri\xe7\xe3o municipal', blank=True)),
                ('taxation', enumfields.fields.EnumField(default='e', max_length=1, verbose_name='Tipo de tributa\xe7\xe3o', enum=shuup_br.models.Taxation)),
                ('responsible', models.CharField(max_length=60, verbose_name='Nome do respons\xe1vel')),
                ('user', models.OneToOneField(related_name='pj_person', verbose_name='pessoa juridica', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pessoa jur\xeddica',
                'verbose_name_plural': 'Pessoas jur\xeddicas',
            },
        ),
        migrations.CreateModel(
            name='ExtraImmutableAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=20, verbose_name='N\xfamero')),
                ('cel', models.CharField(max_length=40, null=True, verbose_name='Telefone celular', blank=True)),
                ('ponto_ref', models.CharField(max_length=60, null=True, verbose_name='Ponto de refer\xeancia', blank=True)),
            ],
            options={
                'verbose_name': 'Endere\xe7o imut\xe1vel - Informa\xe7\xe3o extra',
                'verbose_name_plural': 'Endere\xe7os imut\xe1veis - Informa\xe7\xe3o extra',
            },
        ),
        migrations.CreateModel(
            name='ExtraMutableAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=20, verbose_name='N\xfamero')),
                ('cel', models.CharField(max_length=40, null=True, verbose_name='Telefone celular', blank=True)),
                ('ponto_ref', models.CharField(max_length=60, null=True, verbose_name='Ponto de refer\xeancia', blank=True)),
            ],
            options={
                'verbose_name': 'Endere\xe7o mut\xe1vel - Informa\xe7\xe3o extra',
                'verbose_name_plural': 'Endere\xe7os mut\xe1veis - Informa\xe7\xe3o extra',
            },
        ),
        migrations.CreateModel(
            name='PersonInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name='Nome completo')),
                ('cpf', models.CharField(max_length=14, verbose_name='CPF', validators=[shuup_br.models.validate_cpf])),
                ('rg', models.CharField(max_length=30, verbose_name='Identidade')),
                ('birth_date', models.DateField(verbose_name='Data de nascimento')),
                ('gender', enumfields.fields.EnumField(default='u', max_length=4, verbose_name='Sexo', enum=shuup.core.models.Gender)),
                ('user', models.OneToOneField(related_name='pf_person', verbose_name='pessoa_fisica', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pessoa f\xedsica',
                'verbose_name_plural': 'Pessoas f\xedsicas',
            },
        ),
    ]
