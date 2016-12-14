from collections import OrderedDict
from twilio import twiml
from django.http import HttpResponse
import urllib

IVR_AUDIO_PATH = ' https://s3.amazonaws.com/eu-twilio'

LANGUAGES = OrderedDict([
    ('1', 'English'),
    ('2', 'Kurmanji'),
    ('3', 'Punjabi'),
    ('4', 'Dari'),
    ('5', 'Urdu'),
    ('6', 'Arabic'),
    ('7', 'Farsi'),
    ('8', 'Greek'),
    ('9', 'Sourani')
])


def set_language(view):
    """
    Dectorator to set the language based on language or Digits params
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


def audio_filename(file_ending, language):
    return '{}/{}/{}_{}'.format(IVR_AUDIO_PATH, language, language, file_ending)


def url_with_language(url, language):
    return '{}?{}'.format(url, urllib.urlencode({'language': language}))


# split multiple a number into multiple audio files to play a number in any language
# returns an array of file names
def numbers_in_language(number_string, language):
    files = []
    for digit in number_string:
        files.append(audio_filename('integer_{}'.format(digit), language))
    return files
