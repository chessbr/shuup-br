# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoop', '0020_services_and_methods'),
        ('shoop_br', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraimmutableaddress',
            name='address',
            field=models.OneToOneField(related_name='extra', default=None, to='shoop.ImmutableAddress'),
        ),
        migrations.AddField(
            model_name='extramutableaddress',
            name='address',
            field=models.OneToOneField(related_name='extra', default=None, to='shoop.MutableAddress'),
        ),
    ]
