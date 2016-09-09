import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from djng.views.mixins import JSONResponseMixin

from . import models


@method_decorator(csrf_exempt, name='dispatch')
class SearchJSONView(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        in_data = json.loads(request.body)
        registration_number = in_data['registration_number']

        appointment = models.AppointmentSchedule.objects.filter(registration_number=registration_number)
        if not appointment:
            return self.json_response(None)

        appointment = appointment[0]
        return self.json_response({
            'date': appointment.date.strftime("%x"),
            'registration_number': appointment.registration_number,
            'office_name': appointment.office.name,
            'office': {a.language: {'name': a.name, 'address': a.address} for a in
                       appointment.office.asylumofficedetails_set.all()}
        })
