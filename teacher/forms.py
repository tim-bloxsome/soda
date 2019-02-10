from django import forms
from .models import Student, ExamScore, ExamType, Teacher, Campus
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe


class TeacherForm(forms.ModelForm):
    exams = forms.ModelMultipleChoiceField(
        queryset=ExamType.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Teacher
        fields = (
            'user',
            'campus',
            'course',
            'exams'
        )


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={
            'placeholder': mark_safe('Username'),  # mark_safe('&#xf007 Username')
            'class': 'form-control'}))
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'placeholder': mark_safe('Password'),  # mark_safe('&#xf084 Password')
            'class': 'form-control'}))

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields are case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = (
            'stu_num',
            'last_name',
            'first_name',
            'dob',
            'campus',
            'course',
            'teacher',
            'country',
            'homework',
            'attendance',
            'attitude',
            'comments',
            'previous'
        )


class ExamScoreForm(forms.ModelForm):
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

# class NewPreTestForm(forms.ModelForm):
#     class Meta:
#         model = PreTestPrac
#         fields = ['reading', 'uofe', 'writing', 'listening', 'speaking', 'student']
#         widgets = {
#             'reading': forms.NumberInput(attrs={
#                                    'class': 'score',
#                                    'placeholder': '36',
#                                    'id': 'score-re',
#             }),
#             'uofe': forms.NumberInput(attrs={
#                                    'class': 'score',
#                                    'placeholder': '36',
#                                    'id': 'score-us'
#             }),
#             'writing': forms.NumberInput(attrs={
#                                    'class': 'score',
#                                    'placeholder': '5',
#                                    'id': 'score-wr'
#             }),
#             'listening': forms.NumberInput(attrs={
#                                    'class': 'score',
#                                    'placeholder': '30',
#                                    'id': 'score-li'
#             }),
#             'speaking': forms.NumberInput(attrs={
#                                    'class': 'score',
#                                    'placeholder': '5',
#                                    'id': 'score-sp'
#             }),
#             'student': forms.HiddenInput(attrs={
#                                    'id': 'student-id'})
#         }
# # value="{{ student.id }}
# # 'autofocus': True}
