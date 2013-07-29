#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from opps.api.views.generic.list import ListView as ListAPIView
from opps.api.views.generic.list import ListCreateView
from opps.views.generic.list import ListView
from opps.views.generic.detail import DetailView

from .models import Event, Message
from .forms import MessageForm

import json
import time


class EventServerDetail(DetailView):
    model = Event

    def _longpolling(self, request):
        while True:
            yield "data: test streaming server\n\n"
            time.sleep(0.5)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        response = StreamingHttpResponse(self._longpolling(request),
                                         mimetype='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['Software'] = 'opps-liveblogging'
        response.flush()
        return response


class EventAdmin(object):
    def get_template_names(self):
        su = super(EventAdmin, self).get_template_names()
        return ["{}_admin.html".format(name.split('.html')[0]) for name in su]


class EventAdminList(EventAdmin, ListView):
    model = Event


class EventAdminDetail(EventAdmin, DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventAdminDetail, self).get_context_data(**kwargs)
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
        resp = json.dumps({'menssage': msg, 'status': obj.published})

        # Generate message event INFO
        messages.add_message(request, messages.INFO, resp)
        return HttpResponse(resp, mimetype="application/json")


class EventAPIList(ListAPIView):
    model = Event


class MessageAPIList(ListCreateView):
    model = Message
