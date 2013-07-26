#!/usr/bin/env python
# -*- coding: utf-8 -*-
from opps.api.views.generic.list import ListView as ListAPIView
from opps.api.views.generic.list import ListCreateView
from opps.views.generic.list import ListView
from opps.views.generic.detail import DetailView

from .models import Event, Message


class EventList(ListView):
    model = Event


class EventDetail(DetailView):
    model = Event


class EventAPIList(ListAPIView):
    model = Event


class MessageAPIList(ListCreateView):
    model = Message
