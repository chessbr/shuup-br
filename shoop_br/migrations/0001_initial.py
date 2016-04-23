# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import shoop_br.models
import enumfields.fields
from django.conf import settings
import shoop.core.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('shoop', '0020_services_and_methods'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoopBRUser',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('email', models.EmailField(verbose_name='email address', error_messages={'unique': 'A user with that email already exists.'}, max_length=254, unique=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('person_type', enumfields.fields.EnumField(verbose_name='Tipo de pessoa', enum=shoop_br.models.PersonType, default='PF', max_length=2)),
                ('groups', models.ManyToManyField(verbose_name='groups', to='auth.Group', related_name='user_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', related_name='user_set', blank=True, help_text='Specific permissions for this user.', related_query_name='user')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Razão social', max_length=80)),
                ('cnpj', models.CharField(verbose_name='CNPJ', validators=[shoop_br.models.validate_cnpj], max_length=18)),
                ('ie', models.CharField(verbose_name='Inscrição estadual', max_length=30, blank=True, null=True)),
                ('im', models.CharField(verbose_name='Inscrição municipal', max_length=30, blank=True, null=True)),
                ('taxation', enumfields.fields.EnumField(verbose_name='Tipo de tributação', enum=shoop_br.models.Taxation, default='e', max_length=1)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('numero', models.CharField(verbose_name='Número', max_length=20)),
                ('cel', models.CharField(verbose_name='Telefone celular', max_length=40, blank=True, null=True)),
                ('ponto_ref', models.CharField(verbose_name='Ponto de referência', max_length=60, blank=True, null=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('numero', models.CharField(verbose_name='Número', max_length=20)),
                ('cel', models.CharField(verbose_name='Telefone celular', max_length=40, blank=True, null=True)),
                ('ponto_ref', models.CharField(verbose_name='Ponto de referência', max_length=60, blank=True, null=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Nome completo', max_length=60)),
                ('cpf', models.CharField(verbose_name='CPF', validators=[shoop_br.models.validate_cpf], max_length=14)),
                ('rg', models.CharField(verbose_name='Identidade', max_length=30)),
                ('birth_date', models.DateField(verbose_name='Data de nascimento')),
                ('gender', enumfields.fields.EnumField(verbose_name='Sexo', enum=shoop.core.models.Gender, default='u', max_length=4)),
                ('user', models.OneToOneField(verbose_name='pessoa_fisica', to=settings.AUTH_USER_MODEL, related_name='pf_person')),
            ],
            options={
                'verbose_name': 'Pessoa física',
                'verbose_name_plural': 'Pessoas físicas',
            },
        ),
    ]
