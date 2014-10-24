#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.dispatch import Signal


message_pre_save = Signal(providing_args=['instance', 'extra_data'])
message_post_save = Signal(providing_args=['instance', 'created', 'extra_data'])
message_pre_delete = Signal(providing_args=['instance', 'extra_data'])
message_post_delete = Signal(providing_args=['instance', 'extra_data'])
