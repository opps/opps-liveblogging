#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable
from opps.containers.models import Container


class Events(Container):
    pass


class Messages(Publishable):
    event = models.ForeignKey('liveblogging.Event',
                              on_delete=models.SET_NULL,
                              verbose_name=_(u'Event'))
    message = models.TextField(_(u'Message'))
