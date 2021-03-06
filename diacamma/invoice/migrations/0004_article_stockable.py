# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-15 06:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_bill_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('designation', models.TextField(verbose_name='designation')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'default_permissions': [],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='stockable',
            field=models.IntegerField(choices=[(0, 'no stockable'), (1, 'stockable'), (2, 'stockable & no marketable')], db_index=True, default=0, verbose_name='stockable'),
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(blank=True, to='invoice.Category', verbose_name='categories'),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=50, verbose_name='reference')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Article', verbose_name='article')),
                ('third', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Third', verbose_name='third')),
            ],
            options={
                'verbose_name': 'Provider',
                'default_permissions': [],
                'verbose_name_plural': 'Providers',
            },
        ),
    ]
