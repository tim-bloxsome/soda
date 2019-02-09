# Generated by Django 2.1.5 on 2019-01-24 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0006_auto_20190120_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='attendence',
            field=models.PositiveSmallIntegerField(default=6),
        ),
        migrations.AlterField(
            model_name='student',
            name='attitude',
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='homework',
            field=models.PositiveSmallIntegerField(default=7),
        ),
    ]
