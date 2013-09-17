#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, time
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from opps.api.views.generic.list import ListView as ListAPIView
from opps.api.views.generic.list import ListCreateView
from opps.views.generic.list import ListView
from opps.views.generic.detail import DetailView
from opps.db import Db

from .models import Event, Message
from .forms import MessageForm


class EventDetail(DetailView):
    model = Event

    def get_template_names(self):
        templates = super(EventDetail, self).get_template_names()
        if self.object.event_type:
            domain_folder = self.get_template_folder()
            templates.insert(0, '{}/{}/detail_{}.html'.format(
                domain_folder,
                self.long_slug,
                self.object.event_type.template_suffix
            ))
        return templates


    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        try:
            msg = Message.objects.filter(event__slug=self.slug,
                                         published=True).order_by('-date_insert')
        except Message.DoesNotExist:
            msg = []
        context['msg'] = msg
        return context


class EventServerDetail(DetailView):
    model = Event

    def _queue(self):
        redis = Db('eventadmindetail', self.get_object().id)
        pubsub = redis.object().pubsub()
        pubsub.subscribe(redis.key)

        while True:
            for m in pubsub.listen():
                if m['type'] == 'message':
                    try:
                        d = json.loads(m['data'])
                        yield u"action: {}\n\n".format(d)
                    except ValueError:
                        data = m['data'].decode('utf-8')
                        yield u"data: {}\n\n".format(data)
            yield u"data: \n\n"
            time.sleep(0.5)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        response = StreamingHttpResponse(self._queue(),
                                         mimetype='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['Software'] = 'opps-liveblogging'
        response['Access-Control-Allow-Origin'] = '*'
        response.flush()
        return response


class EventAdmin(object):
    model = Event

    def get_template_names(self):
        su = super(EventAdmin, self).get_template_names()
        return ["{}_admin.html".format(name.split('.html')[0]) for name in su]


class EventAdminList(EventAdmin, ListView):
    pass


class EventAdminDetail(EventAdmin, DetailView):

    def get_template_names(self):
        if self.object.event_type:
            suffix = "_" + self.object.event_type.template_suffix
        else:
            suffix = ""

        su = super(EventAdmin, self).get_template_names()
        templates = ["{}_admin{}.html".format(name.split('.html')[0], suffix) for name in su] + su
        return templates

    def get_context_data(self, **kwargs):
        context = super(EventAdminDetail, self).get_context_data(**kwargs)
        try:
            msg = Message.objects.filter(event__slug=self.slug,
                                         published=True).order_by('-date_insert')
        except Message.DoesNotExist:
            msg = []
        context['msg'] = msg
        context['messageform'] = MessageForm
        return context

    @csrf_exempt
    @login_required(login_url='/admin/')
    def post(self, request, *args, **kwargs):
        msg = request.POST.get('message', None)
        id = request.POST.get('id_message', None)
        event = self.get_object()
        redis = Db(self.__class__.__name__, self.get_object().id)
        if id:
            obj = Message.objects.get(id=id)
            published = request.POST.get('published', True)
            obj.published = published
            obj.message = msg
            obj.user = request.user
            obj.save()
            redis.publish(json.dumps({'action': 'update',
                                      'id': id,
                                      'published': published}))
        else:
            Message.objects.create(message=msg, user=request.user,
                                   event=event, published=True)
            redis.publish(msg)

        event.create_event(request.POST)

        return HttpResponse(msg)


class EventAPIList(ListAPIView):
    model = Event


class MessageAPIList(ListCreateView):
    model = Message
