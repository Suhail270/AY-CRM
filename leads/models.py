from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class PreferredContact(models.Model):
    choice = models.CharField(max_length=100)

    objects = LeadManager()

    def __str__(self):
        return f"{self.choice}"
    
class UserType(models.Model):
    type = models.CharField(max_length=100)

    objects = LeadManager()

    def __str__(self):
        return f"{self.type}"
    
class LeadSource(models.Model):
    type = models.CharField(max_length=100)

    objects = LeadManager() # Website, Referral, Walkin, Campaign

    def __str__(self):
        return f"{self.type}"
    
class Parties(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.ForeignKey(UserType, null=True, blank=True, on_delete=models.SET_NULL) # Individual, Organization
    primary_number = models.CharField(max_length=30)
    whatsapp_number = models.CharField(max_length=30)
    email = models.EmailField()
    preferred_contact_method = models.ForeignKey("PreferredContact", null=True, blank=True, on_delete=models.SET_NULL) # Email, WhatsApp, Call
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(default=datetime.now)
    last_updated_date = models.DateTimeField(default=datetime.now)
    tenant_map_id = models.IntegerField(default=1)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")

    objects = LeadManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Lead(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.ForeignKey("Category", null=True, on_delete=models.SET_NULL, default='New')
    organization = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    source = models.ForeignKey(LeadSource, null=True, blank=False, on_delete=models.SET_NULL)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(default=datetime.now)
    last_updated_date = models.DateTimeField(default=datetime.now)
    converted_date = models.DateTimeField(null=True, blank=True)

    party = models.ForeignKey("Parties", related_name="leads", null=True, blank=False, on_delete=models.SET_NULL)
    tenant_map_id = models.IntegerField(default=1)

    objects = LeadManager()

    def __str__(self):
        return f"{self.name}"


def handle_upload_follow_ups(instance, filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"


class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, related_name="followups", null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)

    def __str__(self):
        return f"{self.lead.name}"


class Agent(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.email
    
    def delete(self, *args, **kwargs):
        user = self.user
        user_profile = self.user.userprofile
        super().delete(*args, **kwargs)
        user.delete()
        user_profile.delete()
    


class Category(models.Model):
    name = models.CharField(max_length=30, default="New")  # Qualified, New, Contacted, Converted, Lost
    organization = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

class Lookup_Names(models.Model):
    lookup_names_id = models.AutoField(primary_key=True)
    field_name = models.CharField(max_length=100, null=True, blank=False)
    name = models.CharField(max_length=100, null=True, blank=False)
    description = models.CharField(max_length=240, null=True, blank=True)
    created_by = models.IntegerField(default=-1, null=True, blank=False)
    created_date = models.DateTimeField(default=datetime.now, null=True, blank=False)
    last_updated_date = models.DateTimeField(default=datetime.now, null=True, blank=False)
    app_id = models.IntegerField(default=1, null=True, blank=False)

    def __str__(self):
        return str(self.name)

class Lookup_Name_Values(models.Model):
    code = models.CharField(max_length=30, null=True, blank=False)
    meaning = models.CharField(max_length=240, null=True, blank=False)
    description = models.CharField(max_length=240, null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    enabled_flag = models.CharField(max_length=1, null=True, blank=True) 
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_by = models.IntegerField(default=-1, null=True, blank=False)
    created_date = models.DateTimeField(default=datetime.now, null=True, blank=False)
    last_updated_date = models.DateTimeField(default=datetime.now, null=True, blank=False)
    lookup_names_id = models.ForeignKey(Lookup_Names,null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Code: " + str(self.code) + " | Lookup name: " + str(self.lookup_names_id.name)
    

# Task Management:

class TaskStatusOptions(models.Model):
    option = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.option)
    
class RepeatOptions(models.Model):
    option = models.CharField(max_length=100)

class Task(models.Model):
    owner = models.ForeignKey(UserProfile, null=True, blank=False, on_delete=models.SET_NULL, related_name='owner')
    organization =  models.ForeignKey(UserProfile, null=True, blank=False, on_delete=models.SET_NULL, related_name='organization')
    title = models.CharField(max_length=100, null=False, blank=False)
    designated_lead = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name='designatedLead')
    creation_date = models.DateTimeField(default=datetime.now, null=False, blank=False)
    start_date = models.DateTimeField(default=datetime.now, null=False, blank=False)
    deadline = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    invitees = models.ManyToManyField(UserProfile)
    status = models.ForeignKey(TaskStatusOptions, null=True, blank=True, on_delete=models.SET_NULL)
    referenceNotes = models.CharField(max_length=500, null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    repeat = models.ForeignKey(RepeatOptions, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.designated_lead:
            return str(self.title) + " | " + str(self.owner) + ": " + str(self.designated_lead)
        else:
            return str(self.title) + " | " + str(self.owner)
        

class TaskAttendees(models.Model):
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.SET_NULL)
    participant = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.task.title) + " - " + str(self.attendee.user.username)

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)