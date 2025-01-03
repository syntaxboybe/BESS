from django import forms
from apps.UserPortal.models import *


class BusinessPermitForm(forms.ModelForm):
    class Meta:
        model = BusinessPermit
        fields = (
            "business_name",
            "location",
            "business_nature",
            "owner",
            "capital_investment",
            "gross_sales",
            "residece_certificate_no",
            "date_released",
            "issued_at",
            "previous_or",
            "date_issued",
            "previous_or_issued_at",
            "amount_collect",
            "paid_or",
            "paid_or_date_issued",
            "paid_or_issued_at",
            "amount_colledted",
        )

        widgets = {
            "business_name": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "business_nature": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "owner": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "capital_investment": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "gross_sales": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "residece_certificate_no": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "date_released": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "issued_at": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "previous_or": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "date_issued": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "previous_or_issued_at": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "amount_collect": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "paid_or": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "paid_or_date_issued": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "paid_or_issued_at": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "amount_colledted": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
        }

    def __init__(self, *args, **kwagrs):
        super(BusinessPermitForm, self).__init__(*args, **kwagrs)
        self.fields["residece_certificate_no"].required = False
        self.fields["date_released"].required = False
        self.fields["issued_at"].required = False

        self.fields["previous_or"].required = False
        self.fields["date_issued"].required = False
        self.fields["previous_or_issued_at"].required = False
        self.fields["amount_collect"].required = False

        self.fields["paid_or"].required = False
        self.fields["paid_or_date_issued"].required = False
        self.fields["paid_or_issued_at"].required = False
        self.fields["amount_colledted"].required = False
