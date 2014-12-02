# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20141130_0207'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedcard',
            name='acq_reps',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
