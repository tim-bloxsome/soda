from django.contrib import admin
from .models import Student, ExamScore, Teacher, ExamType, Campus, Course
from .forms import TeacherForm

admin.site.register(Student)
admin.site.register(Campus)
admin.site.register(ExamScore)
admin.site.register(Course)


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'menu_position')
    list_editable = ('menu_position',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
