from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from appointment_search.models import AppointmentSchedule
from twilio import twiml
from collections import OrderedDict

# TODO: Add S3 Bucket path
IVR_AUDIO_PATH = 'ivr/audio'
LANGUAGES = OrderedDict([
    ('1', 'english'),
    ('2', 'kurmanji'),
    ('3', 'punjabi'),
    ('4', 'dari'),
    ('5', 'urdu'),
    ('6', 'arabic'),
    ('7', 'farsi'),
    ('8', 'greek'),
    ('9', 'sourani')
])

def time_of_day(hour):
    if hour < 12:
        return 'MORNING'
    else:
        return 'AFTERNOON'

def audio_filename(file_ending, language):
    return '{}/{}_{}'.format(IVR_AUDIO_PATH, language, file_ending)

@csrf_exempt
def incoming(request):
    # Language Selection Menu
    repeat_count = 3
    resp = twiml.Response()
    with resp.gather(numDigits=1, action='/ivr/registration') as gather:
        gather.say('Welcome to Refugee Info')
        for _ in xrange(repeat_count):
            for digit, language in LANGUAGES.items():
                gather.play(audio_filename('language_description', language))
                gather.play(audio_filename('integer_{}'.format(digit), language))
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
