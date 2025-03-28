from dataclasses import fields
from django.forms import ModelForm
from apps.AnnouncementManagement.models import Announcement
from django import forms

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Input'}),
            'body' : forms.Textarea(attrs={'class':'form-control form-control-sm', 'placeholder':'Input'}),
            'image' : forms.FileInput(attrs={'class':'form-control', 'id':'file-2', 'accept':'image/*'}),
            'document' : forms.FileInput(attrs={'class':'form-control', 'id':'id_document', 'accept':'.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.zip,.rar', 'style':'display:none;'}),
        }
