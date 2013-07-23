#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

from opps import liveblogging


install_requires = ["opps>=0.2"]

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "Operating System :: OS Independent",
               "Framework :: Django",
               'Programming Language :: Python',
               "Programming Language :: Python :: 2.7",
               "Operating System :: OS Independent",
               "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
               'Topic :: Software Development :: Libraries :: Python Modules']

try:
    long_description = open('README.md').read()
except:
    long_description = liveblogging.__description__

setup(name='opps-liveblogging',
      namespace_packages=['opps'],
      version=liveblogging.__version__,
      description=liveblogging.__description__,
      long_description=long_description,
      classifiers=classifiers,
      keywords='Liveblogging app for opps cms broadcast event via text',
      author=liveblogging.__author__,
      author_email=liveblogging.__email__,
      packages=find_packages(exclude=('doc', 'docs',)),
      install_requires=install_requires,
      include_package_data=True,)
