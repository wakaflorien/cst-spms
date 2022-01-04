from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHOD, Supervisors, Groups, Projects, Proposals, Students, Attendance, AttendanceReport, LeaveReportStudent, LeaveReportStaff, FeedBackStudent, FeedBackSupervisors, NotificationStudent, NotificationSupervisors

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Supervisors)
admin.site.register(Groups)
admin.site.register(Projects)
admin.site.register(Proposals)
admin.site.register(Students)

admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackStudent)
# admin.site.register(FeedBackSupervisors)
admin.site.register(NotificationStudent)
# admin.site.register(NotificationSupervisors)
