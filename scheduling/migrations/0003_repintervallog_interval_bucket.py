# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0002_auto_20141130_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='repintervallog',
            name='interval_bucket',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
