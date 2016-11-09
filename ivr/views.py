from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from appointment_search.models import AppointmentSchedule
from datetime import date as _date

def time_of_day(hour):
    if hour < 12:
        return 'MORNING'
    else:
        return 'AFTERNOON'

@csrf_exempt
def index(request):

    registration_number = request.POST.get('registration_number')
    appointments = AppointmentSchedule.objects.filter(registration_number=registration_number)
    appointment = appointments[0]
    datetime = appointment.date
    date = datetime.strftime('%d-%m-%Y')
    hour = datetime.strftime("%H:%M")
    am_pm = appointment.date.strftime("%p")
    office_name = appointment.office.name
    
    response_str =  """
        <Response>
            <Say>Hello from Twilio! Here is the appointment reminder for registration number {}. 
	     Your appointment will be located at {}, on {}, at {} {}  </Say>
        </Response>
    """.format(registration_number, office_name, date,  hour, am_pm)

    return HttpResponse(response_str)
