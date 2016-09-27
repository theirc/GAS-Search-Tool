import json
import xlrd
import pytz
import dateparser

from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View

from djng.views.mixins import JSONResponseMixin
from pytz import timezone
from datetime import date as _date

from appointment_search.forms import SpreadsheetForm
from . import models


def time_of_day(hour):
    if hour < 12:
        return 'MORNING'
    else:
        return 'AFTERNOON'


@method_decorator(csrf_exempt, name='dispatch')
class SearchJSONView(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        in_data = json.loads(request.body)
        registration_number = in_data['registration_number']

        appointment = models.AppointmentSchedule.objects.filter(registration_number=registration_number)
        if not appointment:
            return self.json_response(None)

        appointment = appointment[0]
        appointment.date = appointment.date.astimezone(timezone("Europe/Athens"))

        return self.json_response({
            'datetime': appointment.date,
            'date': appointment.date.strftime('%d-%m-%Y'),
            'hour': appointment.date.strftime("%H:%M"),
            'am_pm': appointment.date.strftime("%p"),
            'time_of_day': time_of_day(appointment.date.hour),
            'registration_number': appointment.registration_number,
            'office_name': appointment.office.name,
            'office': {a.language: {'name': a.name, 'address': a.address} for a in
                       appointment.office.asylumofficedetails_set.all()}
        })


class ImportSpreadsheetView(FormView):
    template_name = 'admin/import_spreadsheet.html'
    form_class = SpreadsheetForm

    def get_success_url(self):
        return reverse('admin:index')

    def get_success_message(self, created_count, updated_count):
        return 'Created {} new appointment entries.\n' \
               'Updated {} existing appointment entries.'.format(created_count, updated_count)

    def form_valid(self, form):
        spreadsheet = form.cleaned_data['spreadsheet']
        w = xlrd.open_workbook(filename=None, file_contents=spreadsheet.read())
        sheet = w.sheet_by_index(0)

        header = [unicode(sheet.cell_value(0, i)).lower() for i in range(0, sheet.ncols)]
        rows = [dict(zip(header, [sheet.cell_value(j, i) for i in range(0, sheet.ncols)])) for j in
                range(1, sheet.nrows)]

        sample = rows[0] if rows else None
        if sample:
            if len({'refugeeid', 'as office eng', 'date', 'hour of day'}.intersection(sample.keys())) == 4:
                updated_count = 0
                created_count = 0
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
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                messages.success(self.request, self.get_success_message(created_count, updated_count))
            else:
                messages.error(self.request, 'An error occured while parsing uploaded file.')
        return super(ImportSpreadsheetView, self).form_valid(form)
