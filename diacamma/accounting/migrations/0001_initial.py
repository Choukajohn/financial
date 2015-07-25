# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
'''
Initial django functions

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2015 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models, migrations
from lucterios.CORE.models import Parameter
from diacamma.accounting.models import Journal
from django.db.models.deletion import PROTECT

def initial_values(*args):
    # pylint: disable=unused-argument, no-member, expression-not-assigned
    param = Parameter.objects.create(name='accounting-devise', typeparam=0)  # pylint: disable=no-member
    param.title = _("accounting-devise")
    param.args = "{'Multi':False}"
    param.value = '€'
    param.save()

    param = Parameter.objects.create(name='accounting-devise-iso', typeparam=0)  # pylint: disable=no-member
    param.title = _("accounting-devise-iso")
    param.args = "{'Multi':False}"
    param.value = 'EUR'
    param.save()

    param = Parameter.objects.create(name='accounting-devise-prec', typeparam=1)  # pylint: disable=no-member
    param.title = _("accounting-devise-prec")
    param.args = "{'Min':0, 'Max':4}"
    param.value = '2'
    param.save()

    Journal.objects.create(name=_("Last year report"))
    Journal.objects.create(name=_("Buying"))
    Journal.objects.create(name=_("Selling"))
    Journal.objects.create(name=_("Payment"))
    Journal.objects.create(name=_("Other"))

class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountThird',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=50, verbose_name='code')),
            ],
            options={
                'verbose_name': 'account',
                'default_permissions': [],
                'verbose_name_plural': 'accounts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Third',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(choices=[(0, 'Enable'), (1, 'Disable')], verbose_name='status')),
                ('contact', models.ForeignKey(verbose_name='contact', to='contacts.AbstractContact')),
            ],
            options={
                'verbose_name': 'third',
                'verbose_name_plural': 'thirds',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='accountthird',
            name='third',
            field=models.ForeignKey(verbose_name='third', to='accounting.Third'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='FiscalYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('begin', models.DateField(verbose_name='begin')),
                ('end', models.DateField(verbose_name='end')),
                ('status', models.IntegerField(verbose_name='status', choices=[(0, 'building'), (1, 'running'), (2, 'finished')], default=0)),
                ('is_actif', models.BooleanField(verbose_name='actif', default=False)),
                ('last_fiscalyear', models.ForeignKey(to='accounting.FiscalYear', verbose_name='last fiscal year', null=True)),
            ],
            options={
                'verbose_name_plural': 'fiscal years',
                'verbose_name': 'fiscal year',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChartsAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(verbose_name='code', max_length=50)),
                ('name', models.CharField(verbose_name='name', max_length=200)),
                ('type_of_account', models.IntegerField(verbose_name='type of account', \
                    choices=[(0, 'Asset'), (1, 'Liability'), (2, 'Equity'), (3, 'Revenue'), (4, 'Expense'), (5, 'Contra-accounts')], null=True)),
                ('year', models.ForeignKey(verbose_name='fiscal year', to='accounting.FiscalYear')),
            ],
            options={
                'verbose_name': 'charts of account',
                'verbose_name_plural': 'charts of accounts',
                'ordering': ['year', 'code']
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name', unique=True)),
            ],
            options={
                'default_permissions': [],
                'verbose_name': 'accounting journal',
                'verbose_name_plural': 'accounting journals',
            },
        ),
        migrations.CreateModel(
            name='EntryAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('num', models.IntegerField(verbose_name='numeros', null=True)),
                ('journal', models.ForeignKey(verbose_name='journal', to='accounting.Journal', default=0, on_delete=PROTECT)),
                ('date_entry', models.DateField(verbose_name='date entry', null=True)),
                ('date_value', models.DateField(verbose_name='date value', null=True)),
                ('designation', models.CharField(verbose_name='name', max_length=200)),
                ('close', models.BooleanField(verbose_name='close', default=False)),
                ('year', models.ForeignKey(verbose_name='fiscal year', to='accounting.FiscalYear')),
            ],
            options={
                'verbose_name': 'entry of account',
                'verbose_name_plural': 'entries of account',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryLineAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('amount', models.FloatField(verbose_name='amount')),
                ('reference', models.CharField(verbose_name='reference', max_length=100, null=True)),
                ('account', models.ForeignKey(verbose_name='account', to='accounting.ChartsAccount')),
                ('entry', models.ForeignKey(verbose_name='entry', to='accounting.EntryAccount')),
                ('third', models.ForeignKey(null=True, verbose_name='third', to='accounting.Third')),
            ],
            options={
                'default_permissions': [],
                'verbose_name': 'entry line of account',
                'verbose_name_plural': 'entry lines of account',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(initial_values),
    ]
