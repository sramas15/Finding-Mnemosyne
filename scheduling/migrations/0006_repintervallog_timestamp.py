# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0005_repintervallog_acq_reps'),
    ]

    operations = [
        migrations.AddField(
            model_name='repintervallog',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 3, 0, 22, 43, 188235, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
