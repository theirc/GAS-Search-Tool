from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from appointment_search.models import AppointmentSchedule
from language_utils import set_language, language_selection_menu, audio_filename, numbers_in_language
from twilio import twiml
import urllib

OFFICE_NAME_TO_SHORTHAND = {
    'Alimos Asylum Unit': 'alimos',
    'Attica Regional Asylum Office': 'attica',
    'Piraeus Asylum Unit': 'piraeus',
    'Thessaloniki Regional Asylum Office': 'thessaloniki'
}

def time_of_day(hour):
    if hour < 12:
        return 'MORNING'
    else:
        return 'AFTERNOON'

def url_with_params(url, **kwargs):
    return '{}?{}'.format(url, urllib.urlencode(kwargs))

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
    with resp.gather(numDigits=5, action=url_with_params('ivr/confirmation', language=language)) as gather:
        gather.play(audio_filename('registration_id_prompt', language))
    return HttpResponse(resp)

@csrf_exempt
@set_language
@require_POST
def confirmation(request, **kwargs):
    # Confirm Registration ID
    language = kwargs['language']
    if 'Digits' in request.POST:
        registration_code = request.POST['Digits']
        resp = twiml.Response()
        with resp.gather(numDigits=1, action=url_with_params('ivr/appointment', language=language, registration=registration_code)) as gather:
            gather.play(audio_filename('input_repeat', language))
            for file in  numbers_in_language(registration_code, language):
                gather.play(file)
            gather.play(audio_filename('input_correct', language))
            gather.play(audio_filename('integer_1', language))
            gather.play(audio_filename('input_incorrect', language))
            gather.play(audio_filename('integer_2', language))
        return HttpResponse(resp)
    else:
        _appointment_error(language)

@csrf_exempt
@set_language
@require_POST
def appointment(request, **kwargs):
    language = kwargs['language']
    if 'Digits' in request.POST and request.POST['Digits'] == '1' and 'registration' in request.POST:
        return _check_appointment(request.POST['registration'], kwargs['language'])
    else:
        return registration(request, **kwargs)

@csrf_exempt
@set_language
@require_POST
def complete_menu(request, **kwargs):
    language = kwargs['language']
    if 'Digits' not in request.POST:
        return _appointment_error(language)
    elif request.POST['Digits'] == '2':
        return registration(request, **kwargs)
    elif request.POST['Digits'] == '3':
        resp = twiml.Response()
        resp.play(audio_filename('finish', language))
        resp.hangup()
        return HttpResponse(resp)
    else:
        # default or 1 to repeat appointment
        return _check_appointment(request.POST['registration'], kwargs['language'])

def _check_appointment(registration_code, language):
    appointment_details = _get_appointment_details(registration_code)
    if appointment_details:
        resp = twiml.Response()
        resp.play(audio_filename('appointment_scheduled', language))
        resp.play(audio_filename('month_{}'.format(appointment_details['month']), language))
        resp.play(audio_filename('integer_{}'.format(appointment_details['day']), language))
        resp.play(audio_filename('integer_{}'.format(appointment_details['hour']), language))
        resp.play(audio_filename('integer_{}'.format(appointment_details['minute']), language))
        resp.play(audio_filename('time_{}'.format(appointment_details['am_pm']), language))
        resp.play(audio_filename('loc_{}'.format(appointment_details['office_name']), language))
        with resp.gather(numDigits=1, action=url_with_params('ivr/complete_menu', language=language, registration=registration_code)) as gather:
            gather.play(audio_filename('end_menu_repeat', language))
            gather.play(audio_filename('integer_1', language))
            gather.play(audio_filename('end_menu_restart', language))
            gather.play(audio_filename('integer_2', language))
            gather.play(audio_filename('end_menu_finish', language))
            gather.play(audio_filename('integer_3', language))
        return HttpResponse(resp)
    else:
        return _appointment_error(language)

def _appointment_error(language):
    resp = twiml.Response()
    resp.play(audio_filename('registration_id_error', language))
    resp.redirect(url_with_params('ivr/registration', language=language))
    return HttpResponse(resp)

def _get_appointment_details(registration_number):
    appointments = AppointmentSchedule.objects.filter(registration_number=registration_number)
    if not appointments:
        return False
    appt = appointments[0]
    datetime = appt.date
    month = datetime.strftime('%B')
    day = datetime.strftime('%d')
    hour = datetime.strftime("%H")
    minute = datetime.strftime("%M")
    am_pm = appt.date.strftime("%p")
    office_name = OFFICE_NAME_TO_SHORTHAND[appt.office.name]
    return dict(office_name=office_name, month=month, day=day, am_pm=am_pm, hour=hour, minute=minute)
