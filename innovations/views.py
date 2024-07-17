from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Innovation
from .forms import *
from django.contrib import messages
from django.apps import apps
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView, CreateView
from django.urls import reverse
from django.http import Http404, HttpResponse
from django.views.generic.edit import FormView, FormMixin
from django.views.generic.list import ListView, BaseListView
from django.views.generic.base import TemplateResponseMixin
from django.forms import ValidationError
from .filters import BaseFilter
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)



Network_member= apps.get_model('users', 'Network_member')


def innovations(request):
  myinnovations = Innovation.objects.all().values()
  template = loader.get_template('innovations.html')
  context = {
    'myinnovations': myinnovations
  }
  return HttpResponse(template.render(context, request))
  
def innov_details(request, id):
  myinnovation = Innovation.objects.get(id=id)
  template = loader.get_template('innov_details.html')
  context = {
    'myinnovation': myinnovation
  }
  return HttpResponse(template.render(context, request))


def submit(request):
  form = InnovationForm()
  template= loader.get_template("submit_innovation.html")
  network_members= Network_member.objects.values_list("user_id", flat=True)
  context= {"form": form, "network_members": network_members}
  return HttpResponse(template.render(context, request))
  
  
def submit_innovation(request):
  form = InnovationForm()
  x= request.POST.get("Τίτλος")
  Φορέας= request.POST["Φορέας"]
  Επίπεδο= request.POST["Επίπεδο"]
  Περιγραφή= request.POST["Περιγραφή"]
  Τομέας= request.POST["Τομέας"]
  Τύπος= request.POST["Τύπος"]
  Στάδιο= request.POST["Στάδιο"]
  Στόχοι= request.POST["Στόχοι"]
  Αποτελέσματα= request.POST["Αποτελέσματα"]
  Σχεδιασμός= request.POST["Σχεδιασμός"]
  Πειραματική_εφαρμογή= request.POST["Πειραματική_εφαρμογή"]
  Εφαρμογή= request.POST["Εφαρμογή"]
  Διάδοση= request.POST["Διάδοση"]
  Χρηματοδότηση= request.POST["Χρηματοδότηση"]
  user= User(request.user.id)
  network_member= Network_member.objects.get(user_id=user.pk)
  innovation= Innovation(Τίτλος=x, Φορέας=Φορέας, Επίπεδο=Επίπεδο, Περιγραφή=Περιγραφή, Τομέας=Τομέας, Τύπος=Τύπος,
                         Στάδιο=Στάδιο, Στόχοι=Στόχοι, Αποτελέσματα=Αποτελέσματα, Σχεδιασμός=Σχεδιασμός, Πειραματική_εφαρμογή=Πειραματική_εφαρμογή,
                         Εφαρμογή=Εφαρμογή, Διάδοση=Διάδοση, Χρηματοδότηση=Χρηματοδότηση, network_member=network_member)

  innovation.save()
  messages.success(request, ('Η υποβολή των στοιχείων για την καινοτομία πραγματοποιήθηκε με επιτυχία!'))

  return HttpResponseRedirect(reverse('innovations'))
   

class SearchListView(BaseListView, FormMixin, TemplateResponseMixin):
   
    order_field = None
    allowed_orderings = []
    max_num_orderings = 3
    total_count = True

    prefetch_fields = []

    apply_distinct = False

   
    groups_for_userlist = None

    filter_class = BaseFilter

    def __init__(self, *args, **kwargs):
        self.filtering = False
        super(SearchListView, self).__init__(*args, **kwargs)


    def get_form_kwargs(self):
        
        update_data ={}
        sfdict = self.filter_class.get_search_fields()
        for fieldname in sfdict:
            try:
                has_multiple = sfdict[fieldname].get('multiple', False)
            except:
                has_multiple = False

            if has_multiple:
                value = self.request.GET.getlist(fieldname, [])
            else:
                value = self.request.GET.get(fieldname, None)

            update_data[fieldname] =  value

        if self.order_field:
            update_data[self.order_field] = self.request.GET.get(self.order_field, None)

        initial = self.get_initial()
        initial.update(update_data)
        kwargs = {'initial': initial }

        if self.groups_for_userlist != None:
            pot_users = User.objects.exclude(id=self.request.user.id)
            if len(self.groups_for_userlist):
                pot_users = pot_users.filter(groups__name__in = self.groups_for_userlist)
            pot_users = pot_users.distinct().order_by('username')
            user_choices = tuple([(user.id, str(user)) for user in pot_users])
            kwargs['user_choices'] = user_choices

        return kwargs

    def get_search_query(self, request):
        search_query = self.filter_class.build_q(request.GET, request)
        return search_query

    def get_order_by_fields(self, request):
        if self.order_field and self.order_field in request.GET and request.GET[self.order_field]:
            order_by = request.GET[self.order_field]
            order_by_fields = order_by.split(",")
            order_by_fields = [x for x in order_by_fields]
        else:
            order_by_fields = []
        return order_by_fields

    def get_object_list(self, request, search_errors=None):
        search_query = self.get_search_query(request)
        order_by_fields = self.get_order_by_fields(request)
        object_list = self.get_queryset()

        if search_query:
            object_list = object_list.filter(search_query)
            
        if order_by_fields:
            object_list = object_list.order_by(*order_by_fields)


        if self.apply_distinct:
            object_list = object_list.distinct()

        return object_list


    def get(self, request, *args, **kwargs):

        search_errors_fields = []
        search_errors = []

        form_class = self.get_form_class()
        if form_class:
            self.form = self.get_form(form_class)
        else:
            self.form = None

        self.object_list = self.get_object_list(request, search_errors=search_errors)
        search_query = self.get_search_query(request)
        if search_query:
            self.filtering = True

        allow_empty = self.get_allow_empty()
        if not allow_empty:
            
            if (self.get_paginate_by(self.object_list) is not None
                and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404("Empty list and '%(class_name)s.allow_empty' is False."
                        % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        if self.total_count:
            context['total_count'] = self.get_queryset().count()


        if self.prefetch_fields:
            
            context['object_list'] = context['object_list'].prefetch_related(*self.prefetch_fields)

        context['filtering'] = self.filtering
        context['search_errors'] = search_errors
        context['search_errors_fields'] = search_errors_fields

        order_by_fields = self.get_order_by_fields(request)
        context['order_by_fields'] = order_by_fields

        context['order_field'] = self.order_field
        context['allowed_orderings'] = self.allowed_orderings
        context['max_num_orderings'] = min(self.max_num_orderings, len(self.allowed_orderings))


        if self.form:
            context['cleaned_data'] = self.form.fields
        else:
            context['cleaned_data'] = {}

        if len(search_errors):
            messages.add_message(self.request, messages.ERROR, ';'.join(search_errors))


        if not 'request' in context:
            context['request'] = request
        self.before_render(context)

        return self.render_to_response(context)


    def before_render(self, context):
        
        return
    
class InnovationsFilter(BaseFilter):
    search_fields= {
        "Τίτλος": ["Τίτλος"],
        "Φορέας":["Φορέας"],
        "Επίπεδο": {"operator":"__exact", "fields":["Επίπεδο"]},
        "Τομέας": {"operator":"__exact", "fields":["Τομέας"]},
        "Τύπος": {"operator":"__exact", "fields":["Τύπος"]},
        "Ημερομηνία_δημοσίευσης_από": {"operator":"__gte", "fields":["timestamp"]},
        "Ημερομηνία_δημοσίευσης_μέχρι": {"operator":"__lte", "fields":["timestamp"]},
    

    }
    
class InnovationSearchList(SearchListView):
    model= Innovation
    paginate_by=10
    template_name= "search_innovations.html"
    form_class= InnovationSearchForm
    filter_class= InnovationsFilter
     
class InnovationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Innovation
    fields = ['Τίτλος', 'Φορέας', "Επίπεδο", "Περιγραφή", "Τομέας", "Τύπος", "Στάδιο", "Στόχοι", "Αποτελέσματα", "Σχεδιασμός", "Πειραματική_εφαρμογή", "Εφαρμογή", "Διάδοση", "Χρηματοδότηση"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        innovation = self.get_object()
        if self.request.user.id == innovation.network_member.user_id:
            return True
        return False
    
class InnovationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Innovation
    success_url = 'innovations/'

    def test_func(self):
        innovation = self.get_object()
        if self.request.user.id == innovation.network_member.user_id:
            return True
        return False    

    