# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0005_repintervallog_acq_reps'),
    ]

    operations = [
        migrations.AddField(
            model_name='repintervallog',
            name='timestamp',
            field=models.DateTimeField(default=0),
            preserve_default=False,
        ),
    ]
