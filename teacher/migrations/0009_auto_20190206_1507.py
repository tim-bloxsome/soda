# Generated by Django 2.1.5 on 2019-02-06 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0008_auto_20190202_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus_name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['campus_name'],
            },
        ),
        migrations.AlterField(
            model_name='teacher',
            name='campus',
            field=models.CharField(max_length=30),
        ),
    ]