from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from CST_SPMS.models import CustomUser, Projects, Proposals,  StudentGroups, Students, PromotionYear, Supervisors, FeedBackSupervisor
from .forms import AddStudentForm, EditStudentForm

import json
import csv

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import datetime

def admin_home(request):
    # all_student_count = Students.objects.all().count()
    project_count = Projects.objects.all().count()
    Proposal_count = Proposals.objects.all().count()
    supervisor_count = Supervisors.objects.all().count()
    group_count = StudentGroups.objects.all().count()


    # Total Subjects and students in Each Course
    group_all = StudentGroups.objects.all()
    # course_name_list = []
    # subject_count_list = []
    # student_count_list_in_course = []

    # for course in course_all:
    #     subjects = Subjects.objects.filter(course_id=course.id).count()
    #     students = Students.objects.filter(course_id=course.id).count()
    #     course_name_list.append(course.course_name)
    #     subject_count_list.append(subjects)
    #     student_count_list_in_course.append(students)
    
    projects_all = Projects.objects.all()
    # subject_list = []
    # student_count_list_in_subject = []
    # for subject in subject_all:
    #     course = Courses.objects.get(id=subject.course_id.id)
    #     student_count = Students.objects.filter(course_id=course.id).count()
    #     subject_list.append(subject.subject_name)
    #     student_count_list_in_subject.append(student_count)
    
    # For Saffs
    # staff_attendance_present_list=[]
    # staff_attendance_leave_list=[]
    supervisor_name_list=[]

    supervisors = Supervisors.objects.all()
    # for staff in staffs:
    #     subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
    #     attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
    #     leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
    #     staff_attendance_present_list.append(attendance)
    #     staff_attendance_leave_list.append(leaves)
        #   supervisor_name_list.append(supervisor.admin.first_name)

    # For Students
    # student_name_list=[]

    # students = Students.objects.all()
    # for student in students:
        # attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        # absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        # leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        # student_attendance_present_list.append(attendance)
        # student_attendance_leave_list.append(leaves+absent)
        # student_name_list.append(student.admin.first_name)


    context={
        # "all_student_count": all_student_count,
        "project_count": project_count,
        "group_count": group_count,
        "supervisor_count": supervisor_count,
        # "course_name_list": course_name_list,
        # "subject_count_list": subject_count_list,
        # "student_count_list_in_course": student_count_list_in_course,
        # "subject_list": subject_list,
        # "student_count_list_in_subject": student_count_list_in_subject,
        # "staff_attendance_present_list": staff_attendance_present_list,
        # "staff_attendance_leave_list": staff_attendance_leave_list,
        # "staff_name_list": staff_name_list,
        # "student_attendance_present_list": student_attendance_present_list,
        # "student_attendance_leave_list": student_attendance_leave_list,
        # "student_name_list": student_name_list,
    }
    return render(request, "hod_template/home_content.html", context)


def add_supervisor(request):
    # groups = StudentGroups.objects.all()

    # context = {
    #     "groups": groups
    # }
    return render(request, "hod_template/add_supervisor_template.html")


def add_supervisor_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_supervisor')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # address = request.POST.get('address')
        gender = request.POST.get('gender')
        # group_id = request.POST.get('group')
        # group = StudentGroups.objects.get(id=group_id)
       

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.supervisors.gender = gender
            user.save()
            messages.success(request, "supervisor Added Successfully!")
            return redirect('add_supervisor')
        except:
            messages.error(request, "Failed to Add supervisor!")
            return redirect('add_supervisor')



def manage_supervisor(request):
    supervisors = Supervisors.objects.all()
    context = {
        "supervisors": supervisors
    }
    return render(request, "hod_template/manage_supervisor_template.html", context)


def edit_supervisor(request, supervisor_id):
    supervisor = Supervisors.objects.get(admin=supervisor_id)

    context = {
        "supervisor": supervisor,
        "id": supervisor_id
    }
    return render(request, "hod_template/edit_supervisor_template.html", context)


def edit_supervisor_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        supervisor_id = request.POST.get('supervisor_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        # profile_pic = request.POST.get('profile_pic')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=supervisor_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            
            user.save()
            
            # INSERTING into supervisor Model
            supervisor_model = Supervisors.objects.get(admin=supervisor_id)
            supervisor_model.address = address
            # supervisor_model.profile_pic = profile_pic
            supervisor_model.save()

            messages.success(request, "supervisor Updated Successfully.")
            return redirect('/edit_supervisor/'+supervisor_id)

        except:
            messages.error(request, "Failed to Update supervisor.")
            return redirect('/edit_supervisor/'+supervisor_id)



def delete_supervisor(request, supervisor_id):
    upervisor = Supervisors.objects.get(admin=supervisor_id)
    try:
        upervisor.delete()
        messages.success(request, "supervisor Deleted Successfully.")
        return redirect('manage_supervisor')
    except:
        messages.error(request, "Failed to Delete supervisor.")
        return redirect('manage_supervisor')

def export_csv_sup(request):
    '''
        Generating reports Hod Supervisor
    '''
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Supervisors' + str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['id','Gender', 'Created At', 'Updated at'])

    supervisors = Supervisors.objects.all()
    
    for supervisor in supervisors:
        writer.writerow([supervisor.id,supervisor.gender, supervisor.created_at, supervisor.updated_at])

    return response

def export_pdf_sup(request):
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Groups' + str(datetime.datetime.now())+'.pdf'


    response['Content-Transfer-Encoding'] = 'binary'

    supervisors = Supervisors.objects.all()

    html_string = render_to_string('hod_template/pdf_supervisor_template.html', {'supervisors':supervisors})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read()) 

    return response



def add_group(request):
    return render(request, "hod_template/add_group_template.html")


def add_group_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_group')
    else:
        username = request.POST.get('username')
        first_name = ''
        last_name = ''
        
        email = ''
        group_name = request.POST.get('group_name')
        password = request.POST.get('password')
        
        
        
        
        
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.studentgroups.group_name = group_name
            user.save()
            
            messages.success(request, "group Added Successfully!")
            return redirect('add_group')
        except:
            messages.error(request, "Failed to Add group!")
            return redirect('add_group')


def manage_group(request):
    groups = StudentGroups.objects.all()
    context = {
        "groups": groups
    }
    return render(request, 'hod_template/manage_group_template.html', context)


def edit_group(request, group_id):
    group = StudentGroups.objects.get(id=group_id)
    context = {
        "group": group,
        "id": group_id
    }
    return render(request, 'hod_template/edit_group_template.html', context)


def edit_group_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        group_id = request.POST.get('group_id')
        group_name = request.POST.get('group')

        try:
            group = StudentGroups.objects.get(id=group_id)
            group.group_name = group_name
            group.save()

            messages.success(request, "group Updated Successfully.")
            return redirect('/edit_group/'+group_id)

        except:
            messages.error(request, "Failed to Update group.")
            return redirect('/edit_group/'+group_id)


def delete_group(request, group_id):
    group = StudentGroups.objects.get(id=group_id)
    try:
        group.delete()
        messages.success(request, "group Deleted Successfully.")
        return redirect('manage_group')
    except:
        messages.error(request, "Failed to Delete group.")
        return redirect('manage_group')


def export_csv(request):
    '''
        Generating reports Hod Groups
    '''
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Groups' + str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['id','Group Name', 'Created At', 'Updated at'])

    groups = StudentGroups.objects.all()
    
    for group in groups:
        writer.writerow([group.id, group.group_name, group.created_at, group.updated_at])

    return response

def export_pdf(request):
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Groups' + str(datetime.datetime.now())+'.pdf'


    response['Content-Transfer-Encoding'] = 'binary'

    groups = StudentGroups.objects.all()

    html_string = render_to_string('hod_template/pdf_group_output.html', {'groups':groups})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read()) 

    return response

# def manage_session(request):
#     session_years = SessionYearModel.objects.all()
#     context = {
#         "session_years": session_years
#     }
#     return render(request, "hod_template/manage_session_template.html", context)


# def add_session(request):
#     return render(request, "hod_template/add_session_template.html")


# def add_session_save(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('add_group')
#     else:
#         session_start_year = request.POST.get('session_start_year')
#         session_end_year = request.POST.get('session_end_year')

#         try:
#             sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
#             sessionyear.save()
#             messages.success(request, "Session Year added Successfully!")
#             return redirect("add_session")
#         except:
#             messages.error(request, "Failed to Add Session Year")
#             return redirect("add_session")


# def edit_session(request, session_id):
#     session_year = SessionYearModel.objects.get(id=session_id)
#     context = {
#         "session_year": session_year
#     }
#     return render(request, "hod_template/edit_session_template.html", context)


# def edit_session_save(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method!")
#         return redirect('manage_session')
#     else:
#         session_id = request.POST.get('session_id')
#         session_start_year = request.POST.get('session_start_year')
#         session_end_year = request.POST.get('session_end_year')

#         try:
#             session_year = SessionYearModel.objects.get(id=session_id)
#             session_year.session_start_year = session_start_year
#             session_year.session_end_year = session_end_year
#             session_year.save()

#             messages.success(request, "Session Year Updated Successfully.")
#             return redirect('/edit_session/'+session_id)
#         except:
#             messages.error(request, "Failed to Update Session Year.")
#             return redirect('/edit_session/'+session_id)


# def delete_session(request, session_id):
#     session = SessionYearModel.objects.get(id=session_id)
#     try:
#         session.delete()
#         messages.success(request, "Session Deleted Successfully.")
#         return redirect('manage_session')
#     except:
#         messages.error(request, "Failed to Delete Session.")
#         return redirect('manage_session')


def add_student(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_student_template.html', context)




def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            student_group = form.cleaned_data['student_group']
           
            gender = form.cleaned_data['gender']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
           


            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=4)
                user.students.address = address
                group_obj = StudentGroups.objects.get(id=student_group)
                user.students.student_group = group_obj
                user.students.gender = gender
                
                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('add_student')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('add_student')
        else:
            return redirect('add_student')


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)


def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['group_id'].initial = student.group_id.id
    form.fields['gender'].initial = student.gender
    
    

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            group_id = form.cleaned_data['group_id']
            gender = form.cleaned_data['gender']
            

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Students.objects.get(admin=student_id)
                student_model.address = address

                group = StudentGroups.objects.get(id=id)
                student_model.group_id = group
                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect('/edit_student/'+student_id)
        else:
            return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


# def add_subject(request):
#     courses = Courses.objects.all()
#     staffs = CustomUser.objects.filter(user_type='2')
#     context = {
#         "courses": courses,
#         "staffs": staffs
#     }
#     return render(request, 'hod_template/add_subject_template.html', context)



# def add_subject_save(request):
#     if request.method != "POST":
#         messages.error(request, "Method Not Allowed!")
#         return redirect('add_subject')
#     else:
#         subject_name = request.POST.get('subject')

#         course_id = request.POST.get('course')
#         course = Courses.objects.get(id=course_id)
        
#         staff_id = request.POST.get('staff')
#         staff = CustomUser.objects.get(id=staff_id)

#         try:
#             subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
#             subject.save()
#             messages.success(request, "Subject Added Successfully!")
#             return redirect('add_subject')
#         except:
#             messages.error(request, "Failed to Add Subject!")
#             return redirect('add_subject')


# def manage_subject(request):
#     subjects = Subjects.objects.all()
#     context = {
#         "subjects": subjects
#     }
#     return render(request, 'hod_template/manage_subject_template.html', context)


# def edit_subject(request, subject_id):
#     subject = Subjects.objects.get(id=subject_id)
#     courses = Courses.objects.all()
#     staffs = CustomUser.objects.filter(user_type='2')
#     context = {
#         "subject": subject,
#         "courses": courses,
#         "staffs": staffs,
#         "id": subject_id
#     }
#     return render(request, 'hod_template/edit_subject_template.html', context)


# def edit_subject_save(request):
#     if request.method != "POST":
#         HttpResponse("Invalid Method.")
#     else:
#         subject_id = request.POST.get('subject_id')
#         subject_name = request.POST.get('subject')
#         course_id = request.POST.get('course')
#         staff_id = request.POST.get('staff')

#         try:
#             subject = Subjects.objects.get(id=subject_id)
#             subject.subject_name = subject_name

#             course = Courses.objects.get(id=course_id)
#             subject.course_id = course

#             staff = CustomUser.objects.get(id=staff_id)
#             subject.staff_id = staff
            
#             subject.save()

#             messages.success(request, "Subject Updated Successfully.")
#             # return redirect('/edit_subject/'+subject_id)
#             return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

#         except:
#             messages.error(request, "Failed to Update Subject.")
#             return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))
#             # return redirect('/edit_subject/'+subject_id)



# def delete_subject(request, subject_id):
#     subject = Subjects.objects.get(id=subject_id)
#     try:
#         subject.delete()
#         messages.success(request, "Subject Deleted Successfully.")
#         return redirect('manage_subject')
#     except:
#         messages.error(request, "Failed to Delete Subject.")
#         return redirect('manage_subject')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def supervisor_feedback_message(request):
    feedbacks = FeedBackSupervisor.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/supervisor_feedback_template.html', context)


@csrf_exempt
def supervisor_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackSupervisor.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


# def student_leave_view(request):
#     leaves = LeaveReportStudent.objects.all()
#     context = {
#         "leaves": leaves
#     }
#     return render(request, 'hod_template/student_leave_view.html', context)

# def student_leave_approve(request, leave_id):
#     leave = LeaveReportStudent.objects.get(id=leave_id)
#     leave.leave_status = 1
#     leave.save()
#     return redirect('student_leave_view')


# def student_leave_reject(request, leave_id):
#     leave = LeaveReportStudent.objects.get(id=leave_id)
#     leave.leave_status = 2
#     leave.save()
#     return redirect('student_leave_view')


# def staff_leave_view(request):
#     leaves = LeaveReportStaff.objects.all()
#     context = {
#         "leaves": leaves
#     }
#     return render(request, 'hod_template/staff_leave_view.html', context)


# def staff_leave_approve(request, leave_id):
#     leave = LeaveReportStaff.objects.get(id=leave_id)
#     leave.leave_status = 1
#     leave.save()
#     return redirect('staff_leave_view')


# def staff_leave_reject(request, leave_id):
#     leave = LeaveReportStaff.objects.get(id=leave_id)
#     leave.leave_status = 2
#     leave.save()
#     return redirect('staff_leave_view')


# def admin_view_attendance(request):
#     subjects = Subjects.objects.all()
#     session_years = SessionYearModel.objects.all()
#     context = {
#         "subjects": subjects,
#         "session_years": session_years
#     }
#     return render(request, "hod_template/admin_view_attendance.html", context)


# @csrf_exempt
# def admin_get_attendance_dates(request):
#     # Getting Values from Ajax POST 'Fetch Student'
#     subject_id = request.POST.get("subject")
#     session_year = request.POST.get("session_year_id")

#     # Students enroll to Course, Course has Subjects
#     # Getting all data from subject model based on subject_id
#     subject_model = Subjects.objects.get(id=subject_id)

#     session_model = SessionYearModel.objects.get(id=session_year)

#     # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
#     attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

#     # Only Passing Student Id and Student Name Only
#     list_data = []

#     for attendance_single in attendance:
#         data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
#         list_data.append(data_small)

#     return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# @csrf_exempt
# def admin_get_attendance_student(request):
#     # Getting Values from Ajax POST 'Fetch Student'
#     attendance_date = request.POST.get('attendance_date')
#     attendance = Attendance.objects.get(id=attendance_date)

#     attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
#     # Only Passing Student Id and Student Name Only
#     list_data = []

#     for student in attendance_data:
#         data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
#         list_data.append(data_small)

#     return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def supervisor_profile(request):
    pass


# def student_profile(requtest):
#     pass



