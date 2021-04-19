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

# -*- coding: utf-8 -*-n
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):
        csv_dir = "/Users/AKS/securities-data/SP500_DATA/Individual/"
        # csv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'example_db', 'csv')
        csv_files = os.listdir(csv_dir)

        for tfile in csv_files:
            handle = open(os.path.join(csv_dir, tfile), 'r')
            ticker = os.path.splitext(tfile)[0]
            print(tfile)
            lines = handle.readlines()
            print(lines[1])
            handle.close()
            columns = re.split(',', lines[0].rstrip())

            records = []
            for line in lines[1:]:
                values = re.split(',', line.rstrip())
                ohlc_dict = dict(zip(columns, values))
                if ohlc_dict['high']:
                    ohlc = OHLC(
                        ticker=ticker,
                        date=re.split(' ', ohlc_dict['datetime'])[0],
                        high=float(ohlc_dict['high']),
                        opening=float(ohlc_dict['open']),
                        low=float(ohlc_dict['low']),
                        close=float(ohlc_dict['close']),
                        volume=float(ohlc_dict['volume']),
                        adj_close= 0.0
                    )
                    records.append(ohlc)
                    if len(records) > 500:
                        OHLC.objects.bulk_create(records)
                        records = []

            OHLC.objects.bulk_create(records)


