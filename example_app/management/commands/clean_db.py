from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from example_app.models import *

import os
import re
import shutil
import sys
import tempfile
import base64
import requests
import json
import datetime
import time

# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):


        OHLC.objects.all().delete()

