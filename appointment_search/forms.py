import os

from django import forms
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


class SpreadsheetForm(forms.Form):
    spreadsheet = forms.FileField(validators=[validate_file_extension])
