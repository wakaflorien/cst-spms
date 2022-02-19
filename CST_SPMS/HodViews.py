from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from CST_SPMS.models import AdminHOD, CustomUser, FeedBackGroup, FeedBackHOD, Projects, Proposals,  StudentGroups, Students, PromotionYear, Supervisors, FeedBackSupervisor
# from .forms import AddStudentForm, EditStudentForm

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
    groups = StudentGroups.objects.all()

    context = {
        "groups": groups
    }
    return render(request, "hod_template/add_supervisor_template.html", context)


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
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        degree = request.POST.get('degree')
        spec = request.POST.get('spec')
        profile = request.POST.get('profile_pic')
        group_id = request.POST.get('group')
        # group = StudentGroups.objects.get(id=group_id)
       
        # try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
        # admin = user.id
        supervisor = Supervisors(specialization=spec, degree=degree, address=address, gender=gender, profile_pic=profile, admin=user)
        supervisor.save()
        user.save()
        messages.success(request, "supervisor Added Successfully!")
        return redirect('manage_supervisor')
        # except:
            # messages.error(request, "Failed to Add supervisor!")
            # return redirect('add_supervisor')



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
        gender = request.POST.get('gender')
        spec = request.POST.get('spec')
        degree = request.POST.get('degree')
        address = request.POST.get('address')
        profile_pic = request.POST.get('profile_pic')
        password = request.POST.get('password')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=supervisor_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.password = password
            
            user.save()
            
            # INSERTING into supervisor Model
            supervisor_model = Supervisors.objects.get(admin=supervisor_id)
            supervisor_model.specialization = spec
            supervisor_model.degree = degree
            supervisor_model.address = address
            supervisor_model.gender = gender
            supervisor_model.profile_pic = profile_pic
            supervisor_model.save()

            messages.success(request, "supervisor Updated Successfully.")
            return redirect('/manage_supervisor/')
            # return redirect('/manage_supervisor/'+supervisor_id)

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
        group_no = request.POST.get('group_no')
        first_name = ''
        last_name = ''
        
        email = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        # try:
        for i in range(int(group_no)):
            counter = 0
            counter = StudentGroups.objects.count()
            counter += 1
            username = username+ "_" +str(counter)
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.studentgroups.group_name = username
            user.save()
            splited = username.split('_')
            splited.pop(1)
            username=''.join(splited)
            # print(username)
        messages.success(request, "Groups Created Successfully!")
        return redirect('manage_group')
        # except:
        #     messages.error(request, "Failed to Add group!")
        #     return redirect('add_group')


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
            return redirect('/manage_group/')

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

def add_student(request):
    groups = StudentGroups.objects.all()

    context = {
        "groups": groups
    }
    return render(request, 'hod_template/add_student_template.html', context)

def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            group_id = request.POST.get('group')
            group = StudentGroups.objects.get(id=group_id)
            
            print(address, gender ,group)
            # try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=4)
            
            student = Students(address=address, gender=gender, group=group, admin=user)
            student.save()
            user.save()
            messages.success(request, "Student Added Successfully!")
            return redirect('manage_student')
            # except:
            #     messages.error(request, "Failed to Add Student!")
            #     return redirect('add_student')
            


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)

def manage_project(request):
    proposals = Proposals.objects.all()
    supervisors = Supervisors.objects.all()
    students = StudentGroups.objects.all()
    students_no = StudentGroups.objects.all().count()

    for supervi in supervisors:
        groups = StudentGroups.objects.filter(supervisor = supervi.id).count()
        groups +=1

        # print (supervi.id)
    # print(groups)
    members = []
    for student in students:
        member = Students.objects.filter(group = student.id)

        if member:
            member_no = Students.objects.filter(group = student.id).count()
            for i in range(member_no):
                one=member[i].admin.first_name +" "+ member[i].admin.last_name 
                members.append(one)
            # print(one)
        
    print(members)
    
    context = {
        "proposals": proposals,
        "supervisors": supervisors,
        "groups": groups,
        "members": members,
    }
    return render(request, 'hod_template/manage_project_template.html', context)

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
manage_project

@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def hod_group_feedback_message(request):
    feedback_data = FeedBackGroup.objects.all()
    
    groups = StudentGroups.objects.all()

    context = {
        "feedback_data":feedback_data,
        "groups": groups
    }
    return render(request, "hod_template/group_feedback_template.html", context)

def supervisor_feedback_message(request):
    feedback_data = FeedBackSupervisor.objects.all()
    
    print(feedback_data)

    context = {
        "feedback_data":feedback_data,
    }
    return render(request, "hod_template/supervisor_feedback_template.html", context)


@csrf_exempt
def supervisor_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')
    hod = AdminHOD.objects.get()
    try:
        feedback = FeedBackGroup.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.hod = hod
        feedback.save()
        
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def hod_feedback_message(request):
    hod_obj = AdminHOD.objects.get(admin=request.user.id)
    # feedback_data = FeedBackHOD.objects.filter(hod=hod_obj)

    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('supervisor_feedback_message')
    else:
        feedback = request.POST.get('feedback_message')
        to = request.POST.get('to')
        too = StudentGroups.objects.get(id = to)

        print(to)

        # try:
        add_feedback = FeedBackGroup(hod=hod_obj, feedback="", feedback_reply=feedback, group = too)
        add_feedback.save()
        messages.success(request, "Message Sent.")
        return redirect('hod_group_feedback_message')
        # except:
        #     messages.error(request, "Failed to Send Feedback.")
        #     return redirect('hod_group_feedback_message')

@csrf_exempt
def proposal_accept(request):
    proposal_id = request.POST.get('id')
    # feedback_reply = request.POST.get('reply')
    hod = AdminHOD.objects.get()
    try:
        proposal = Proposals.objects.get(id=proposal_id)
        proposal.status = proposal_id
        proposal.save()
        
        return HttpResponse("True")

    except:
        return HttpResponse("False")

@csrf_exempt
def proposal_deny(request):
    proposal_id = request.POST.get('id')
    # feedback_reply = request.POST.get('reply')
    hod = AdminHOD.objects.get()
    try:
        proposal = Proposals.objects.get(id=proposal_id)
        proposal.status = "0"
        proposal.save()
        
        return HttpResponse("True")

    except:
        return HttpResponse("False")

@csrf_exempt
def supervisor_assign(request):

    proposal_id = request.POST.get('id1')
    id2 = request.POST.get('id2')

    supervisor_id = Supervisors.objects.get(id=id2)

    print(supervisor_id, proposal_id)
    # hod = AdminHOD.objects.get()
    # try:

    group = StudentGroups.objects.get(id=proposal_id)
    group.supervisor = supervisor_id
    group.save()
    
    return HttpResponse("True")

    # except:
    # return HttpResponse("False")
    # INSERTING into Group Model
    # group = StudentGroups.objects.get(admin=supervisor_id)
    # supervisor_model.specialization = spec
    # messages.success(request, "supervisor Updated Successfully.")
    # return redirect('/manage_supervisor/')



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



