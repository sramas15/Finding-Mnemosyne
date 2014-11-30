# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20141130_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignedcard',
            name='last_shown',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assignedcard',
            name='scheduled_rep',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
