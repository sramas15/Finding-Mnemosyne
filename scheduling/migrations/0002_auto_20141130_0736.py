# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regressionweights',
            name='interval',
        ),
        migrations.AddField(
            model_name='regressionweights',
            name='intercept',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
