#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable
from opps.containers.models import Container
from opps.channels.models import Channel

from .conf import settings


class Event(Container):
    pass


class Message(Publishable):
    event = models.ForeignKey('liveblogging.Event',
                              verbose_name=_(u'Event'))
    message = models.TextField(_(u'Message'))

    def save(self, *args, **kwargs):
        channel = Channel.objects.get(slug=settings.OPPS_LIVEBLOGGING_CHANNEL)
        self.channel = channel
        super(Message, self).save(*args, **kwargs)
