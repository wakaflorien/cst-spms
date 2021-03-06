from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime # To Parse input DateTime into Python Date Time Object

from CST_SPMS.models import AdminHOD, CustomUser, StudentGroups,  Students, Proposals, Projects,FeedBackGroup, Supervisors


def group_home(request):
    # group_obj = StudentGroups.objects.get(admin=request.user.id)

    user = StudentGroups.objects.get(admin=request.user.id)
    # members = Students.objects.get(group_id=user)
    member_no = Students.objects.filter(group_id=user).count()
    proposals_no = Proposals.objects.filter(studentgroup_id = user).count()

    context={
        "user": user,
        # "members": members,
        "member_no":member_no,
        "proposals_no":proposals_no,
       
    }

    return render(request, "group_template/group_home_template.html", context)


def group_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    group = StudentGroups.objects.get(admin=user)

    context1={
        "user": user,
        "group": group
    }
    return render(request, 'group_template/group_profile.html', context1)


def group_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('group_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            group = StudentGroups.objects.get(admin=customuser.id)
            group.address = address
            group.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('group_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('group_profile')


# The following are views for a group member
def add_member(request):
    groups = StudentGroups.objects.all()

    context = {
        "groups": groups
    }
    return render(request, "group_template/add_student_template.html", context)


def add_member_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_student')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        group = StudentGroups.objects.get(admin=request.user.id)
       
        # try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=4)
        # admin = user.id
        student = Students(address=address, gender=gender, group=group, admin=user)
        student.save()
        user.save()
        messages.success(request, "student Added Successfully!")
        return redirect('manage_member')
        # except:
            # messages.error(request, "Failed to Add student!")
            # return redirect('add_student')



def manage_member(request):
    groups= StudentGroups.objects.filter(admin=request.user.id)
    # students_all = Students.objects.all()
    # student_list = []
    for group in groups:
        students = Students.objects.filter(group=group.id)
        # student_list.append(students)
    context = {
        "students": students
    }
    return render(request, "group_template/manage_student_template.html", context)


def edit_member(request, student_id):
    student = Students.objects.get(admin=student_id)

    context = {
        "student": student,
        "id": student_id
    }
    return render(request, "group_template/edit_student_template.html", context)


def edit_member_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.POST.get('student_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        
        password = request.POST.get('password')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.password = password
            
            user.save()
            
            # INSERTING into student Model
            student_model = Students.objects.get(admin=student_id)
            student_model.address = address
            student_model.gender = gender
            
            student_model.save()

            messages.success(request, "student Updated Successfully.")
            return redirect('/manage_member/')
            # return redirect('/manage_student/'+student_id)

        except:
            messages.error(request, "Failed to Update student.")
            return redirect('/edit_member/'+student_id)


#The following are views for project proposals
def add_proposal(request):
    
    
    groups = CustomUser.objects.filter(user_type='3')
    context = {
        
        "groups": groups
    }
    return render(request, 'group_template/add_proposal_template.html', context)



def add_proposal_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_proposal')
    else:
        proposal_title = request.POST.get('proposal')
        promotion = request.POST.get('promotion')
        abstract = request.POST.get('abstract')
        
        
        group = StudentGroups.objects.get(admin=request.user.id)

        # try:
        proposal = Proposals(proposal_title=proposal_title,promotion=promotion, abstract=abstract, studentgroup_id=group)
        proposal.save()
        messages.success(request, "proposal Added Successfully!")
        return redirect('manage_proposal')
    # except:
        #     messages.error(request, "Failed to Add proposal!")
        #     return redirect('add_proposal')


def manage_proposal(request):

    user = StudentGroups.objects.get(admin=request.user.id)
    # member_no = Students.objects.filter(group_id=user).count()


    proposals = Proposals.objects.filter(studentgroup_id = user)
    
    context = {
        "proposals": proposals,
        
    }
    # print(proposals)
    return render(request, 'group_template/manage_proposal_template.html', context)


def edit_proposal(request, proposal_id):
    proposal = Proposals.objects.get(id=proposal_id)
    groups = CustomUser.objects.filter(user_type='3')
    context = {
        "proposal": proposal,
        "groups": groups,
        "id":proposal
    }
    return render(request, 'group_template/edit_proposal_template.html', context)


def edit_proposal_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        id = request.POST.get('id')
        proposal_title = request.POST.get('proposal')
        promotion = request.POST.get('promotion')
        abstract = request.POST.get('abstract')
        group = StudentGroups.objects.get(admin=request.user.id)

        # try:
        proposal = Proposals.objects.get(studentgroup_id=group)

        proposal.proposal_title = proposal_title
        proposal.promotion = promotion
        proposal.abstract = abstract
        proposal.studentgroup_id = group
        proposal.save()

        messages.success(request, "proposal Updated Successfully.")
        return redirect('/manage_proposal/')
            # return HttpResponseRedirect(reverse("edit_proposal", kwargs={"proposal_id":id}))

        # except:
        #     messages.error(request, "Failed to Update proposal.")
        #     # return HttpResponseRedirect(reverse("edit_proposal", kwargs={"proposal_id":id}))
        #     return redirect('/manage_proposal/')



def delete_proposal(request, proposal_id):
    proposal = Proposals.objects.get(id=proposal_id)
    try:
        proposal.delete()
        messages.success(request, "proposal Deleted Successfully.")
        return redirect('manage_proposal')
    except:
        messages.error(request, "Failed to Delete proposal.")
        return redirect('manage_proposal')


def group_feedback(request):
    group_obj = StudentGroups.objects.get(admin=request.user.id)
    feedback_data = FeedBackGroup.objects.filter(group=group_obj, supervisor=True)

    supervisor = Supervisors.objects.get(group = group_obj)

    # print(supervisor.id)

    context = {
        "feedback_data": feedback_data,
        "supervisor": supervisor
    }
    return render(request, 'group_template/group_contact_supervisor.html', context)

def group_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('group_feedback')
    else:
        # supervisor = request.POST.get('sup')
        # print(supervisor)

        feedback = request.POST.get('feedback_message')
        group_obj = StudentGroups.objects.get(admin=request.user.id)
        supervisor = Supervisors.objects.get(group = group_obj)

        # try:
        add_feedback = FeedBackGroup(group=group_obj, feedback=feedback, feedback_reply="", supervisor=supervisor)
        add_feedback.save()
        messages.success(request, "Feedback Sent.")
        return redirect('group_feedback')
        # except:
        #     messages.error(request, "Failed to Send Feedback.")
        #     return redirect('group_feedback')


def group_hod_feedback(request):
    group_obj = StudentGroups.objects.get(admin=request.user.id)
    feedback_data = FeedBackGroup.objects.filter(group=group_obj, hod = True)

    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'group_template/group_contact_hod.html', context)

def group_hod_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('group_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        group_obj = StudentGroups.objects.get(admin=request.user.id)
        hod = AdminHOD.objects.get()
        print(hod)

        try:
            add_feedback = FeedBackGroup(group=group_obj, feedback=feedback, feedback_reply="", hod = hod)
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('group_hod_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('group_feedback')

# def group_contact_hod(request):
#     return render(request, "group_template/group_contact_hod.html")


# def group_contact_hod_save(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('staff_apply_leave')
#     else:
#         leave_date = request.POST.get('leave_date')
#         leave_message = request.POST.get('leave_message')

#         staff_obj = groups.objects.get(admin=request.user.id)
#         try:
#             leave_report = Notificationgroups(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
#             leave_report.save()
#             messages.success(request, "Applied for Leave.")
#             return redirect('staff_apply_leave')
#         except:
#             messages.error(request, "Failed to Apply Leave")
#             return redirect('staff_apply_leave')

