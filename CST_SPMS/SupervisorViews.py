from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from CST_SPMS.models import CustomUser, Projects, FeedBackSupervisor, Proposals,  StudentGroups, Students, PromotionYear, Supervisors, NotificationSupervisors, FeedBackGroup

def supervisor_home(request):
    
    supervisors = Supervisors.objects.all()
    studentgroups = StudentGroups.objects.all()
    group_id_list = []
    # for studentgroup in studentgroups:
        # group_id_list.append(studentgroup.id)
    
    for sup in supervisors:
        # print(group.group.id)
        for group in studentgroups:
            groups = StudentGroups.objects.filter(id = sup.group.id)
            groups_count = groups.count()
    # students_count = Students.objects.all().count()

    context={
        # "students_count": students_count,
        "groups_count": groups_count,
  
    }
    return render(request, "supervisor_template/supervisor_home_template.html", context)

def supervisor_manage_proposal(request):
    proposas = Proposals.objects.all()
    print(proposas)
    context = {
        "proposals": proposas
    }
    return render(request, "supervisor_template/supervisor_manage_proposal.html", context)

def supervisor_assigned_group(request):
    supervisor = Supervisors.objects.get(admin=request.user.id)
    print(supervisor.admin.id)
    all_groups = StudentGroups.objects.filter()
    supervisors = Supervisors.objects.all()


    for sup in supervisors:
        # print(group.group.id, and sup.admin.id == supervisor.admin.id)
        for group in all_groups:
            # print(sup.admin.id, "hey")
            groups = StudentGroups.objects.filter(id = sup.group.id)
   
    print(groups)
    context = {
        "groups": groups
    }
    return render(request, "supervisor_template/supervisor_assigned_group.html", context)

def supervisor_assigned_ngroup(request, group_id):
    
    groups = StudentGroups.objects.filter(id = group_id)
   
    print(groups)
    context = {
        "groups": groups,
        "id": group_id
    }
    return render(request, "supervisor_template/supervisor_assigned_ngroup.html", context)
def group_feedback_message(request):
    feedbacks = FeedBackGroup.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'supervisor_template/group_feedback_template.html', context)


@csrf_exempt
def group_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackSupervisor.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def supervisor_feedback(request):
    supervisors_obj = Supervisors.objects.get(admin=request.user.id)
    feedback_data = FeedBackSupervisor.objects.filter(supervisor_id=supervisors_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "supervisor_template/supervisor_feedback_template.html", context)


def supervisor_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('supervisor_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        supervisor_obj = Supervisors.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackSupervisor(supervisor_id=supervisor_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('supervisor_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('supervisor_feedback')

# def supervisor_contact_hod(request):
#     return render(request, "supervisor_template/supervisor_contact_hod.html")


# def supervisor_contact_hod_save(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('staff_apply_leave')
#     else:
#         leave_date = request.POST.get('leave_date')
#         leave_message = request.POST.get('leave_message')

#         staff_obj = Supervisors.objects.get(admin=request.user.id)
#         try:
#             leave_report = NotificationSupervisors(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
#             leave_report.save()
#             messages.success(request, "Applied for Leave.")
#             return redirect('staff_apply_leave')
#         except:
#             messages.error(request, "Failed to Apply Leave")
#             return redirect('staff_apply_leave')

# # WE don't need csrf_token when using Ajax
# @csrf_exempt
# def get_students(request):
#     # Getting Values from Ajax POST 'Fetch Student'
#     subject_id = request.POST.get("subject")
#     session_year = request.POST.get("session_year")

#     # Students enroll to Course, Course has Subjects
#     # Getting all data from subject model based on subject_id
#     subject_model = Subjects.objects.get(id=subject_id)

#     session_model = SessionYearModel.objects.get(id=session_year)

#     students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)

#     # Only Passing Student Id and Student Name Only
#     list_data = []

#     for student in students:
#         data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name}
#         list_data.append(data_small)

#     return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

def supervisor_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    supervisor = Supervisors.objects.get(admin=user)

    context={
        "user": user,
        "supervisor": supervisor
    }
    return render(request, 'supervisor_template/supervisor_profile.html', context)


def supervisor_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('supervisor_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')
        profile_pic = request.POST.get('profile_pic')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            supervisor = Supervisors.objects.get(admin=customuser.id)
            supervisor.address = address
            supervisor.profile_pic = profile_pic
            supervisor.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('supervisor_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('supervisor_profile')