# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0003_repintervallog_interval_bucket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repintervallog',
            name='card',
            field=models.ForeignKey(to='cards.Card', null=True),
            preserve_default=True,
        ),
    ]
