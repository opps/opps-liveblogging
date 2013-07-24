#!/usr/bin/env python
# -*- coding: utf-8 -*-
from opps.api.views.generic.list import ListView as ListAPIView

from .models import Event


class EventAPIList(ListAPIView):
    model = Event
