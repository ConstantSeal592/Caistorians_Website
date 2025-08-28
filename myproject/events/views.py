from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Event

# Create your views here.


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    ordering = ["start_date"]


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"