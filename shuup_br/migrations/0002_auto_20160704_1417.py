# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuup', '0001_initial'),
        ('shuup_br', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraimmutableaddress',
            name='address',
            field=models.OneToOneField(related_name='extra', default=None, to='shuup.ImmutableAddress'),
        ),
        migrations.AddField(
            model_name='extramutableaddress',
            name='address',
            field=models.OneToOneField(related_name='extra', default=None, to='shuup.MutableAddress'),
        ),
    ]
