from typing import Any, Dict
from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.template.loader import render_to_string
import datetime
from django.views import generic
from leads.models import KPI, Targets, Lead, LeadSource, Agent, UserProfile, Module, Condition1, Condition2, ConditionOperator, Opportunities
from django.forms.models import BaseModelForm, model_to_dict
from .forms import (
    KpiModelForm,
    KpiForm,
    TargetModelForm
)
from django.db.models import ForeignKey
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.apps import apps

def get_foreign(model, field_name):
    if field_name == "---------":
        return None
    field = model._meta.get_field(field_name)
    field_type = type(field)
    is_foreign = str(field_type) == "<class 'django.db.models.fields.related.ForeignKey'>"
    if is_foreign:
        return field.remote_field.model
    else:
        return None


# ---------

def load_list_contents(request):
    period = int(request.GET.get("period"))

    if request.user.is_organizer:
        organization = request.user.userprofile
    else:
        organization = request.user.agent.organization
    
    cutoff = datetime.date.today() - datetime.timedelta(days=period)

    kpis = KPI.objects.filter(organization = organization)
    queryset = []
    for kpi in kpis:
        module = eval(kpi.module.option)
        og_field = field = str(kpi.condition1)

        if kpi.record_selection.option == "created":
            record_select = "created_date__gte"
        elif kpi.record_selection.option == "modified":
            record_select = "last_updated_date__gte"
        elif kpi.record_selection.option == "converted":
            record_select = "converted_date__gte"

        if str(kpi.conditionOp) == "is":
            model = get_foreign(module, field)
            if model == None:
                field_val = kpi.condition2
            else:
                field_val = model.objects.get(pk=kpi.condition2)
            objects = module.objects.filter(**{field: field_val})#, record_select: cutoff})
        else:
            field_val = kpi.condition2
            if str(kpi.conditionOp) == "greater than or equal to":
                field = field + "__gte"
            elif str(kpi.conditionOp) == "lower than or equal to":
                field = field + "__lte"
            objects = module.objects.filter(**{field: field_val})#, record_select: cutoff})
        if kpi.points_valueOfField:
            value = 0
            for obj in objects:
                value += getattr(obj, og_field)
        else:
            value = objects.count() * kpi.points_per_record
        dic = model_to_dict(kpi)
        dic['value'] = value
        # if value != 0:
        queryset.append(dic)

    return render(request, 'kpis/kpi_list_contents.html', {"kpis": queryset})

def load_targets(request):
    if request.user.is_organizer:
        organization = request.user.userprofile
    else:
        organization = request.user.agent.organization
    
    targets = Targets.objects.filter(organization = organization)
    
    queryset = []
    for target in targets:
        kpi = target.related_kpi
        period_str = target.time_period
        period = 0
        if period_str == "Daily":
            period = 1
        elif period_str == "Weekly":
            period = 7
        elif period_str == "Monthly":
            period = 30
        elif period_str == "Yearly":
            period = 365
        cutoff = datetime.date.today() - datetime.timedelta(days=period)
        # field = str(kpi.condition1)
        # if kpi.record_selection.option == "created":
        #     record_select = "created_date__gte"
        # elif kpi.record_selection.option == "modified":
        #     record_select = "last_updated_date__gte"
        # elif kpi.record_selection.option == "converted":
        #     record_select = "converted_date__gte"
        # if str(kpi.conditionOp) == "is":
        #     field_val = get_foreign(Lead, field).objects.get(pk=kpi.condition2)
        #     value = Lead.objects.filter(**{field: field_val, record_select: cutoff}).count()
        #     value = value * kpi.points_per_record
        # dic = model_to_dict(target)
        # dic['score'] = value
        # queryset.append(dic)


        # module = eval(kpi.module.option)
        module_class = KPI
        og_field = field = str(kpi.condition1)
        kpi_module = kpi.module.option
        module_class = apps.get_model(app_label='leads', model_name='Targets')

        if kpi.record_selection.option == "created":
            record_select = "created_date__gte"
        elif kpi.record_selection.option == "modified":
            record_select = "last_updated_date__gte"
        elif kpi.record_selection.option == "converted":
            record_select = "converted_date__gte"

        if str(kpi.conditionOp) == "is":
            model = get_foreign(module_class, field)
            if model == None:
                field_val = kpi.condition2
            else:
                field_val = model.objects.get(pk=kpi.condition2)
            # objects = module_class.objects.filter(**{field: field_val, record_select: cutoff})
            objects = module_class.objects.filter(**{field: field_val})
        else:
            field_val = kpi.condition2
            if str(kpi.conditionOp) == "greater than or equal to":
                field = field + "__gte"
            elif str(kpi.conditionOp) == "lower than or equal to":
                field = field + "__lte"
            # objects = module.objects.filter(**{field: field_val, record_select: cutoff})
            objects = module_class.objects.filter(**{field: field_val})
        if kpi.points_valueOfField:
            value = 0
            for obj in objects:
                value += getattr(obj, og_field)
        else:
            value = objects.count() * kpi.points_per_record
        dic = model_to_dict(target)
        dic['score'] = value
        # if value != 0:
        queryset.append(dic)
    return render(request, 'kpis/target_list_contents.html', {"targets": queryset})


def load_cond1(request):
    module_option = request.GET.get('module')
    fields = Module.objects.get(option=module_option).fields.all()
    print("@@@@@@@")
    print(fields)
    print("@@@@@@@")
    dics = []
    for field in fields:
        dic = model_to_dict(field)
        dic['str'] = str(field)
        dics.append(dic)
    return render(request, 'kpis/kpi_dropdown_cond2.html', {'field_vals': dics})

def load_cond2(request):
    module = eval(request.GET.get('module'))
    field = request.GET.get('field')
    foreign = get_foreign(module, field)
    if foreign == None:
        field_vals = []
    else:
        field_vals = foreign.objects.all()
    print(field_vals)
    dics = []
    for field_val in field_vals:
        dic = model_to_dict(field_val)
        dic['str'] = str(field_val)
        dics.append(dic)
        print(dic)
    return render(request, 'kpis/kpi_dropdown_cond2.html', {'field_vals': dics})

def load_cond_op(request):
    module = eval(request.GET.get('module'))
    field = request.GET.get('field')
    foreign = get_foreign(module, field)
    if foreign == None:
        is_foreign = False
        field_vals = ConditionOperator.objects.all()
    else:
        is_foreign = True
        field_vals = ConditionOperator.objects.filter(option="is")
    print(field_vals)
    dics = []
    for field_val in field_vals:
        dic = model_to_dict(field_val)
        dic['str'] = str(field_val)
        dics.append(dic)
        print(dic)
    return JsonResponse({"h": render_to_string(request=request, template_name='kpis/kpi_dropdown_cond2.html', context={'field_vals': dics}), "foreign": is_foreign})


class KpiListView(generic.TemplateView):
    template_name = "kpis/kpi_list.html"


# class KpiCreateView(generic.CreateView):
#     template_name = "kpis/kpi_create.html"
#     form_class = KpiModelForm

#     def get_success_url(self):
#         return reverse("kpis:kpi-list")

#     def get_form(self, form_class=None):
#         print([f.name for f in KPI._meta.get_fields()])
#         form = super().get_form(form_class)

#         return form

#     def form_valid(self, form):
#         kpi = form.save(commit=False)
#         user = self.request.user
#         if user.is_organizer:
#             organization = user.userprofile
#         else:
#             organization = user.agent.organization
#         kpi.organization = organization
#         kpi.save()
#         return super(KpiCreateView, self).form_valid(form)


class KpiCreateView(generic.FormView):
    template_name = "kpis/kpi_create.html"
    form_class = KpiForm

    def get_success_url(self):
        return reverse("kpis:kpi-list")

    def get_form(self, form_class=None):
        print([f.name for f in KPI._meta.get_fields()])
        form = super().get_form(form_class)

        return form
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        print(request.POST.get('condition1'))
        print(request.POST.get('conditionOp'))
        print(request.POST.get('condition2'))
        condition1 = request.POST.get('condition1')
        conditionOp = request.POST.get('conditionOp')
        condition2 = request.POST.get('condition2')
        # form.fields['condition1'].choices = [(Condition1.objects.get(pk=condition1), condition1)]
        # form.fields['conditionOp'].choices = [(ConditionOperator.objects.get(pk=conditionOp), conditionOp)]
        # form.fields['condition2'].choices = [(Condition2.objects.get(pk=condition2), condition2)]
        form.fields['condition1'].choices = [(condition1, condition1)]
        form.fields['conditionOp'].choices = [(conditionOp, conditionOp)]
        form.fields['condition2'].choices = [(condition2, condition2)]
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    # def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
    #     print(request.POST.get('condition1'))
    #     print(request.POST.get('conditionOp'))
    #     print(request.POST.get('condition2'))
        
    #     return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        module = form.cleaned_data["module"]
        record_selection = form.cleaned_data["record_selection"]
        points_per_record = form.cleaned_data["points_per_record"]
        # recipient= form.cleaned_data["recipient"]
        condition1 = form.cleaned_data["condition1"]
        conditionOp = form.cleaned_data["conditionOp"]
        points_valueOfField = form.cleaned_data["points_valueOfField"]
        # condition2 = form.cleaned_data["condition2"]

        if points_per_record == 0 or points_per_record == None:
            points_per_record = 1

        module_class = eval(module.option)
        field = str(Condition1.objects.get(pk=condition1))
        if get_foreign(module_class, field) == None:
            condition2 = form.cleaned_data["condition2int"]
        else:
            condition2 = form.cleaned_data["condition2"]

        kpi = KPI(
            name=name,
            module=module,
            record_selection=record_selection,
            points_per_record=points_per_record,
            # recipient=recipient,
            condition1=Condition1.objects.get(pk=condition1),
            conditionOp=ConditionOperator.objects.get(pk=conditionOp),
            # conditionOp=conditionOp,
            condition2=condition2,
            points_valueOfField=points_valueOfField
        )
        user = self.request.user
        if user.is_organizer:
            organization = user.userprofile
        else:
            organization = user.agent.organization
        kpi.organization = organization
        kpi.save()
        return super(KpiCreateView, self).form_valid(form)


class TargetListView(generic.TemplateView):
    template_name = "kpis/target_list.html"

class TargetCreateView(generic.CreateView):
    template_name = "kpis/target_create.html"
    form_class = TargetModelForm

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    
    # def form_invalid(self, form):
    #     return super().form_invalid(form)

    # def get_success_url(self):
    #     return reverse("kpis:target-list")

    def get_success_url(self):
        return reverse("kpis:target-list")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print("DEEEEEEEEfgsgrgsgsdfgEEZ")
    #     print(self.request.user)
    #     context['form'] = self.form_class()
    #     return context
    
    def get_form(self, form_class=TargetModelForm):
        
        print("DEEEEEEEEEEZ")
        print(self.request.user)
        form = super().get_form(form_class)

        # if user.is_organizer:
        #     # form.fields['agents'].queryset = UserProfile.objects.filter(
        #     #     user__is_agent = True
        #     # ).filter(user__agent__organization=user.userprofile)
        #     form.fields['related_kpi'].queryset = KPI.objects.filter(
        #         organization=user.userprofile
        #     )
        #     for thing in form.fields['agents'].queryset:
        #         print(thing.user.is_agent)
        #         print(thing.user.username)
        # else:
        #     form.fields['agents'].queryset = UserProfile.objects.filter(
        #         user=user
        #     )
        #     form.fields['related_kpi'].queryset = KPI.objects.filter(
        #         organization= user.agent.organization
        #     )
            
        return form
    
    def get_form_kwargs(self):
        kwargs = super(TargetCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        target = form.save(commit=False)

        if not self.request.user.is_organizer:
            target.organization = Agent.objects.filter(user=self.request.user)[0].organization
            target.agent = Agent.objects.filter(
                    user=self.request.user
                )[0]
            
        else:
            target.organization = self.request.user.userprofile

        target.save()
        return super(TargetCreateView, self).form_valid(form)
    
class TargetUpdateView(UserPassesTestMixin, generic.UpdateView):
    template_name = 'kpis/target_update.html'
    form_class = TargetModelForm

    def get_success_url(self):
        return reverse("kpis:target-list")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            return Targets.objects.filter(organization=user.userprofile)
        else:
            return Targets.objects.filter(organization=Agent.objects.filter(user=user)[0].organization)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        
        if not user.is_organizer:
            organization = Agent.objects.get(user=user).organization
            form.fields['agents'].queryset = UserProfile.objects.filter(
            user__is_agent=True, user__agent__organization=organization)
        return form
    
    def test_func(self):
        #TEST USER HAS TO PASS
        return self.request.user.is_organizer
        
    def form_valid(self, form):

        target_before_update = self.get_object()
        instance = form.save(commit=False)
        messages.info(self.request, "You have successfully edited this target")
        instance.save()
        return super(TargetUpdateView, self).form_valid(form)
