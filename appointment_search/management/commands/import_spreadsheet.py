from __future__ import print_function, unicode_literals
import tempfile
from datetime import datetime,date as _date
import pytz
import dateparser

import requests
import xlrd
from django.core.management.base import BaseCommand

from appointment_search import models


class Command(BaseCommand):
    help = 'Imports data for the appointment database'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs=1, type=str)

    def handle(self, *args, **options):
        url, = options['url']
        res = requests.get(url)
        with tempfile.NamedTemporaryFile(suffix='.xlsx') as temp:
            temp.delete = True
            with open(temp.name, 'w+') as fp:
                fp.write(res.content)

            w = xlrd.open_workbook(temp.name)

        sheet = w.sheet_by_index(0)

        header = [unicode(sheet.cell_value(0, i)).lower() for i in range(0, sheet.ncols)]
        rows = [dict(zip(header, [sheet.cell_value(j, i) for i in range(0, sheet.ncols)])) for j in
                range(1, sheet.nrows)]

        sample = rows[0] if rows else None
        print ('Loaded spreadsheet')
        if sample:
            if len({'refugeeid', 'as office eng', 'date', 'hour of day'}.intersection(sample.keys())) == 4:
                for r in rows:
                    appointment, created = models.AppointmentSchedule.objects.get_or_create(
                        registration_number=str(int(r['refugeeid'])))
                    if type(r['date']) is float:
                        date = xlrd.xldate_as_tuple(r['date'], w.datemode)
                        date = "{} {}".format(_date(*date[0:3]).isoformat(), r['hour of day'])
                        date = dateparser.parse(date)
                    else:
                        date = "{} {}".format(r['date'], r['hour of day'])
                        date = dateparser.parse(date, settings={'DATE_ORDER': 'DMY'})

                    athens = pytz.timezone("Europe/Athens")
                    date = athens.localize(date)

                    asylum_office, c = models.AsylumOffice.objects.get_or_create(name=r['as office eng'])

                    appointment.date = date
                    appointment.office = asylum_office
                    appointment.save()

                    print('Imported appointment for registration number {}'.format(appointment.registration_number))
        print('Import complete')