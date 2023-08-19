from django import forms
from leads.models import (KPI, LeadSource, Targets)
from django.db.models import ForeignKey

def get_fk_model(model, fieldname):
    """Returns None if not foreignkey, otherswise the relevant model"""
    field_object, model, direct, m2m = model._meta.get_field_by_name(fieldname)
    if not m2m and direct and isinstance(field_object, ForeignKey):
        return field_object.rel.to
    return None

class RestrictedConditionInput():
    None

class KpiModelForm(forms.ModelForm):
    # condition2 = None

    class Meta:
        model = KPI 
        fields = [
            "name",
            "record_selection",
            "points_per_record",
            "recipient",
            "condition1",
            "conditionOp",
            "condition2"
        ]
        widgets = {
            "condition2": forms.Select(),
            "points_valueOfField": forms.CheckboxInput()
        }

    def clean(self):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['condition2'].queryset = []
        self.fields['condition1'].label = "Record selection"
        self.fields['conditionOp'].label = ""
        self.fields['condition2'].label = ""

# class KpiForm(forms.Form):
#     None

class TargetModelForm(forms.ModelForm):
    class Meta:
        model = Targets
        fields = (
            'name',
            'related_kpi',
            'time_period',
            'for_org',
            'agents',
        )
        widgets = {
            "for_org": forms.CheckboxInput()
        }

    def clean_first_name(self):
        data = self.cleaned_data["name"]
        return data

    def clean(self):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['for_org'].label = "for entire organization?"
