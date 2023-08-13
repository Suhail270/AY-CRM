from django.shortcuts import render
from django.views import generic
from leads.models import KPI, Targets, Lead, LeadSource
from django.forms.models import model_to_dict
from .forms import (
    KpiModelForm
)
from django.db.models import ForeignKey

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

def load_cond2(request):
    field = request.GET.get('field')
    foreign = get_foreign(Lead, field)
    if foreign == None:
        field_vals = []
    else:
        field_vals = foreign.objects.all()
    # if field == "source":
    #     field_vals = LeadSource.objects.all()
    # else:
    #     field_vals = [0]
    print(field_vals)
    return render(request, 'kpis/kpi_dropdown_cond2.html', {'field_vals': field_vals})

class KpiListView(generic.ListView):
    template_name = "kpis/kpi_list.html"
    context_object_name = "kpis"

    def get_queryset(self):
        kpis = KPI.objects.all()
        queryset = []
        for kpi in kpis:
            value = 0
            if str(kpi.conditionOp) == "is":
                field = str(kpi.condition1)
                field_val_foreign = str(kpi.condition2)
                field_val = None
                value = Lead.objects.filter(**{field: field_val})
            dic = model_to_dict(kpi)
            dic['value'] = value
            queryset.append(dic)
        return queryset


class KpiCreateView(generic.CreateView):
    template_name = "kpis/kpi_create.html"
    form_class = KpiModelForm

    def get_form(self, form_class=None):
        print([f.name for f in KPI._meta.get_fields()])
        form = super().get_form(form_class)
        return form


class TargetListView(generic.ListView):
    template_name = "kpis/target_list.html"
    context_object_name = "targets"

    def get_queryset(self):
        user = self.request.user
        return Targets.objects.all()

class TargetCreateView(generic.TemplateView):
    template_name = "kpis/target_create.html"