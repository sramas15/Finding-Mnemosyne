# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0004_auto_20141130_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='repintervallog',
            name='acq_reps',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
