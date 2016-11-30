from collections import OrderedDict
from twilio import twiml
from django.http import HttpResponse
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
    return '{}/{}_{}'.format(IVR_AUDIO_PATH, language, file_ending)

def url_with_language(url, language):
    return '{}?{}'.format(url, urllib.urlencode({'language': language}))

def numbers_in_language(number_string, language):
    # TODO: spit multiple audio files to say a number in any language
    return number_string
