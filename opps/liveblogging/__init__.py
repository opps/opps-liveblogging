#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pkg_resources

pkg_resources.declare_namespace(__name__)

VERSION = (0, 1, 1)

__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = u"Liveblogging app, event broadcast via text"

__author__ = u"Thiago Avelino"
__credits__ = []
__email__ = u"thiago@avelino.xxx"
__copyright__ = u"Copyright 2014, Thiago Avelino"
