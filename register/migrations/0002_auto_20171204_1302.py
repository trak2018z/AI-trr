# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 13:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('city_name', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('region_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('street_name', models.CharField(max_length=80)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.City')),
            ],
        ),
        migrations.RenameField(
            model_name='building',
            old_name='address',
            new_name='number',
        ),
        migrations.RemoveField(
            model_name='building',
            name='city',
        ),
        migrations.AddField(
            model_name='building',
            name='owner_registered',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='register.User'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='description',
            field=models.CharField(max_length=500),
        ),
        migrations.AddField(
            model_name='region',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.State'),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Region'),
        ),
        migrations.AddField(
            model_name='building',
            name='street',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='register.Region'),
        ),
        migrations.AddField(
            model_name='user',
            name='region',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='register.Region'),
        ),
    ]