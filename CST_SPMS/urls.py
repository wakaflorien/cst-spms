
from django.urls import path, include
from . import views
from .import HodViews, SupervisorViews, GroupViews


urlpatterns = [
    path('', views.home, name="index"),
    path('group/', views.group, name="group"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.loginPage, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('add_supervisor/', HodViews.add_supervisor, name="add_supervisor"),
    path('add_supervisor_save/', HodViews.add_supervisor_save, name="add_supervisor_save"),
    path('manage_supervisor/', HodViews.manage_supervisor, name="manage_supervisor"),
    path('edit_supervisor/<supervisor_id>/', HodViews.edit_supervisor, name="edit_supervisor"),
    path('edit_supervisor_save/', HodViews.edit_supervisor_save, name="edit_supervisor_save"),
    path('delete_supervisor/<supervisor_id>/', HodViews.delete_supervisor, name="delete_supervisor"),
    path('add_group/', HodViews.add_group, name="add_group"),
    path('add_group_save/', HodViews.add_group_save, name="add_group_save"),
    path('manage_group/', HodViews.manage_group, name="manage_group"),
    path('edit_group/<group_id>/', HodViews.edit_group, name="edit_group"),
    path('edit_group_save/', HodViews.edit_group_save, name="edit_group_save"),
    path('delete_group/<group_id>/', HodViews.delete_group, name="delete_group"),

    path('export_csv/', HodViews.export_csv, name="export_csv"),
    path('export_pdf/', HodViews.export_pdf, name="export_pdf"),


    path('export_csv_sup/', HodViews.export_csv_sup, name="export_csv_sup"),
    path('export_pdf_sup/', HodViews.export_pdf_sup, name="export_pdf_sup"),
    # path('manage_session/', HodViews.manage_session, name="manage_session"),
    # path('add_session/', HodViews.add_session, name="add_session"),
    # path('add_session_save/', HodViews.add_session_save, name="add_session_save"),
    # path('edit_session/<session_id>', HodViews.edit_session, name="edit_session"),
    # path('edit_session_save/', HodViews.edit_session_save, name="edit_session_save"),
    # path('delete_session/<session_id>/', HodViews.delete_session, name="delete_session"),
    path('add_student/', HodViews.add_student, name="add_student"),
    path('add_student_save/', HodViews.add_student_save, name="add_student_save"),
    # path('edit_student/<student_id>', HodViews.edit_student, name="edit_student"),
    # path('edit_student_save/', HodViews.edit_student_save, name="edit_student_save"),
    path('manage_student/', HodViews.manage_student, name="manage_student"),
    # path('delete_student/<student_id>/', HodViews.delete_student, name="delete_student"),
    
    path('check_email_exist/', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', HodViews.check_username_exist, name="check_username_exist"),

    path('group_feedback_message/', SupervisorViews.group_feedback_message, name="group_feedback_message"),
    path('group_feedback_message_reply/', SupervisorViews.group_feedback_message_reply, name="group_feedback_message_reply"),

    path('supervisor_feedback_message/', HodViews.supervisor_feedback_message, name="supervisor_feedback_message"),
    path('supervisor_feedback_message_reply/', HodViews.supervisor_feedback_message_reply, name="supervisor_feedback_message_reply"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HodViews.admin_profile_update, name="admin_profile_update"),
    


    # # URLS for Staff
    path('supervisor_home/', SupervisorViews.supervisor_home, name="supervisor_home"),
    path('supervisor_manage_proposal/', SupervisorViews.supervisor_manage_proposal, name="supervisor_manage_proposal"),
    path('supervisor_assigned_group/', SupervisorViews.supervisor_assigned_group, name="supervisor_assigned_group"),
    # path('supervisor_contact_group/', SupervisorViews.supervisor_contact_group, name="supervisor_contact_group"),
    # path('supervisor_contact_hod/', SupervisorViews.supervisor_contact_hod, name="supervisor_contact_hod"),
    path('supervisor_feedback/', SupervisorViews.supervisor_feedback, name="supervisor_feedback"),
    path('supervisor_feedback_save/', SupervisorViews.supervisor_feedback_save, name="supervisor_feedback_save"),

    path('supervisor_profile/', SupervisorViews.supervisor_profile, name="supervisor_profile"),
    path('supervisor_profile_update/', SupervisorViews.supervisor_profile_update, name="supervisor_profile_update"),

    # URSL for Groups
    path('group_home/', GroupViews.group_home, name="group_home"),
    path('group_profile/', GroupViews.group_profile, name="group_profile"),
    path('group_profile_update/', GroupViews.group_profile_update, name="group_profile_update"),
    path('add_member/', GroupViews.add_member, name="add_member"),
    path('add_member_save/', GroupViews.add_member_save, name="add_member_save"),
    path('edit_member/<student_id>', GroupViews.edit_member, name="edit_member"),
    path('edit_member_save/', GroupViews.edit_member_save, name="edit_member_save"),
    path('manage_member/', GroupViews.manage_member, name="manage_member"),
    
    path('add_proposal/', GroupViews.add_proposal, name="add_proposal"),
    path('add_proposal_save/', GroupViews.add_proposal_save, name="add_proposal_save"),
    path('manage_proposal/', GroupViews.manage_proposal, name="manage_proposal"),
    path('edit_proposal/<proposal_id>/', GroupViews.edit_proposal, name="edit_proposal"),
    path('edit_proposal_save/', GroupViews.edit_proposal_save, name="edit_proposal_save"),
    path('delete_proposal/<proposal_id>/', GroupViews.delete_proposal, name="delete_proposal"),
    # path('delete_member/<member_id>/', GroupViews.delete_member, name="delete_member"),
    # path('student_view_attendance_post/', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    # path('student_apply_leave/', StudentViews.student_apply_leave, name="student_apply_leave"),
    # path('student_apply_leave_save/', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('group_feedback/', GroupViews.group_feedback, name="group_feedback"),
    path('group_feedback_save/', GroupViews.group_feedback_save, name="group_feedback_save"),

    # path('student_view_result/', StudentViews.student_view_result, name="student_view_result"),
]
