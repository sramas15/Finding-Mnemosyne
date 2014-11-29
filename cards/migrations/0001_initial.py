# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_shown', models.DateField(auto_now=True)),
                ('last_grade', models.SmallIntegerField(default=0)),
                ('easiness', models.FloatField(default=2.5)),
                ('ret_reps', models.IntegerField(default=0)),
                ('ret_reps_since_lapse', models.IntegerField(default=0)),
                ('lapses', models.IntegerField(default=0)),
                ('scheduled_interval', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200)),
                ('answer', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='card',
            name='card_set',
            field=models.ForeignKey(to='cards.CardSet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedcard',
            name='card',
            field=models.ForeignKey(to='cards.Card'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedcard',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
