# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignedcard',
            name='scheduled_interval',
        ),
        migrations.AddField(
            model_name='assignedcard',
            name='scheduled_rep',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assignedcard',
            name='last_shown',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
