# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ablum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('starName', models.CharField(max_length=50)),
                ('starID', models.IntegerField()),
                ('picUrl', models.TextField()),
                ('tag', models.CharField(max_length=50)),
                ('pictureCnt', models.IntegerField()),
                ('publishDate', models.DateField()),
                ('cover', models.URLField()),
                ('des', models.TextField()),
                ('company', models.CharField(max_length=30)),
                ('termID', models.PositiveIntegerField()),
                ('lastModified', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='star',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('birthday', models.CharField(max_length=20)),
                ('threeD', models.CharField(max_length=15)),
                ('hobby', models.CharField(max_length=40)),
                ('wordPlace', models.CharField(max_length=15)),
                ('ablumID', models.CharField(max_length=300)),
                ('des', models.TextField()),
                ('tag', models.CharField(max_length=50)),
                ('cover', models.URLField()),
            ],
        ),
    ]