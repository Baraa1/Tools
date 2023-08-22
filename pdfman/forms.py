from django import forms

# These allow multiple file upload using one input field
# MultipleFileInput, MultipleFileField, and FileFieldForm
# were pulled directly from Django 4.2 Docs and I don't see any need to edit it
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class FileFieldForm(forms.Form):
    file_field = MultipleFileField()