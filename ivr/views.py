from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from appointment_search.models import AppointmentSchedule
from twilio import twiml
from collections import OrderedDict
import urllib

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

def set_language(view):
    """
    Sets the language based on language or Digits params
    """
    def decorated(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponse(language_selection_menu())
        elif 'language' in request.POST:
            language = request.POST['language']
            if language in LANGUAGES.values():
                kwargs['language'] = language
                return view(request, *args, **kwargs)
            else:
                return HttpResponse(language_selection_menu())
        elif 'Digits' in request.POST and request.POST['Digits'] in LANGUAGES:
            kwargs['language'] = LANGUAGES[request.POST['Digits']]
            return view(request, *args, **kwargs)
        else:
            return HttpResponse(language_selection_menu())
    decorated.__doc__ = view.__doc__
    decorated.__name__ = view.__name__
    return decorated

def audio_filename(file_ending, language):
    return '{}/{}_{}'.format(IVR_AUDIO_PATH, language, file_ending)

def url_with_language(url, language):
    return '{}?{}'.format(url, urllib.urlencode({'language': language}))

def language_selection_menu():
    repeat_count = 3
    resp = twiml.Response()
    with resp.gather(numDigits=1, action='/ivr/registration') as gather:
        gather.say('Welcome to Refugee Info')
        for _ in xrange(repeat_count):
            for digit, language in LANGUAGES.items():
                gather.play(audio_filename('language_description', language))
                gather.play(audio_filename('integer_{}'.format(digit), language))
    return resp

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
