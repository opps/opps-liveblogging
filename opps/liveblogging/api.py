#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import timezone

from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL

from opps.api import MetaBase

from .models import Event as EventModel
from .models import Message as MessageModel


class Event(ModelResource):
    class Meta(MetaBase):
        queryset = EventModel.objects.filter(
            published=True,
            date_available__lte=timezone.now()
        )


class Message(ModelResource):
    class Meta:
        queryset = MessageModel.objects.filter(
            published=True,
            date_available__lte=timezone.now()
        )
        allowed_methods = ['get', 'post']
        filtering = {
            'site_domain': ALL,
            'channel_long_slug': ALL,
            'event': ALL,
        }
        authorization = DjangoAuthorization()
