from django import forms
from apps.UserPortal.models import *


class BuildingPermitForm(forms.ModelForm):
    class Meta:
        model = BuildingPermit
        fields = (
            "proposed_construction",
            "total_area",
            "estimated_cost",
            "location",
            "owner",
            "contractor",
            "prepared_by",
            "paid_under_or",
            "date_released",
            "amount_paid",
        )

        widgets = {
            "proposed_construction": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "total_area": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "estimated_cost": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "owner": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "contractor": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "prepared_by": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "paid_under_or": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "date_released": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "amount_paid": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
        }

    def __init__(self, *args, **kwagrs):
        super(BuildingPermitForm, self).__init__(*args, **kwagrs)
        self.fields["prepared_by"].required = False
        self.fields["paid_under_or"].required = False
        self.fields["date_released"].required = False
        self.fields["amount_paid"].required = False
