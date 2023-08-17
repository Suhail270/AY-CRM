from django.shortcuts import render, reverse
import datetime
from django.views import generic
from leads.models import KPI, Targets, Lead, LeadSource
from django.forms.models import model_to_dict
from .forms import (
    KpiModelForm
)
from django.db.models import ForeignKey
from django.http import HttpResponse

def get_fk_model(model, fieldname):
    """Returns None if not foreignkey, otherswise the relevant model"""
    field_object, model, direct, m2m = model._meta.get_field(fieldname)
    if not m2m and direct and isinstance(field_object, ForeignKey):
        return field_object.rel.to
    return None

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
        field = str(kpi.condition1)
        if kpi.record_selection.option == "created":
            record_select = "created_date__gte"
        elif kpi.record_selection.option == "modified":
            record_select = "last_updated_date__gte"
        if str(kpi.conditionOp) == "is":
            field_val = get_foreign(Lead, field).objects.get(pk=kpi.condition2)
            value = Lead.objects.filter(**{field: field_val, record_select: cutoff}).count()
            value = value * kpi.points_per_record
        dic = model_to_dict(kpi)
        dic['value'] = value
        # if value != 0:
        queryset.append(dic)

    return render(request, 'kpis/kpi_list_contents.html', {"kpis": queryset})

def load_cond2(request):
    field = request.GET.get('field')
    foreign = get_foreign(Lead, field)
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

class KpiListView(generic.TemplateView):
    template_name = "kpis/kpi_list.html"


class KpiCreateView(generic.CreateView):
    template_name = "kpis/kpi_create.html"
    form_class = KpiModelForm

    def get_success_url(self):
        return reverse("kpis:kpi-list")

    def get_form(self, form_class=None):
        print([f.name for f in KPI._meta.get_fields()])
        form = super().get_form(form_class)
        return form

    def form_valid(self, form):
        print(self.request.POST)
        kpi = form.save(commit=False)
        kpi.save()
        return super(KpiCreateView, self).form_valid(form)


class TargetListView(generic.ListView):
    template_name = "kpis/target_list.html"
    context_object_name = "targets"

    def get_queryset(self):
        user = self.request.user
        return Targets.objects.all()

class TargetCreateView(generic.TemplateView):
    template_name = "kpis/target_create.html"