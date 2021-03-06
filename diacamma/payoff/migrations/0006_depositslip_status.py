# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-07-01 17:09
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('payoff', '0005_payoffbankfee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositslip',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, 'building'), (1, 'closed'), (2, 'valid')], db_index=True, default=0, verbose_name='status'),
        ),
    ]
