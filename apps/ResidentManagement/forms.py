from dataclasses import field
from pyexpat import model
from django import forms
from .models import *
from apps.UserPortal.models import *

from django.contrib.auth.models import User


# class DateInput(forms.DateInput):
#     input_type = 'date'
# class TimeInput(forms.TimeInput):
#     input_type = 'time'
class ProfileForm(forms.ModelForm):
    class Meta:
        model = ResidentsInfo
        fields = (
            "image",
            "firstname",
            "middlename",
            "lastname",
            "suffix",
            "sex",
            "phone",
            "birthdate",
            "birthplace",
            "civil_status",
            "citizenship",
            "purok",
            "address",
            "occupation",
            "educ_attainment",
            "single_parent",
            "status",
            "years_resided",
        )

        singParentChoices = (
            ("", "-Select-"),
            ("Yes", "Yes"),
            ("No", "No"),
        )

        widgets = {
            "image": forms.FileInput(
                attrs={"class": "form-control",
                       "id": "file", "accept": "image/*"}
            ),
            "firstname": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Firstname",
                }
            ),
            "middlename": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Middlename",
                }
            ),
            "lastname": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Lastname",
                }
            ),
            "suffix": forms.TextInput(
                attrs={"class": "form-control form-control-sm",
                       "placeholder": "Suffix"}
            ),
            "sex": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "phone": forms.NumberInput(
                attrs={"class": "form-control form-control-sm",
                       "placeholder": "+63"}
            ),
            "birthdate": forms.DateInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Select a date",
                }
            ),
            "birthplace": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Birthplace",
                }
            ),
            "civil_status": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "citizenship": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Citizenship",
                }
            ),
            "purok": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Address",
                }
            ),
            "occupation": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Occupation",
                }
            ),
            "educ_attainment": forms.Select(
                attrs={"class": "form-select form-select-sm"}
            ),
            "single_parent": forms.Select(
                choices=singParentChoices, attrs={
                    "class": "form-select form-select-sm"}
            ),
            "status": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "years_resided": forms.DateInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Select a year",
                    "id": "year",
                }
            ),
        }

    def __init__(self, *args, **kwagrs):
        super(ProfileForm, self).__init__(*args, **kwagrs)
        self.fields["sex"].empty_label = "Select"
        self.fields["civil_status"].empty_label = "Select"
        self.fields["purok"].empty_label = "Select"
        self.fields["educ_attainment"].empty_label = "Select"
        self.fields["status"].empty_label = "Select"
        self.fields["suffix"].required = False


class EditUserAccountForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "email")


class ProcessClearanceForm(forms.ModelForm):
    class Meta:
        model = clearance
        fields = ("age", "purpose", "community_tax_num",
                  "community_tax_date_issued")

        widgets = {
            "age": forms.NumberInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "purpose": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "community_tax_num": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "community_tax_date_issued": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
        }

    def __init__(self, *args, **kwagrs):
        super(ProcessClearanceForm, self).__init__(*args, **kwagrs)
        self.fields["age"].required = False


class ProcessIndigencyForm(forms.ModelForm):
    class Meta:
        model = CertificateOfIndigency
        fields = ("age", "purpose")

        widgets = {
            "age": forms.NumberInput(
                attrs={"class": "form-control form-control-sm",
                       "placeholder": "Age"}
            ),
            "purpose": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "purpose",
                }
            ),
        }

    def __init__(self, *args, **kwagrs):
        super(ProcessIndigencyForm, self).__init__(*args, **kwagrs)
        self.fields["age"].required = False


class ProcessBusinessPermitForm(forms.ModelForm):
    class Meta:
        model = BusinessPermit
        fields = (
            "business_name",
            "location",
            "business_nature",
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


class ProcessBuildingPermitForm(forms.ModelForm):
    class Meta:
        model = BuildingPermit
        fields = (
            "proposed_construction",
            "total_area",
            "estimated_cost",
            "location",
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


class ProcessResidencyCertificateForm(forms.ModelForm):
    class Meta:
        model = ResidencyCertificate
        fields = ("purpose",)

        widgets = {
            "purpose": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
        }
