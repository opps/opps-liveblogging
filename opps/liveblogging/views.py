#!/usr/bin/env python
# -*- coding: utf-8 -*-
from opps.api.views.generic.list import ListView as ListAPIView
from opps.api.views.generic.list import ListCreateView

from .models import Event, Message


class EventAPIList(ListAPIView):
    model = Event


class MessageAPIList(ListCreateView):
    model = Message
