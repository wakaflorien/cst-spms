from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver



class PromotionYear(models.Model):
    id = models.AutoField(primary_key=True)
    promotion_end_year = models.DateField()
    
    objects = models.Manager()



# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Supervisor"), (3, "Group"), (4, "Student") )
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)



class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=50)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class StudentGroups(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    group_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class Supervisors(models.Model):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=50)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    # address = models.TextField()
    # group_id = models.ForeignKey(StudentGroups, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()






class Proposals(models.Model):
    id =models.AutoField(primary_key=True)
    proposal_title = models.CharField(max_length=255)
    promotion = models.OneToOneField(PromotionYear, on_delete=CASCADE)
    studentgroup_id = models.ForeignKey(StudentGroups, on_delete=models.CASCADE, default=1) #need to give defauult group
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Projects(models.Model):
    id =models.AutoField(primary_key=True)
    projeject_title = models.CharField(max_length=255)
    project_pic = models.FileField()
    promotion = models.OneToOneField(PromotionYear, on_delete=CASCADE)
    proposal_id = models.ForeignKey(Proposals, on_delete=models.CASCADE, default=1) #need to give defauult proposal
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()





class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50)
    student_group = models.ForeignKey(StudentGroups, on_delete=CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()




class FeedBackGroup(models.Model):
    id = models.AutoField(primary_key=True)
    studentgroup_id = models.ForeignKey(StudentGroups, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class FeedBackHOD(models.Model):
    id = models.AutoField(primary_key=True)
    hod_id = models.ForeignKey(AdminHOD, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackSupervisor(models.Model):
    id = models.AutoField(primary_key=True)
    supervisor_id = models.ForeignKey(Supervisors, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class NotificationGroup(models.Model):
    id = models.AutoField(primary_key=True)
    studentgroup_id = models.ForeignKey(StudentGroups, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationSupervisors(models.Model):
    id = models.AutoField(primary_key=True)
    supervisor_id = models.ForeignKey(Supervisors, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()




#Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, supervisor,group or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Supervisors.objects.create(admin=instance)
        if instance.user_type == 3:
            StudentGroups.objects.create(admin=instance)
        if instance.user_type == 4:
            Students.objects.create(admin=instance)
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.supervisors.save()
    if instance.user_type == 3:
        instance.studentgroups.save()
    if instance.user_type == 4:
        instance.students.save()


