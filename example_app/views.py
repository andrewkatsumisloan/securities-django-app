# -*- coding: utf-8 -*-
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


def index(request):
    host = request.META['HTTP_HOST']
    if request.method == "POST":
        args = request.POST
        print("POST:", args)
        results = OHLC.objects.filter(ticker=args['ticker'], date__range=[args['start'], args['end']]).order_by('date')
        closes = []
        dates = []
        for result in results:
            result.timestamp = time.mktime(result.date.timetuple())
            closes.append(result.close)
            dates.append(result.date.strftime('%B %d %y'))
        print(dates)
        return render(
            request, 'example_app/chartjs_test.html',
            {
                'ticker': args['ticker'],
                'start': args['start'],
                'end': args['end'],
                'array_table': results,
                'close_table': closes,
                'date_table': str(dates)
            })

    return render(request, 'example_app/chartjs_test.html', {})


def db_init(request):
    csv_dir = '/Users/AKS/securities-data/SP500_DATA/Individual/'
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
        count = 0
        for line in lines[1:]:
            values = re.split(',', line.rstrip())

            ohlc_dict = dict(zip(columns, values))
            if ohlc_dict['high']:
                pass
                # ohlc = OHLC(
                #     ticker=ticker,
                #     date=re.split(' ', ohlc_dict['datetime'])[0],
                #     high=float(ohlc_dict['high']),
                #     opening=float(ohlc_dict['open']),
                #     low=float(ohlc_dict['low']),
                #     close=float(ohlc_dict['close']),
                #     volume=float(ohlc_dict['volume']),
                #     adj_close= 0.0
                # )
            if not count%100:
                print("line ",count, line)
            count = count + 1
                # ohlc.save()

    host = request.META['HTTP_HOST']
    if request.method == "POST":
        args = request.POST
        print("args:", args)
    params = {}    
    return render(request, 'example_app/testing.html', params)
