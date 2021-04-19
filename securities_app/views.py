# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from securities_app.models import *

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
            request, 'securities_app/chartjs_test.html',
            {
                'ticker': args['ticker'],
                'start': args['start'],
                'end': args['end'],
                'array_table': results,
                'close_table': closes,
                'date_table': str(dates)
            })

    return render(request, 'securities_app/chartjs_test.html', {})

