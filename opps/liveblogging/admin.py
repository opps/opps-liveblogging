#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from opps.core.admin import PublishableAdmin

from .models import Event, Message, EventType


class EventAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["title"]}
    raw_id_fields = ['channel', 'main_image']
    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'short_url')}),
        (_(u'Content'), {
            'fields': ('hat',
                       ('main_image', 'main_image_caption'),
                       'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('event_type', 'published', 'date_available',
                       'show_on_root_channel',)}),
    )


class MessageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


class EventTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"], "template_suffix": ["title"]}


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Message, MessageAdmin)
