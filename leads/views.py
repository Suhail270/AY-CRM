import logging
import datetime
from typing import Any, Dict
from django import contrib
from django.contrib import messages
from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganizerAndLoginRequiredMixin
from .models import Lead, Agent, Category, FollowUp, Parties ,Opportunities,UserProfile
from .forms import (
    LeadForm, 
    LeadModelForm, 
    CustomUserCreationForm, 
    AssignAgentForm, 
    LeadCategoryUpdateForm,
    CategoryModelForm,
    FollowUpModelForm,
    OpportunityModelForm,
    OpportunityUpdateModelForm
)
from django.db.models import Q


logger = logging.getLogger(__name__)


# CRUD+L - Create, Retrieve, Update and Delete + List

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_agent:
                return redirect("leads:lead-list")
            elif request.user.is_organizer:
                return redirect("dashboard")

        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, generic.TemplateView):

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization, 
                agent__isnull=False
            )

        # How many leads we have in total
        total_lead_count = queryset.filter(organization=user.userprofile).count()

        # How many new leads in the last 30 days
        thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)

        total_in_past30 = queryset.filter(
            organization=user.userprofile,
            created_date__gte=thirty_days_ago
        ).count()

        # How many converted leads in the last 30 days
        converted_category = Category.objects.get(name="Converted", organization=user.userprofile)
        converted_in_past30 = queryset.filter(
            organization=user.userprofile,
            status=converted_category,
            converted_date__gte=thirty_days_ago
        ).count()

        all_categories = []
        
        for i in Category.objects.all():
            all_categories.append(str(i))
            category_count = Category.objects.get(name=i, organization=user.userprofile)
            category_count.count = queryset.filter(status__name__exact=i).count()
            category_count.save()

        context.update({
            "total_lead_count": total_lead_count,
            "total_in_past30": total_in_past30,
            "converted_in_past30": converted_in_past30,
            "qs": Category.objects.filter(organization__exact=user.userprofile)
        })
        return context
 

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context



class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        # Agent.objects.filter(user=user)[0].organization

        if user.is_organizer:
            form.fields['status'].queryset = Category.objects.filter(
            organization=user.userprofile
            )
            form.fields['agent'].queryset = Agent.objects.filter(
                organization=user.userprofile
            )
            form.fields['party'].queryset = Parties.objects.filter(
                organization=user.userprofile
            )
        
        else:
            organization = Agent.objects.filter(user=user)[0].organization

            form.fields['status'].queryset = Category.objects.filter(
            organization=organization
            )
            form.fields['agent'].queryset = Agent.objects.filter(
                user=user
            )
            form.fields['party'].queryset = Parties.objects.filter(
                organization=organization
            ).filter(Q(agent=Agent.objects.filter(user=user)[0]) | Q(agent=None))
            
        return form

    def form_valid(self, form):
        lead = form.save(commit=False)

        if not self.request.user.is_organizer:
            lead.organization = Agent.objects.filter(user=self.request.user)[0].organization
            lead.agent = Agent.objects.filter(
                user=self.request.user
            )[0]
        
        else:
            lead.organization = self.request.user.userprofile

        lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            return Lead.objects.filter(organization=user.userprofile)
        else:
            return Lead.objects.filter(organization=Agent.objects.filter(user=user)[0].organization)

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        
        if user.is_organizer:
            form.fields['status'].queryset = Category.objects.filter(
            organization=user.userprofile
            )
            form.fields['agent'].queryset = Agent.objects.filter(
                organization=user.userprofile
            )
            form.fields['party'].queryset = Parties.objects.filter(
                organization=user.userprofile
            )
        
        else:
            organization = Agent.objects.filter(user=user)[0].organization

            form.fields['status'].queryset = Category.objects.filter(
            organization=organization
            )
            form.fields['agent'].queryset = Agent.objects.filter(
                user=user
            )
            form.fields['party'].queryset = Parties.objects.filter(
                organization=organization
            ).filter(Q(agent=Agent.objects.filter(user=user)[0]) | Q(agent=None))

        return form

    def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        messages.info(self.request, "You have successfully updated this lead")
        if lead_before_update.last_updated_date != datetime.datetime.now():
                # this lead has now been converted
                instance.last_updated_date = datetime.datetime.now()
        instance.save()
        return super(LeadUpdateView, self).form_valid(form)


class LeadDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        return Lead.objects.filter(organization=user.userprofile)

class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization
            )

        for category_name in self.object_list:
            category_count = Lead.objects.filter(status__name__exact=category_name).count()

        context.update({
            "unassigned_lead_count": queryset.filter(agent__isnull=True).count(),
            "new_lead_count": queryset.filter(status__name__exact="New").count(),
            "contacted_lead_count": queryset.filter(status__name__exact="Contacted").count(),
            "converted_lead_count": queryset.filter(status__name__exact="Converted").count(),
            "qualified_lead_count": queryset.filter(status__name__exact="Qualified").count(),
            "lost_lead_count": queryset.filter(status__name__exact="Lost").count(),
        })

        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization
            )

        pk = self.kwargs['pk']
        for i in Category.objects.filter(id=pk):
            category_name = i

        context.update({
            "category_count": queryset.filter(status__exact=category_name),
        })
        
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class CategoryCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class CategoryDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_form_kwargs(self):
        kwargs = super(LeadCategoryUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        user = self.request.user
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = Category.objects.get(name="Converted", organization=user.userprofile)
        if form.cleaned_data["status"] == converted_category:
            # update the date at which this lead was converted
            if lead_before_update.status != converted_category:
                # this lead has now been converted
                instance.converted_date = datetime.datetime.now()
        instance.save()
        return super(LeadCategoryUpdateView, self).form_valid(form)


class FollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)


class FollowUpUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/followup_update.html"
    form_class = FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = FollowUp.objects.filter(lead__organization=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().lead.id})


class FollowUpDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("leads:lead-detail", kwargs={"pk": followup.lead.pk})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = FollowUp.objects.filter(lead__organization=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

class LeadJsonView(generic.View):

    def get(self, request, *args, **kwargs):
        
        qs = list(Lead.objects.all().values(
            "first_name", 
            "last_name", 
            "age")
        )

        return JsonResponse({
            "qs": qs,
        })
    

# class OpportunityListView(LoginRequiredMixin, generic.ListView):
#     template_name = "leads/opportunity_list.html"
#     context_object_name = "opportunities"

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Lead.objects.filter(
#             party__isnull = False,
#             party__first_name__isnull = False,
#             party__email__isnull = False,
#             party__primary_number__isnull = False
#         ) | Lead.objects.filter(
#             party__isnull = False,
#             party__first_name__isnull = False,
#             party__email__isnull = False,
#             party__whatsapp_number__isnull = False
#         )
#         self.create_queryOpportunities(queryset)
#         queryset2 = Opportunities.objects.filter(
#             party__isnull = False,
#         )
#         return queryset2
    
#     def create_queryOpportunities(self, queryset):
#         for lead in queryset:
#             existing_opportunity = Opportunities.objects.filter(
#             name=lead.name,
#             source=lead.source,
#             status=lead.status,
#             agent_id = lead.agent_id,
#             organization_id = lead.organization_id,
#             party_id = lead.party_id,
#             source_id = lead.source_id          
#         ).first()
#             if not existing_opportunity:
#                 # Create an Opportunity instance for each lead and set the relevant fields
#                 opportunity = Opportunities()
#                 opportunity.name = lead.name
#                 opportunity.description = lead.description
#                 opportunity.source = lead.source
#                 opportunity.status = lead.status
#                 opportunity.agent = lead.agent
#                 opportunity.organization = lead.organization
#                 opportunity.party = lead.party
#                 opportunity.tenant_map_id = lead.tenant_map_id

#                 # Save the Opportunity instance to the database
#                 opportunity.save()

class OpportunityListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/opportunity_list.html"
    context_object_name = "opportunities"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Opportunities.objects.filter(
                organization=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Opportunities.objects.filter(
                organization=user.agent.organization, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super(OpportunityListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Opportunities.objects.filter(
                organization=user.userprofile, 
                agent__isnull=True
            )
            # context.update({
            #     "unassigned_leads": queryset
            # })
        return context

              

class OpportunityConvertView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/opportunity_convert.html"
    form_class = OpportunityModelForm
     
    def get_initial(self):
        curr_lead = Lead.objects.get(pk=self.kwargs["pk"])
        name = curr_lead.name
        description = curr_lead.description
        status = Category.objects.get(name="Converted")
        organization = curr_lead.organization
        source = curr_lead.source
        agent = curr_lead.agent
        party = curr_lead.party
        
        return {
            "name": name,
            "description": description,
            "status": Category.objects.get(name="Converted"),
            "source": source,
        }
    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(OpportunityConvertView, self).get_context_data(**kwargs)
        curr_lead = Lead.objects.get(pk=self.kwargs["pk"])
        curr_party = curr_lead.party
        context.update({

            "name": curr_lead.name,
            "description": curr_lead.description,
            "status": Category.objects.get(name="Converted"),
            "organization" : curr_lead.organization,
            "source": curr_lead.source,
            "agent": curr_lead.agent,
            "party": curr_lead.party,
            "converted_date" : datetime.datetime.now,
            "tenant_map_id" : curr_lead.tenant_map_id,
            "original_lead": curr_lead,
            
        })
        return context

    def form_valid(self, form):
        curr_lead = Lead.objects.get(pk=self.kwargs["pk"])
        opportunity = form.save(commit=False)
        opportunity.name = curr_lead.name
        opportunity.description = curr_lead.description
        opportunity.status = Category.objects.get(name="Converted")
        opportunity.organization = curr_lead.organization
        opportunity.source = curr_lead.source
        opportunity.agent = curr_lead.agent
        opportunity.party = curr_lead.party
        opportunity.tenant_map_id = curr_lead.tenant_map_id
        opportunity.converted_date = datetime.datetime.now()
        opportunity.original_lead = curr_lead
        opportunity.save()
        user = self.request.user
        converted_category = Category.objects.get(name="Converted")
        curr_lead.status = converted_category
        curr_lead.converted_date = datetime.datetime.now()
        curr_lead.save()
        return super(OpportunityConvertView, self).form_valid(form)

   
class OpportunityUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/opportunity_update.html"
    form_class = OpportunityUpdateModelForm
    context_object_name = "opportunities"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        queryset = Opportunities.objects.all()
        if user.is_agent:
            queryset = queryset.filter(agent=Agent.objects.get(user = user))
        return queryset
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        return form

    def get_success_url(self):
        return reverse("leads:opportunity-list")

    def form_valid(self, form):
        updatedTask = self.get_object()
        instance = form.save(commit=False)
        messages.info(self.request, "You have successfully updated this opportunity")
        if instance.last_updated_date != datetime.datetime.now():
            instance.last_updated_date = datetime.datetime.now()
        instance.save()
        return super(OpportunityUpdateView, self).form_valid(form)

class OpportunityDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/opportunity_detail.html"
    context_object_name = "opportunity"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Opportunities.objects.filter(organization=user.userprofile)
        else:
            queryset = Opportunities.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

class OppFollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:opportunity-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(OppFollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "opportunity": Opportunities.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        opportunity = Opportunities.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.opportunity = opportunity
        followup.save()
        return super(OppFollowUpCreateView, self).form_valid(form)


class OppFollowUpUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/followup_update.html"
    form_class = FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = FollowUp.objects.filter(opportunity__organization=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(opportunity__organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(opportunity__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:opportunity-detail", kwargs={"pk": self.get_object().opportunity.id})


class TimelineView(LoginRequiredMixin, generic.TemplateView):

    template_name = "leads/timeline.html"

    def get_context_data(self, **kwargs):
        context = super(TimelineView, self).get_context_data(**kwargs)

        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization, 
                agent__isnull=False
            )

        # How many leads we have in total
        if user.is_organizer:
            curr_lead = queryset.filter(organization=user.userprofile, id = self.kwargs["pk"]).first()
        else :
            curr_lead = queryset.filter(agent=user.agent, id = self.kwargs["pk"]).first()
        
        curr_opp = None
        if curr_lead.converted_date is not None:
            print("not none")
            if user.is_organizer:
                curr_opp = Opportunities.objects.filter(
                    organization=user.userprofile, 
                    agent__isnull=False,
                    original_lead = curr_lead,
                ).first()
            else:
                curr_opp = Opportunities.objects.filter(
                    agent=user.agent, 
                    agent__isnull=False,
                    original_lead = curr_lead,
                ).first()


        

    

        context.update({
            "curr_lead": curr_lead,
            "qs": Category.objects.filter(organization__exact=user.userprofile),
            "curr_opp": curr_opp
        })
        return context
 
class OppTimelineView(LoginRequiredMixin, generic.TemplateView):

    template_name = "leads/timeline.html"

    def get_context_data(self, **kwargs):
        context = super(OppTimelineView, self).get_context_data(**kwargs)

        user = self.request.user

        if user.is_organizer:
            queryset = Opportunities.objects.filter(
                organization=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Opportunities.objects.filter(
                organization=user.agent.organization, 
                agent__isnull=False
            )

        # How many leads we have in total
        curr_opp = None
        curr_lead = None
        if user.is_organizer:
            curr_opp = queryset.filter(organization=user.userprofile, id = self.kwargs["pk"]).first()
            curr_lead = curr_opp.original_lead      

        else :
            curr_opp = queryset.filter(agent=user.agent, id = self.kwargs["pk"]).first()
            curr_lead = curr_opp.original_lead    


        

    

        context.update({
            "curr_lead": curr_lead,
            "qs": Category.objects.filter(organization__exact=user.userprofile),
            "curr_opp": curr_opp
        })
        return context
 
