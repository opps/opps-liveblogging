#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings

from appconf import AppConf


class OppsLiveBloggingConf(AppConf):
    CHANNEL = getattr(settings, 'OPPS_LIVEBLOGGING_CHANNEL', 'live')
    class Meta:
        prefix = 'opps_liveblogging'
