# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegressionWeights',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.FloatField()),
                ('new_grade', models.FloatField()),
                ('easiness', models.FloatField()),
                ('ret_reps', models.FloatField()),
                ('ret_reps_since_lapse', models.FloatField()),
                ('lapses', models.FloatField()),
                ('interval', models.FloatField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepIntervalLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.SmallIntegerField()),
                ('new_grade', models.SmallIntegerField()),
                ('easiness', models.FloatField()),
                ('ret_reps', models.IntegerField()),
                ('ret_reps_since_lapse', models.IntegerField()),
                ('lapses', models.IntegerField()),
                ('interval', models.IntegerField()),
                ('card', models.ForeignKey(to='cards.Card')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
