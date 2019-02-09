# Generated by Django 2.1.5 on 2019-01-05 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(max_length=20)),
                ('reading', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('uofe', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='use of English')),
                ('writing', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('listening', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('speaking', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'ordering': ['student'],
            },
        ),
        migrations.CreateModel(
            name='ExamType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(max_length=30)),
                ('menu_position', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['menu_position'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_num', models.IntegerField(verbose_name='student number')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('dob', models.DateField(blank=True, null=True)),
                ('campus', models.CharField(blank=True, max_length=30)),
                ('course', models.CharField(max_length=25)),
                ('teacher', models.CharField(max_length=50)),
                ('country', models.CharField(choices=[('ch', 'Switzerland'), ('br', 'Brazil'), ('es', 'Spain'), ('de', 'Germany'), ('fr', 'France'), ('kr', 'South Korea')], max_length=2)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus', models.CharField(blank=True, max_length=30)),
                ('level', models.CharField(blank=True, max_length=30)),
                ('exams', models.ManyToManyField(to='teacher.ExamType')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.AddField(
            model_name='examscore',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Student'),
        ),
    ]
