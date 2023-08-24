from django import forms
from leads.models import (KPI, LeadSource, Opportunities, Targets, UserProfile, Condition1, ConditionOperator, Condition2, Module, RecordSelection, Recipient)
from django.db.models import ForeignKey

def get_fk_model(model, fieldname):
    """Returns None if not foreignkey, otherswise the relevant model"""
    field_object, model, direct, m2m = model._meta.get_field_by_name(fieldname)
    if not m2m and direct and isinstance(field_object, ForeignKey):
        return field_object.rel.to
    return None

class RestrictedConditionInput():
    None

class KpiForm(forms.Form):
    name =  forms.CharField(max_length=100)
    module = forms.ModelChoiceField(queryset=Module.objects.all())
    record_selection = forms.ModelChoiceField(queryset=RecordSelection.objects.all())
    points_val_select = forms.BooleanField(label="Set custom value", required=False)
    points_valueOfField = forms.BooleanField(label="Use value of the field as points", required=False)
    points_per_record = forms.IntegerField(label="Set points per record", required=False)
    # recipient = forms.ModelChoiceField(queryset=Recipient.objects.all())
    condition1 = forms.ChoiceField(label="Condition")
    conditionOp = forms.ChoiceField(label="")
    condition2 = forms.ChoiceField(label="", required=False)
    condition2int = forms.IntegerField(required=False)

# class KpiModelForm(forms.ModelForm):
#     # condition2 = None

#     class Meta:
#         model = KPI 
#         fields = [
#             "name",
#             "module",
#             "record_selection",
#             "points_per_record",
#             "recipient",
#             "condition1",
#             "conditionOp",
#             "condition2"
#         ]
#         widgets = {
#             "condition2": forms.Select(),
#             "points_valueOfField": forms.CheckboxInput()
#         }

#     def clean(self):
#         pass

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['condition1'].queryset = Condition1.objects.none()
#         self.fields['condition2'].queryset = Condition2.objects.none()
#         self.fields['condition1'].label = "Condition"
#         self.fields['conditionOp'].label = ""
#         self.fields['condition2'].label = ""

class TargetModelForm(forms.ModelForm):
    class Meta:
        model = Targets
        fields = (
            'name',
            'related_kpi',
            'target_points',
            'time_period',
            'for_org',
            'agents'
            # 'organization'
        )
        widgets = {
            "for_org": forms.CheckboxInput(),
            'agents': forms.CheckboxSelectMultiple()
        }

    def clean_first_name(self):
        data = self.cleaned_data["name"]
        return data

    # def clean(self):
    #     pass

    def __init__(self, *args, **kwargs):
        print("HEEEEREREREERE")
        self.user = kwargs.pop('user', None)
        user_var = self.user
        print("#########")
        # print(self.user)
        # print(self.user.userprofile)
        print("########!")
        super(TargetModelForm, self).__init__(*args, **kwargs)
        self.fields['for_org'].label = "for entire organization?"
        agent_queryset = UserProfile.objects.filter(
            user__is_agent = True
        ).filter(user__agent__organization=user_var.userprofile)
        self.fields['agents'].queryset = agent_queryset
        print("hereherehereherehereheerehere")
        # if self.user.is_organizer:
        #     # form.fields['agents'].queryset = UserProfile.objects.filter(
        #     #     user__is_agent = True
        #     # ).filter(user__agent__organization=user.userprofile)
        #     self.fields['related_kpi'].queryset = KPI.objects.filter(
        #         organization=self.user.userprofile
        #     )
        #     for thing in self.fields['agents'].queryset:
        #         print(thing.user.is_agent)
        #         print(thing.user.username)
        # else:
        #     self.fields['agents'].queryset = UserProfile.objects.filter(
        #         user=self.user
        #     )
        #     self.fields['related_kpi'].queryset = KPI.objects.filter(
        #         organization= self.user.agent.organization
        #     )
