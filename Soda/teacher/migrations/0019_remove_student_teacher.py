# Generated by Django 2.1.5 on 2019-02-07 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0018_auto_20190207_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='teacher',
        ),
    ]
