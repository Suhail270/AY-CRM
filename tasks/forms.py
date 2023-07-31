from django import forms
from leads.models import Task

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'title',
            'location',
            'all_day',
            'start_date',
            'start_time',
            'end_date',
            'end_time',
            'travel_time',
            'repeat',
            'invitees',
            'alert',
            'showAs',
            'referenceURL',
            'referenceNotes'
        )

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data

    def clean(self):
        pass