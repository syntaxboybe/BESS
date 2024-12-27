from django import forms
from apps.UserPortal.models import *


class indigencyForm(forms.ModelForm):
    class Meta:
        model = clearance
        fields = ("age", "purpose", "date_released")

        widgets = {
            "age": forms.NumberInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "purpose": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "date_released": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
        }

    def __init__(self, *args, **kwagrs):
        super(indigencyForm, self).__init__(*args, **kwagrs)
        self.fields["date_released"].required = False
        self.fields["age"].required = False
