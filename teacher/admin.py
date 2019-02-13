from django.contrib import admin
from import_export import resources
from .models import Student, ExamScore, Teacher, ExamType, Campus, Course
from .forms import TeacherForm
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field


admin.site.site_header = 'Soda Admin'
admin.site.index_title = 'Soda Administration'
admin.site.site_title = 'Soda'


@admin.register(ExamScore)
class ExamScoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'exam_name')
    search_fields = ['exam_name', 'student__first_name', 'student__last_name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'id')
    readonly_fields = ('id',)


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('campus_name', 'id')
    readonly_fields = ('id',)


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'menu_position')
    list_editable = ('menu_position',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
    list_display = ('__str__', 'id')
    readonly_fields = ('id',)


class StudentResource(resources.ModelResource):

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
    list_display = ('__str__', 'course', 'teacher')
    search_fields = ['first_name', 'last_name']
