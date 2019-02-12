# Generated by Django 2.1.2 on 2019-02-12 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0032_course_course_long_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examscore',
            name='listening',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examscore',
            name='reading',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examscore',
            name='speaking',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='examscore',
            name='uofe',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='use of English'),
        ),
        migrations.AlterField(
            model_name='examscore',
            name='writing',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='country',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
