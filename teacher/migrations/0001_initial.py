# Generated by Django 2.1.7 on 2019-02-15 23:16

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
            name='Campus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus_name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'campuses',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=30)),
                ('course_long_name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'courses',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ExamScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(max_length=20)),
                ('reading', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('uofe', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='use of English')),
                ('writing', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('listening', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('speaking', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
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
                ('country', models.CharField(blank=True, max_length=30, null=True)),
                ('homework', models.PositiveSmallIntegerField(default=90)),
                ('attendance', models.PositiveSmallIntegerField(default=70)),
                ('attitude', models.PositiveSmallIntegerField(default=50)),
                ('comments', models.TextField(blank=True, default='', null=True)),
                ('previous', models.TextField(blank=True, default='', null=True)),
                ('campus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher.Campus')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher.Course')),
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
                ('campus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher.Campus')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher.Course')),
                ('exams', models.ManyToManyField(to='teacher.ExamType')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher.Teacher'),
        ),
        migrations.AddField(
            model_name='examscore',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Student'),
        ),
    ]
