#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='pyscript-cache',
      version='0.1',
      description='Simple caching structure especially useful for prototyping, exploratory analysis and plots with time consuming data aquisition',
      packages=find_packages()
      )
