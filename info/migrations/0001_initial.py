# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-03 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bugs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(db_index=True, max_length=100, verbose_name='Term')),
                ('freq', models.SmallIntegerField(default=0)),
                ('bug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugs.BugReport')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='frequency',
            unique_together=set([('bug', 'term')]),
        ),
    ]
