from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime # To Parse input DateTime into Python Date Time Object

from CST_SPMS.models import CustomUser, StudentGroups,  Students


def group_home(request):
    group_obj = StudentGroups.objects.get(admin=request.user.id)

    
    return render(request, "group_template/group_home_template.html")



# def group_feedback(request):
#     group_obj = groups.objects.get(admin=request.user.id)
#     feedback_data = FeedBackgroup.objects.filter(group_id=group_obj)
#     context = {
#         "feedback_data": feedback_data
#     }
#     return render(request, 'group_template/group_feedback.html', context)


# def group_feedback_save(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method.")
#         return redirect('group_feedback')
#     else:
#         feedback = request.POST.get('feedback_message')
#         group_obj = groups.objects.get(admin=request.user.id)

#         try:
#             add_feedback = FeedBackgroup(group_id=group_obj, feedback=feedback, feedback_reply="")
#             add_feedback.save()
#             messages.success(request, "Feedback Sent.")
#             return redirect('group_feedback')
#         except:
#             messages.error(request, "Failed to Send Feedback.")
#             return redirect('group_feedback')


def group_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    group = StudentGroups.objects.get(admin=user)

    context={
        "user": user,
        "group": group
    }
    return render(request, 'group_template/group_profile.html', context)


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






