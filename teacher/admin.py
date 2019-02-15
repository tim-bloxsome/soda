from django.contrib import admin
from import_export import resources
from .models import Student, ExamScore, Teacher, ExamType, Campus, Course
from .forms import TeacherForm, RegistrationForm
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.site_header = 'Soda Admin'
admin.site.index_title = 'Soda Administration'
admin.site.site_title = 'Soda'


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


class ExamScoreResource(resources.ModelResource):

    class Meta:
        model = ExamScore
        fields = (
            'exam_name',
            'reading',
            'uofe',
            'writing',
            'listening',
            'speaking',
            'student',
        )


@admin.register(ExamScore)
class ExamScoreAdmin(ImportExportModelAdmin):
    resource_class = ExamScoreResource
    list_display = ('__str__', 'exam_name')
    search_fields = ['exam_name', 'student__first_name', 'student__last_name']


class UserAdmin(UserAdmin):
    add_form = RegistrationForm
    prepopulated_fields = {'username': ('first_name', 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'is_superuser',),
        }),
    )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
