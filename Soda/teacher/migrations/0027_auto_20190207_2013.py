# Generated by Django 2.1.5 on 2019-02-07 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0026_auto_20190207_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='attendance',
            field=models.PositiveSmallIntegerField(default=70),
        ),
        migrations.AlterField(
            model_name='student',
            name='attitude',
            field=models.PositiveSmallIntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='homework',
            field=models.PositiveSmallIntegerField(default=90),
        ),
    ]
