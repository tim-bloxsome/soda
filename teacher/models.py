from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Campus(models.Model):
    campus_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "campuses"
        ordering = ['id']

    def __str__(self):
        return f'{self.campus_name}'


class Course(models.Model):
    course_name = models.CharField(max_length=30)
    course_long_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "courses"
        ordering = ['id']

    def __str__(self):
        return f'{self.course_name}'


class ExamType(models.Model):
    exam_name = models.CharField(max_length=30)
    menu_position = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['menu_position']

    def __str__(self):
        return f'{self.exam_name}'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    exams = models.ManyToManyField('ExamType')

    @receiver(post_save, sender=User)
    def create_user_teacher(sender, instance, created, **kwargs):
        if created:
            Teacher.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_teacher(sender, instance, **kwargs):
        instance.teacher.save()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Student(models.Model):
    stu_num = models.IntegerField(verbose_name='student number')
    last_name = models.CharField(max_length=50, verbose_name='last name')
    first_name = models.CharField(max_length=50, verbose_name='first name')
    dob = models.DateField(blank=True, null=True)
    campus = models.ForeignKey(Campus, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)
    country = models.CharField(blank=True, null=True, max_length=30)
    # don't forget student.get_country_display()
    homework = models.PositiveSmallIntegerField(default=90)
    attendance = models.PositiveSmallIntegerField(default=70)
    attitude = models.PositiveSmallIntegerField(default=50)
    comments = models.TextField(blank=True, null=True)
    previous = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ExamScore(models.Model):
    exam_name = models.CharField(max_length=20)
    reading = models.PositiveSmallIntegerField(blank=True, null=True)
    uofe = models.PositiveSmallIntegerField(blank=True, null=True,
                                            verbose_name='use of English')
    writing = models.DecimalField(blank=True, null=True, max_digits=2, decimal_places=1)
    listening = models.PositiveSmallIntegerField(blank=True, null=True)
    speaking = models.DecimalField(blank=True, null=True, max_digits=2, decimal_places=1)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        ordering = ['student']

    def __str__(self):
        return f'{self.exam_name} - {self.student}'
