from django.contrib import admin
from import_export import resources
from .models import Student, ExamScore, Teacher, ExamType, Campus, Course
from .forms import TeacherForm
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

# admin.site.register(Student)
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


class StudentResource(resources.ModelResource):
    # stu_num = Field(attribute='stu_num', column_name='Student No')
    # last_name = Field(attribute='last_name', column_name='Last Name')

    class Meta:
        model = Student
        import_id_fields = ('stu_num',)
        fields = (
            'stu_num',
            'last_name',
            'first_name',
            'campus',
            'course',
            'teacher',
            'country',
        )
        exclude = (
            'dob',
            'homework',
            'attendance',
            'attitude',
            'comments',
            'previous',
        )


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
