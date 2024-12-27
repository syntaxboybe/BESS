from django import forms
from apps.UserPortal.models import *


class ResidencyCertificateForm(forms.ModelForm):
    class Meta:
        model = ResidencyCertificate
        fields = (
            "purpose",
            "date_released",
        )

        widgets = {
            "purpose": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "date_released": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
        }

    def __init__(self, *args, **kwagrs):
        super(ResidencyCertificateForm, self).__init__(*args, **kwagrs)
        self.fields["date_released"].required = False
