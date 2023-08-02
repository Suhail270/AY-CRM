from django.contrib import admin

from .models import (User, 
                     Lead, 
                     Agent, 
                     UserProfile, 
                     Category, 
                     FollowUp, 
                     Parties, 
                     PreferredContact, 
                     UserType, 
                     LeadSource,
                     Lookup_Names,
                     Lookup_Name_Values,
                     TaskAttendees,
                     Task,
                     TaskStatusOptions)



class LeadAdmin(admin.ModelAdmin):

    list_display = ['name', 'party']
    list_display_links = ['name']
    list_editable = ['party']
    list_filter = ['status']
    search_fields = ['name']



admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Agent)
admin.site.register(FollowUp)
admin.site.register(Parties)
admin.site.register(PreferredContact)
admin.site.register(UserType)
admin.site.register(LeadSource)
admin.site.register(Lookup_Names)
admin.site.register(Lookup_Name_Values)
admin.site.register(Task)
admin.site.register(TaskAttendees)
admin.site.register(TaskStatusOptions)
