#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from tastypie.api import Api

from .conf import settings
from .api import Event, Message


_api = Api(api_name=settings.OPPS_LIVEBLOGGING_CHANNEL)
_api.register(Event())
_api.register(Message())

urlpatterns = patterns(
    '',
    url(r'^api/', include(_api.urls)),
)
