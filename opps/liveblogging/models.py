#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from opps.core.models import Publishable
from opps.containers.models import Container
from opps.channels.models import Channel

from .conf import settings


class EventType(models.Model):
    title = models.CharField(_("Name"), max_length=30, unique=True)
    slug = models.SlugField(_("Identifier"), db_index=True, max_length=35)
    template_suffix = models.SlugField(
        _("Template suffix"),
        max_length=35,
        null=True,
        blank=True,
        help_text=_("Ex: '<strong>soccer</strong>' so the template will be "
                    "containers/{}/detail_<strong>soccer</strong>.html".format(
                        settings.OPPS_LIVEBLOGGING_CHANNEL
                    )
        )
    )

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        self.template_suffix = self.template_suffix or self.slug
        super(EventType, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Event Type')
        verbose_name_plural = _('Event Types')


class Event(Container):
    event_type = models.ForeignKey('liveblogging.EventType', null=True, blank=True,
                                   verbose_name=_("Event type"),
                                   help_text=_("Leave blank to use default event template"))

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-date_available', 'title', 'channel_long_slug']


class Message(Publishable):
    event = models.ForeignKey('liveblogging.Event',
                              verbose_name=_('Event'))
    message = models.TextField(_('Message'))

    def save(self, *args, **kwargs):
        channel = Channel.objects.get(slug=settings.OPPS_LIVEBLOGGING_CHANNEL)
        self.channel = channel
        super(Message, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
