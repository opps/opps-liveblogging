#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from piston.resource import Resource

from .api import EventHandler, MessageHandler


event = Resource(handler=EventHandler)
message = Resource(handler=MessageHandler)

urlpatterns = patterns(
    '',
    url(r'^api/event/$', event),
    url(r'^api/message/$', message),
)
