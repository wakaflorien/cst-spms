from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from CST_SPMS.models import CustomUser, Projects, Proposals,  StudentGroups, Students, PromotionYear, Supervisors
from .forms import AddStudentForm, EditStudentForm


# def supervisor_home(request):
    

#     subjects = Subjects.objects.filter(staff_id=request.user.id)
#     course_id_list = []
#     for subject in subjects:
#         course = Courses.objects.get(id=subject.course_id.id)
#         course_id_list.append(course.id)
    
#     final_course = []
#     # Removing Duplicate Course Id
#     for course_id in course_id_list:
#         if course_id not in final_course:
#             final_course.append(course_id)
    
#     students_count = Students.objects.filter(course_id__in=final_course).count()
#     subject_count = subjects.count()

#     # Fetch All Attendance Count
#     attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
#     # Fetch All Approve Leave
#     staff = Staffs.objects.get(admin=request.user.id)
#     leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()

#     #Fetch Attendance Data by Subjects
#     subject_list = []
#     attendance_list = []
#     for subject in subjects:
#         attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
#         subject_list.append(subject.subject_name)
#         attendance_list.append(attendance_count1)

#     students_attendance = Students.objects.filter(course_id__in=final_course)
#     student_list = []
#     student_list_attendance_present = []
#     student_list_attendance_absent = []
#     for student in students_attendance:
#         attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
#         attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
#         student_list.append(student.admin.first_name+" "+ student.admin.last_name)
#         student_list_attendance_present.append(attendance_present_count)
#         student_list_attendance_absent.append(attendance_absent_count)

#     context={
#         "students_count": students_count,
#         "attendance_count": attendance_count,
#         "leave_count": leave_count,
#         "subject_count": subject_count,
#         "subject_list": subject_list,
#         "attendance_list": attendance_list,
#         "student_list": student_list,
#         "attendance_present_list": student_list_attendance_present,
#         "attendance_absent_list": student_list_attendance_absent
#     }
#     return render(request, "staff_template/staff_home_template.html", context)