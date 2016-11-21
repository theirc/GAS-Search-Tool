from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from appointment_search.models import AppointmentSchedule
from twilio import twiml

# TODO: Add S3 Bucket path
IVR_AUDIO_PATH = ''

def time_of_day(hour):
    if hour < 12:
        return 'MORNING'
    else:
        return 'AFTERNOON'


@csrf_exempt
def incoming(request):
    # Language Selection Menu
    languages = ['english', 'kurmanji', 'punjabi', 'dari', 'urdu', 'arabic', 'farsi', 'greek', 'sourani']
    repeat_count = 3
    resp = twiml.Response()
    with resp.gather(numDigits=1, action='/ivr/registration') as gather:
        gather.say('Welcome to Refugee Info')
        for _ in xrange(repeat_count):
            for language in languages:
                gather.play('{}/{}_language_description.wav'.format(IVR_AUDIO_PATH, language))
    return HttpResponse(resp)


@csrf_exempt
def registration(request):
    # Registration Prompt
    resp = twiml.Response()
    resp.say('something')
    return HttpResponse(resp)


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
