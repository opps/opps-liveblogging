#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse

from opps.api.views.generic.list import ListView as ListAPIView
from opps.api.views.generic.list import ListCreateView
from opps.views.generic.list import ListView
from opps.views.generic.detail import DetailView

from .models import Event, Message
from .forms import MessageForm

import json


class EventList(ListView):
    model = Event


class EventDetail(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        try:
            msg = Message.objects.get(event__slug=self.slug)
        except Message.DoesNotExist:
            msg = []
        context['messages'] = msg
        context['messageform'] = MessageForm
        return context


class EventAPIList(ListAPIView):
    model = Event


class MessageAPIList(ListCreateView):
    model = Message
