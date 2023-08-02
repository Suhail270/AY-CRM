from django import forms
from leads.models import (Task,
                        #   TravelTimeOptions,
                        #   RepeatOptions,
                        #   AlertOptions,
                        #   CalendarDisplayOptions
                          )

# class TaskForm(forms.Form):
#     title = forms.CharField(label="Title", max_length=100,  required=True)
#     location = forms.CharField(label="Location", max_length=100,  required=True)
#     all_day = forms.BooleanField(label="All day", required=True)
#     start_date = forms.DateField(label="Start date", required=True)
#     start_time = forms.TimeField(label="Start time", required=False)
#     end_date = forms.DateField(label="Start date", required=True)
#     end_time = forms.TimeField(label="Start time", required=False)
#     travel_time = forms.ModelChoiceField(queryset=TravelTimeOptions.objects.all())
#     # repeat
#     # invitees
#     # alert
#     # showAs
#     referenceURL = "test"
#     referenceNotes = "test"
#     task = Task(
#         title=title,
#         location=location,
#         all_day=all_day,
#         start_date=start_date,
#         start_time=start_time,
#         end_date=end_date,
#         end_time=end_time,
#         travel_time=travel_time,
#         referenceURL=referenceURL,
#         referenceNotes=referenceNotes
#     )

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'designated_lead',
            'start_date',
            'deadline',
            'end_date',
            'invitees',
            'status',
            'referenceNotes',
        ]
        widgets = {
            "start_date": forms.DateInput(),
            "end_date": forms.DateInput(),
        }

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data

    def clean(self):
        pass