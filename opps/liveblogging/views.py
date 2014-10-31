#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import logging
from django.db import connections
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.core.serializers.json import DjangoJSONEncoder

from opps.views.generic.list import ListView
from opps.views.generic.detail import DetailView
from opps.db import Db
from redis.exceptions import RedisError

import signals
from .models import Event, Message
from .forms import MessageForm


logger = logging.getLogger(__name__)


def redis_wrapper(instance, method, *args, **kwargs):
    try:
        return getattr(instance, method)(*args, **kwargs)
    except RedisError as e:
        logger.error(
            'Redis error: {}'.format(e), exc_info=True, extra={
                'exception': e,
            }
        )


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
            msg = Message.objects.filter(
                event__slug=self.slug, published=True).order_by('-date_insert')
        except Message.DoesNotExist:
            msg = []
        context['msg'] = msg
        context['OPPS_LIVEBLOGGING_URL'] = getattr(
            settings, 'OPPS_LIVEBLOGGING_URL')
        return context


class EventServerDetail(DetailView):
    model = Event

    def _queue(self):
        try:
            redis = Db('eventadmindetail', self.get_object().id)
        except:
            redis = Db('eventadmindetail', self.event_obj.id)
        pubsub = redis.object().pubsub()
        pubsub.subscribe(redis.key)

        for conn in connections.all():
            conn.close()

        while True:
            for m in pubsub.listen():
                if m['type'] == 'message':
                    msg  = u"compatibility: true\n"
                    msg += u"retry: 10000\n"
                    msg += u"data: {}\n\n".format(m['data'])
                    yield msg

                stream  = u"compatibility: true\n"
                stream += u"retry: 10000\n"
                stream += u"data: {}\n\n".format(
                    json.dumps({"event": "stream"}))
                yield stream
            time.sleep(0.5)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.slug = self.kwargs.get('slug')
        self.event_obj = self.model.objects.get(
                channel_long_slug=self.get_long_slug(), slug=self.slug)

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
        suffix = ""
        if self.object.event_type:
            suffix = "_" + self.object.event_type.template_suffix

        su = super(EventAdmin, self).get_template_names()
        t = "{}_admin{}.html"
        templates = [t.format(name.split('.html')[0], suffix) for name in su]
        return templates + su

    def get_context_data(self, **kwargs):
        context = super(EventAdminDetail, self).get_context_data(**kwargs)
        try:
            msg = Message.objects.filter(
                event__slug=self.slug, published=True).order_by('-date_insert')
        except Message.DoesNotExist:
            msg = []
        context['msg'] = msg
        context['messageform'] = MessageForm
        context['OPPS_LIVEBLOGGING_URL'] = getattr(
            settings, 'OPPS_LIVEBLOGGING_URL')
        return context

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        msg = request.POST.get('message', None)
        id = request.POST.get('id_message', None)
        event = self.get_object()
        redis = Db(self.__class__.__name__, self.get_object().id)

        if request.POST.get('stream', None):
            redis_wrapper(redis, 'publish', json.dumps({"event": "stream"}))
            return HttpResponse('stream')

        _list = {}
        for k, v in request.POST.iteritems():
            _list[k] = v

        if id:
            obj = Message.objects.get(id=id)

            published = True

            if request.POST.get('published') == 'false':
                published = False

            obj.published = published

            if msg:
                obj.message = msg

            obj.user = request.user

            if published:
                signals.message_pre_save.send(
                    sender=self.__class__, instance=obj, extra_data=_list)
            else:
                signals.message_pre_delete.send(
                    sender=self.__class__, instance=obj, extra_data=_list)

            obj.save()

            redis_wrapper(redis, 'publish', json.dumps({
                    "event": "update",
                    "id": id,
                    "published": published,
                    "msg": msg,
                    "date": obj.date_available
                },
                cls=DjangoJSONEncoder))

            if published:
                signals.message_post_save.send(
                    sender=self.__class__, instance=obj, created=False,
                    extra_data=_list)
            else:
                signals.message_post_delete.send(
                    sender=self.__class__, instance=obj, extra_data=_list)
        else:
            obj = Message(
                message=msg, user=request.user, event=event, published=True)


            signals.message_pre_save.send(
                sender=self.__class__, instance=obj, extra_data=_list)

            obj.save(force_insert=True)

            signals.message_pre_save
            id = obj.id

            redis_wrapper(redis, 'publish', json.dumps({
                    "event": "message",
                    "id": id,
                    "msg": msg,
                    "date": obj.date_available
                },
                cls=DjangoJSONEncoder))

            _list['id_message'] = id

            signals.message_post_save.send(
                sender=self.__class__, instance=obj, created=True,
                extra_data=_list)

        return HttpResponse(msg)
