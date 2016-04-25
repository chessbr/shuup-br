# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import shoop.core.models
import django.utils.timezone
import shoop_br.models
import enumfields.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('shoop', '0020_services_and_methods'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoopBRUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address', error_messages={'unique': 'A user with that email already exists.'})),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('person_type', enumfields.fields.EnumField(default='PF', max_length=2, enum=shoop_br.models.PersonType, verbose_name='Tipo de pessoa')),
                ('groups', models.ManyToManyField(verbose_name='groups', related_query_name='user', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', blank=True)),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', related_query_name='user', to='auth.Permission', help_text='Specific permissions for this user.', related_name='user_set', blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', shoop_br.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=80, verbose_name='Razão social')),
                ('cnpj', models.CharField(max_length=18, validators=[shoop_br.models.validate_cnpj], verbose_name='CNPJ')),
                ('ie', models.CharField(max_length=30, null=True, verbose_name='Inscrição estadual', blank=True)),
                ('im', models.CharField(max_length=30, null=True, verbose_name='Inscrição municipal', blank=True)),
                ('taxation', enumfields.fields.EnumField(default='e', max_length=1, enum=shoop_br.models.Taxation, verbose_name='Tipo de tributação')),
                ('responsible', models.CharField(max_length=60, verbose_name='Nome do responsável')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('numero', models.CharField(max_length=20, verbose_name='Número')),
                ('cel', models.CharField(max_length=40, null=True, verbose_name='Telefone celular', blank=True)),
                ('ponto_ref', models.CharField(max_length=60, null=True, verbose_name='Ponto de referência', blank=True)),
                ('address', models.OneToOneField(to='shoop.ImmutableAddress', related_name='extra')),
            ],
            options={
                'verbose_name': 'Endereço imutável - Informação extra',
                'verbose_name_plural': 'Endereços imutáveis - Informação extra',
            },
        ),
        migrations.CreateModel(
            name='ExtraMutableAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('numero', models.CharField(max_length=20, verbose_name='Número')),
                ('cel', models.CharField(max_length=40, null=True, verbose_name='Telefone celular', blank=True)),
                ('ponto_ref', models.CharField(max_length=60, null=True, verbose_name='Ponto de referência', blank=True)),
                ('address', models.OneToOneField(to='shoop.MutableAddress', related_name='extra')),
            ],
            options={
                'verbose_name': 'Endereço mutável - Informação extra',
                'verbose_name_plural': 'Endereços mutáveis - Informação extra',
            },
        ),
        migrations.CreateModel(
            name='PersonInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=60, verbose_name='Nome completo')),
                ('cpf', models.CharField(max_length=14, validators=[shoop_br.models.validate_cpf], verbose_name='CPF')),
                ('rg', models.CharField(max_length=30, verbose_name='Identidade')),
                ('birth_date', models.DateField(verbose_name='Data de nascimento')),
                ('gender', enumfields.fields.EnumField(default='u', max_length=4, enum=shoop.core.models.Gender, verbose_name='Sexo')),
                ('user', models.OneToOneField(verbose_name='pessoa_fisica', to=settings.AUTH_USER_MODEL, related_name='pf_person')),
            ],
            options={
                'verbose_name': 'Pessoa física',
                'verbose_name_plural': 'Pessoas físicas',
            },
        ),
    ]
