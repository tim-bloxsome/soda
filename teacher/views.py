import os
import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.conf import settings
from django.views.generic import DetailView

from xhtml2pdf import pisa
from tablib import Dataset
from import_export import resources


from teacher.forms import StudentForm, CustomAuthForm, ExamScoreForm
from teacher.models import Student, ExamType, ExamScore, Teacher, Campus
import teacher.descriptors as des
from teacher.admin import StudentResource


"""

TODO Need a link to change forgotten passwords
TODO CSV export for exam scores
TODO change model to correct decimal inputs
TODO slider input only on handle
TODO admin customisations

"""


def csv_upload(request):
    if request.method == 'POST':
        student_resource = StudentResource()
        # dataset = Dataset()
        new_students = request.FILES['myfile']
        dataset = Dataset().load(new_students.read())
        result = student_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            student_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'teacher/csv_upload.html')


@login_required
def StudentDetail(request, username, pk):
    student_pk = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student_pk)
        if form.is_valid():
            form.save()
            # this means we won't rePOST data in form i.e. no unwanted resubmit
            # return redirect('student-detail')
            return HttpResponse("")
        else:
            print(form.errors)
    else:
        form = StudentForm(instance=student_pk)

    context = {'form': form, 'student': student_pk}

    return render(request, 'teacher/student_detail.html', context)


def u_or_c_exam(request, id):
    studentid = get_object_or_404(Student, id=id)
    if request.method == "POST":
        form = ExamScoreForm(request.POST, instance=studentid)
        if form.is_valid():
            exam_name = form.cleaned_data.get('exam_name')
            reading = form.cleaned_data.get('reading')
            uofe = form.cleaned_data.get('uofe')
            writing = form.cleaned_data.get('writing')
            listening = form.cleaned_data.get('listening')
            speaking = form.cleaned_data.get('speaking')
            student_obj = form.cleaned_data.get('student')
            student = Student.objects.get(id=student_obj.id)

            ExamScore.objects.update_or_create(
                # filtering by these two keyword arguments
                student=student,
                exam_name=exam_name,
                defaults={
                    'exam_name': exam_name,
                    'reading': reading,
                    'uofe': uofe,
                    'writing': writing,
                    'listening': listening,
                    'speaking': speaking
                }
            )
            return HttpResponse("")
        else:
            print(form.errors)


@login_required
def reports(request, username):
    return render(request, 'teacher/reports.html')


@login_required
def exam_scores(request, username, exam_name):
    context = {'exam_name': exam_name}
    return render(request, 'teacher/scores.html', context)


class CustomLoginView(LoginView):
    """returns a url specific to the user"""
    def get_success_url(self):
        return reverse('teacher-home', args=[self.request.user.username])


@login_required
def home(request):
    return render(request, 'teacher/teacher_home.html')


@login_required
def teacher_home(request, username):
    # user = request.user.id
    # if Teacher.objects.filter(user__id=user).exists():
    #     teacher = Teacher.objects.get(user__id=user)
    # context = {'teacher': teacher}
    return render(request, 'teacher/teacher_home.html')


def happyland(request):
    return render(request, 'teacher/happyland.html')


def error(request):
    return render(request, 'teacher/error.html')


def render_midpdf_view(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if ExamScore.objects.filter(student_id=pk, exam_name='PreCourse').exists():
        precourse = ExamScore.objects.get(student_id=pk, exam_name='PreCourse')
    else:
        precourse = ""
    if ExamScore.objects.filter(student_id=pk, exam_name='MidCourse').exists():
        midcourse = ExamScore.objects.get(student_id=pk, exam_name='MidCourse')
    else:
        midcourse = ""
    if ExamScore.objects.filter(student_id=pk, exam_name='EndCourse').exists():
        endcourse = ExamScore.objects.get(student_id=pk, exam_name='EndCourse')
    else:
        endcourse = ""

    if midcourse != "":
        uofe_perc = round((midcourse.uofe / 36) * 100, 0)
        reading_perc = round((midcourse.reading / 36) * 100, 0)
        listening_perc = round((midcourse.listening / 30) * 100, 0)
        speaking_perc = round((midcourse.speaking / 5) * 100, 0)
        writing_perc = round((midcourse.writing / 5) * 100, 0)
        total_perc = round((uofe_perc + reading_perc + listening_perc + speaking_perc + writing_perc) / 5, 0)
    else:
        uofe_perc = 0
        reading_perc = 0
        listening_perc = 0
        speaking_perc = 0
        writing_perc = 0
        total_perc = 0

    uofe_comment = ''
    reading_comment = ''
    listening_comment = ''
    speaking_comment = ''
    writing_comment = ''

    if student.course.course_name == 'CPE':
        if uofe_perc < 50:
            uofe_comment = random.choice([des.B2P_U_A, des.B2P_U_B, des.B2P_U_C])
        elif uofe_perc < 60:
            uofe_comment = random.choice([des.C1_U_A, des.C1_U_B, des.C1_U_C])
        elif uofe_perc < 70:
            uofe_comment = random.choice([des.C1P_U_A, des.C1P_U_B, des.C1P_U_C])
        elif uofe_perc >= 70:
            uofe_comment = random.choice([des.C2_U_A, des.C2_U_B, des.C2_U_C])

        if reading_perc < 50:
            reading_comment = random.choice([des.B2P_R_A, des.B2P_R_B, des.B2P_R_C])
        elif reading_perc < 60:
            reading_comment = random.choice([des.C1_R_A, des.C1_R_B, des.C1_R_C])
        elif reading_perc < 70:
            reading_comment = random.choice([des.C1P_R_A, des.C1P_R_B, des.C1P_R_C])
        elif reading_perc >= 70:
            reading_comment = random.choice([des.C2_R_A, des.C2_R_B, des.C2_R_C])

        if listening_perc < 50:
            listening_comment = random.choice([des.B2P_L_A, des.B2P_L_B, des.B2P_L_C])
        elif listening_perc < 60:
            listening_comment = random.choice([des.C1_L_A, des.C1_L_B, des.C1_L_C])
        elif listening_perc < 70:
            listening_comment = random.choice([des.C1P_L_A, des.C1P_L_B, des.C1P_L_C])
        elif listening_perc >= 70:
            listening_comment = random.choice([des.C2_L_A, des.C2_L_B, des.C2_L_C])

        if speaking_perc < 50:
            speaking_comment = random.choice([des.B2P_S_A, des.B2P_S_B, des.B2P_S_C])
        elif speaking_perc < 60:
            speaking_comment = random.choice([des.C1_S_A, des.C1_S_B, des.C1_S_C])
        elif speaking_perc < 70:
            speaking_comment = random.choice([des.C1P_S_A, des.C1P_S_B, des.C1P_S_C])
        elif speaking_perc >= 70:
            speaking_comment = random.choice([des.C2_S_A, des.C2_S_B, des.C2_S_C])

        if writing_perc < 50:
            writing_comment = random.choice([des.B2P_W_A, des.B2P_W_B, des.B2P_W_C])
        elif writing_perc < 60:
            writing_comment = random.choice([des.C1_W_A, des.C1_W_B, des.C1_W_C])
        elif writing_perc < 70:
            writing_comment = random.choice([des.C1P_W_A, des.C1P_W_B, des.C1P_W_C])
        elif writing_perc >= 70:
            writing_comment = random.choice([des.C2_W_A, des.C2_W_B, des.C2_W_C])

    elif student.course.course_name == 'CAE':
        if uofe_perc < 50:
            uofe_comment = random.choice([des.B2_U_A, des.B2_U_B, des.B2_U_C])
        elif uofe_perc < 60:
            uofe_comment = random.choice([des.B2P_U_A, des.B2P_U_B, des.B2P_U_C])
        elif uofe_perc < 70:
            uofe_comment = random.choice([des.C1_U_A, des.C1_U_B, des.C1_U_C])
        elif reading_perc < 80:
            reading_comment = random.choice([des.C1P_U_A, des.C1P_U_B, des.C1P_U_C])
        elif uofe_perc >= 80:
            uofe_comment = random.choice([des.C2_U_A, des.C2_U_B, des.C2_U_C])

        if reading_perc < 50:
            reading_comment = random.choice([des.B2_R_A, des.B2_R_B, des.B2_R_C])
        elif reading_perc < 60:
            reading_comment = random.choice([des.B2P_R_A, des.B2P_R_B, des.B2P_R_C])
        elif reading_perc < 70:
            reading_comment = random.choice([des.C1_R_A, des.C1_R_B, des.C1_R_C])
        elif reading_perc < 80:
            reading_comment = random.choice([des.C1P_R_A, des.C1P_R_B, des.C1P_R_C])
        elif reading_perc >= 80:
            reading_comment = random.choice([des.C2_R_A, des.C2_R_B, des.C2_R_C])

        if listening_perc < 50:
            listening_comment = random.choice([des.B2_L_A, des.B2_L_B, des.B2_L_C])
        elif listening_perc < 60:
            listening_comment = random.choice([des.B2P_L_A, des.B2P_L_B, des.B2P_L_C])
        elif listening_perc < 70:
            listening_comment = random.choice([des.C1_L_A, des.C1_L_B, des.C1_L_C])
        elif listening_perc < 80:
            listening_comment = random.choice([des.C1P_L_A, des.C1P_L_B, des.C1P_L_C])
        elif listening_perc >= 80:
            listening_comment = random.choice([des.C2_L_A, des.C2_L_B, des.C2_L_C])

        if speaking_perc < 50:
            speaking_comment = random.choice([des.B2_S_A, des.B2_S_B, des.B2_S_C])
        elif speaking_perc < 60:
            speaking_comment = random.choice([des.B2P_S_A, des.B2P_S_B, des.B2P_S_C])
        elif speaking_perc < 70:
            speaking_comment = random.choice([des.C1_S_A, des.C1_S_B, des.C1_S_C])
        elif speaking_perc < 80:
            speaking_comment = random.choice([des.C1P_S_A, des.C1P_S_B, des.C1P_S_C])
        elif speaking_perc >= 80:
            speaking_comment = random.choice([des.C2_S_A, des.C2_S_B, des.C2_S_C])

        if writing_perc < 50:
            writing_comment = random.choice([des.B2_W_A, des.B2_W_B, des.B2_W_C])
        elif writing_perc < 60:
            writing_comment = random.choice([des.B2P_W_A, des.B2P_W_B, des.B2P_W_C])
        elif writing_perc < 70:
            writing_comment = random.choice([des.C1_W_A, des.C1_W_B, des.C1_W_C])
        elif writing_perc < 80:
            writing_comment = random.choice([des.C1P_W_A, des.C1P_W_B, des.C1P_W_C])
        elif writing_perc >= 80:
            writing_comment = random.choice([des.C2_W_A, des.C2_W_B, des.C2_W_C])

    elif student.course.course_name == 'FCE':
        if uofe_perc < 50:
            uofe_comment = random.choice([des.B1_U_A, des.B1_U_B, des.B1_U_C])
        elif uofe_perc < 60:
            uofe_comment = random.choice([des.B1P_U_A, des.B1P_U_B, des.B1P_U_C])
        elif uofe_perc < 70:
            uofe_comment = random.choice([des.B2_U_A, des.B2_U_B, des.B2_U_C])
        elif reading_perc < 80:
            reading_comment = random.choice([des.B2P_U_A, des.B2P_U_B, des.B2P_U_C])
        elif uofe_perc >= 80:
            uofe_comment = random.choice([des.C1_U_A, des.C1_U_B, des.C1_U_C])

        if reading_perc < 50:
            reading_comment = random.choice([des.B1_R_A, des.B1_R_B, des.B1_R_C])
        elif reading_perc < 60:
            reading_comment = random.choice([des.B1P_R_A, des.B1P_R_B, des.B1P_R_C])
        elif reading_perc < 70:
            reading_comment = random.choice([des.B2_R_A, des.B2_R_B, des.B2_R_C])
        elif reading_perc < 80:
            reading_comment = random.choice([des.B2P_R_A, des.B2P_R_B, des.B2P_R_C])
        elif reading_perc >= 80:
            reading_comment = random.choice([des.C1_R_A, des.C1_R_B, des.C1_R_C])

        if listening_perc < 50:
            listening_comment = random.choice([des.B1_L_A, des.B1_L_B, des.B1_L_C])
        elif listening_perc < 60:
            listening_comment = random.choice([des.B1P_L_A, des.B1P_L_B, des.B1P_L_C])
        elif listening_perc < 70:
            listening_comment = random.choice([des.B2_L_A, des.B2_L_B, des.B2_L_C])
        elif listening_perc < 80:
            listening_comment = random.choice([des.B2P_L_A, des.B2P_L_B, des.B2P_L_C])
        elif listening_perc >= 80:
            listening_comment = random.choice([des.C1_L_A, des.C1_L_B, des.C1_L_C])

        if speaking_perc < 50:
            speaking_comment = random.choice([des.B1_S_A, des.B1_S_B, des.B1_S_C])
        elif speaking_perc < 60:
            speaking_comment = random.choice([des.B1P_S_A, des.B1P_S_B, des.B1P_S_C])
        elif speaking_perc < 70:
            speaking_comment = random.choice([des.B2_S_A, des.B2_S_B, des.B2_S_C])
        elif speaking_perc < 80:
            speaking_comment = random.choice([des.B2P_S_A, des.B2P_S_B, des.B2P_S_C])
        elif speaking_perc >= 80:
            speaking_comment = random.choice([des.C1_S_A, des.C1_S_B, des.C1_S_C])

        if writing_perc < 50:
            writing_comment = random.choice([des.B1_W_A, des.B1_W_B, des.B1_W_C])
        elif writing_perc < 60:
            writing_comment = random.choice([des.B1P_W_A, des.B1P_W_B, des.B1P_W_C])
        elif writing_perc < 70:
            writing_comment = random.choice([des.B2_W_A, des.B2_W_B, des.B2_W_C])
        elif writing_perc < 80:
            writing_comment = random.choice([des.B2P_W_A, des.B2P_W_B, des.B2P_W_C])
        elif writing_perc >= 80:
            writing_comment = random.choice([des.C1_W_A, des.C1_W_B, des.C1_W_C])

    context = {
        'student': student,
        'precourse': precourse,
        'midcourse': midcourse,
        'endcourse': endcourse,
        'uofe_perc': uofe_perc,
        'reading_perc': reading_perc,
        'listening_perc': listening_perc,
        'speaking_perc': speaking_perc,
        'writing_perc': writing_perc,
        'total_perc': total_perc,
        'uofe_comment': uofe_comment,
        'reading_comment': reading_comment,
        'listening_comment': listening_comment,
        'speaking_comment': speaking_comment,
        'writing_comment': writing_comment,
    }

    template_path = 'teacher/report-mid.html'

    filename = f'{student.first_name} {student.last_name} mid.pdf'
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="%s"' % (filename)
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


def render_endpdf_view(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if ExamScore.objects.filter(student_id=pk, exam_name='PreCourse').exists():
        precourse = ExamScore.objects.get(student_id=pk, exam_name='PreCourse')
    else:
        precourse = ""
    if ExamScore.objects.filter(student_id=pk, exam_name='MidCourse').exists():
        midcourse = ExamScore.objects.get(student_id=pk, exam_name='MidCourse')
    else:
        midcourse = ""
    if ExamScore.objects.filter(student_id=pk, exam_name='EndCourse').exists():
        endcourse = ExamScore.objects.get(student_id=pk, exam_name='EndCourse')
    else:
        endcourse = ""

    if precourse != "":
        pre_uofe_perc = round((precourse.uofe / 36) * 100, 0)
        pre_reading_perc = round((precourse.reading / 36) * 100, 0)
        pre_listening_perc = round((precourse.listening / 30) * 100, 0)
        pre_speaking_perc = round((precourse.speaking / 5) * 100, 0)
        pre_writing_perc = round((precourse.writing / 5) * 100, 0)
        pre_total_perc = round((pre_uofe_perc + pre_reading_perc + pre_listening_perc + pre_speaking_perc + pre_writing_perc) / 5, 0)
    else:
        pre_uofe_perc = 0
        pre_reading_perc = 0
        pre_listening_perc = 0
        pre_speaking_perc = 0
        pre_writing_perc = 0
        pre_total_perc = 0

    if midcourse != "":
        mid_uofe_perc = round((midcourse.uofe / 36) * 100, 0)
        mid_reading_perc = round((midcourse.reading / 36) * 100, 0)
        mid_listening_perc = round((midcourse.listening / 30) * 100, 0)
        mid_speaking_perc = round((midcourse.speaking / 5) * 100, 0)
        mid_writing_perc = round((midcourse.writing / 5) * 100, 0)
        mid_total_perc = round((mid_uofe_perc + mid_reading_perc + mid_listening_perc + mid_speaking_perc + mid_writing_perc) / 5, 0)
    else:
        mid_uofe_perc = 0
        mid_reading_perc = 0
        mid_listening_perc = 0
        mid_speaking_perc = 0
        mid_writing_perc = 0
        mid_total_perc = 0

    if endcourse != "":
        end_uofe_perc = round((endcourse.uofe / 36) * 100, 0)
        end_reading_perc = round((endcourse.reading / 36) * 100, 0)
        end_listening_perc = round((endcourse.listening / 30) * 100, 0)
        end_speaking_perc = round((endcourse.speaking / 5) * 100, 0)
        end_writing_perc = round((endcourse.writing / 5) * 100, 0)
        end_total_perc = round((end_uofe_perc + end_reading_perc + end_listening_perc + end_speaking_perc + end_writing_perc) / 5, 0)
    else:
        end_uofe_perc = 0
        end_reading_perc = 0
        end_listening_perc = 0
        end_speaking_perc = 0
        end_writing_perc = 0
        end_total_perc = 0

    grade = ""
    if end_total_perc < 16:
        grade = 'F'
    elif end_total_perc < 40:
        grade = 'E'
    elif end_total_perc < 50:
        grade = 'D'
    elif end_total_perc < 70:
        grade = 'C'
    elif end_total_perc < 80:
        grade = 'B'
    elif end_total_perc >= 80:
        grade = 'A'

    context = {
        'student': student,
        'precourse': precourse,
        'midcourse': midcourse,
        'endcourse': endcourse,
        'pre_uofe_perc': pre_uofe_perc,
        'pre_reading_perc': pre_reading_perc,
        'pre_listening_perc': pre_listening_perc,
        'pre_speaking_perc': pre_speaking_perc,
        'pre_writing_perc': pre_writing_perc,
        'pre_total_perc': pre_total_perc,
        'mid_uofe_perc': mid_uofe_perc,
        'mid_reading_perc': mid_reading_perc,
        'mid_listening_perc': mid_listening_perc,
        'mid_speaking_perc': mid_speaking_perc,
        'mid_writing_perc': mid_writing_perc,
        'mid_total_perc': mid_total_perc,
        'end_uofe_perc': end_uofe_perc,
        'end_reading_perc': end_reading_perc,
        'end_listening_perc': end_listening_perc,
        'end_speaking_perc': end_speaking_perc,
        'end_writing_perc': end_writing_perc,
        'end_total_perc': end_total_perc,
        'grade': grade
    }

    template_path = 'teacher/report-end.html'

    filename = f'{student.first_name} {student.last_name} end.pdf'
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="%s"' % (filename)
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# class MidReportDetailView(DetailView):
#     template_name = 'teacher/report-mid.html'
#     model = Student
#     context_object_name = 'student'


