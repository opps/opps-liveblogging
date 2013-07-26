#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    message = forms.CharField(required=True)
    class Meta:
        model = Message
        fields = ('message',)
