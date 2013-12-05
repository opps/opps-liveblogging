#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import timezone

from opps.api import BaseHandler

from .models import Event, Message


class Handler(BaseHandler):

    def read(self, request):
        filters = {}
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        return self.model.objects.filter(**filters)


class EventHandler(Handler):
    model = Event

    def read(self, request):
        filters = {}
        filters['date_available__lte'] = timezone.now()
        filters['published'] = True
        return self.model.objects.filter(**filters)


class MessageHandler(Handler):
    allowed_methods = ['GET', 'POST']
    model = Message
