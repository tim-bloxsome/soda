# Generated by Django 2.1.5 on 2019-02-07 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0022_auto_20190207_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher'),
            preserve_default=False,
        ),
    ]
