from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from appointment_search.models import AppointmentSchedule
from language_utils import set_language, language_selection_menu, audio_filename, url_with_language
from twilio import twiml

def time_of_day(hour):
    if hour < 12:
        return 'MORNING'
    else:
        return 'AFTERNOON'

@csrf_exempt
def incoming(request):
    # Language Selection Menu
    return HttpResponse(language_selection_menu())

@csrf_exempt
@set_language
def registration(request, **kwargs):
    # Registration Prompt
    language = kwargs['language']
    resp = twiml.Response()
    with resp.gather(numDigits=5, action=url_with_language('ivr/appointment', language)) as gather:
        gather.play(audio_filename('registration_id_prompt', language))
    return HttpResponse(resp)

@csrf_exempt
@set_language
@require_POST
def confirmation(request, **kwargs):
    # Confirm Registration ID
    language = kwargs['language']
    if 'Digits' in request.POST:
        registration_number = request.POST['Digits']
        appointment = models.AppointmentSchedule.objects.filter(registration_number=registration_number)
    return HttpResponse()

@csrf_exempt
def appointment(request):
    return HttpResponse("TwiML for playing back detailed appointment information")



@csrf_exempt
def complete_menu(request):
    return HttpResponse("TwiML for redirect based on selection")

# This is a test method to demon how to retrieve the appointment details for existing dal layer
@csrf_exempt
def test(request):
    registration_number = request.POST.get('registration_number')
    appointment_details = _get_appointment_details(registration_number)

    # TODO: Below is just place holder TWIML and will be replaced by IRS flow
    response_str = """
        <Response>
            <Say>Here is the appointment reminder for registration number {}.
            Your appointment will be located at {}, on {}, at {} {}  </Say>
        </Response>
    """.format(registration_number,
               appointment_details['office_name'],
               appointment_details['date'],
               appointment_details['hour'],
               appointment_details['am_pm'])

    return HttpResponse(response_str)


def _get_appointment_details(registration_number):
    appointments = AppointmentSchedule.objects.filter(registration_number=registration_number)
    appt = appointments[0]
    datetime = appt.date
    date = datetime.strftime('%d-%m-%Y')
    hour = datetime.strftime("%H:%M")
    am_pm = appointment.date.strftime("%p")
    office_name = appointment.office.name
    return dict(office_name=office_name, date=date, am_pm=am_pm, hour=hour)
