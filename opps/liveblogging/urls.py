#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from .views import EventAPIList, MessageAPIList
from .views import EventList, EventDetail
from .conf import settings


urlpatterns = patterns(
    '',
    url(r'^admin/liveblogging/message/(?P<slug>[\w-]+)$', EventDetail.as_view(),
        name='event-detail', kwargs={'channel__long_slug': u'live'}),
    url(r'^admin/liveblogging/message/$', EventList.as_view(),
        name='event-list', kwargs={'channel__long_slug': u'live'}),
)

urlpatterns += patterns(
    '',
    url(r'^{}/event/(?P<event__id>\d+).api$'.format(
        settings.OPPS_LIVEBLOGGING_CHANNEL),
        cache_page(settings.OPPS_CACHE_EXPIRE_DETAIL)(
            MessageAPIList.as_view()), name='event-api',
        kwargs={'channel__long_slug': u'live'}),

    url(r'^{}/events.api$'.format(settings.OPPS_LIVEBLOGGING_CHANNEL),
        cache_page(settings.OPPS_CACHE_EXPIRE_DETAIL)(
            EventAPIList.as_view()), name='events-api',
        kwargs={'channel__long_slug': u'live'}),
)
