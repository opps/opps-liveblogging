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
            msg = Message.objects.filter(event__slug=self.slug,
                                         published=True)
        except Message.DoesNotExist:
            msg = []
        context['msg'] = msg
        context['messageform'] = MessageForm
        return context

    def post(self, request, *args, **kwargs):
        msg = request.POST['message']
        obj = Message.objects.create(message=msg, user=request.user,
                                     event=self.get_object(), published=True)
        resp = {'menssage': msg, 'status': obj.published}
        return HttpResponse(json.dumps(resp), mimetype="application/json")


class EventAPIList(ListAPIView):
    model = Event


class MessageAPIList(ListCreateView):
    model = Message
