from django import forms
from .models import Student, ExamScore, ExamType, Teacher, Campus
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()

                return User
