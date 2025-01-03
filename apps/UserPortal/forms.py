from django import forms
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.utils.translation import gettext_lazy as _


class CleranceForm(forms.ModelForm):
    class Meta:
        model = clearance
        fields = ("age", "purpose")

        widgets = {
            "age": forms.NumberInput(
                attrs={"class": "form-control form-control-sm", "placeholder": "Age"}
            ),
            "purpose": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "",
                }
            ),
        }

    def __init__(self, *args, **kwagrs):
        super(CleranceForm, self).__init__(*args, **kwagrs)
        self.fields["age"].required = False


class IndigencyForm(forms.ModelForm):
    class Meta:
        model = CertificateOfIndigency
        fields = ("age", "purpose")

        widgets = {
            "age": forms.NumberInput(
                attrs={"class": "form-control form-control-sm", "placeholder": "Age"}
            ),
            "purpose": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "",
                }
            ),
        }

    def __init__(self, *args, **kwagrs):
        super(IndigencyForm, self).__init__(*args, **kwagrs)
        self.fields["age"].required = False


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
        }


class BusinessPermitForm(forms.ModelForm):
    class Meta:
        model = BusinessPermit
        fields = (
            "business_name",
            "location",
            "business_nature",
            "owner",
            "residece_certificate_no",
            "capital_investment",
            "gross_sales",
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
            "residece_certificate_no": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "capital_investment": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
            "gross_sales": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
        }


class ResidencyCertificateForm(forms.ModelForm):
    class Meta:
        model = ResidencyCertificate
        fields = ("purpose",)

        widgets = {
            "purpose": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "placeholder": ""}
            ),
        }


class CaptchaPasswordChangeForm(PasswordChangeForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    captcha = ReCaptchaField(
        error_messages={
            "required": _("You forgot to answer captcha, you're not a robot, right?")
        }
    )


class UpdateUsernameForm(forms.ModelForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ("username",)


class UpdateEmailForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ("email",)
