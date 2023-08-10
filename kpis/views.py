from django.shortcuts import render
from django.views import generic
from leads.models import KPI, Targets

class KpiListView(generic.ListView):
    template_name = "kpis/kpi_list.html"
    context_object_name = "kpis"

    def get_queryset(self):
        user = self.request.user
        return KPI.objects.all()


class KpiCreateView(generic.TemplateView):
    template_name = "kpis/kpi_create.html"

class TargetListView(generic.ListView):
    template_name = "kpis/target_list.html"
    context_object_name = "targets"

    def get_queryset(self):
        user = self.request.user
        return Targets.objects.all()

class TargetCreateView(generic.TemplateView):
    template_name = "kpis/target_create.html"