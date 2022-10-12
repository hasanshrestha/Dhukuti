from django import forms
from .models import Files


class FilesForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = "__all__"
        labels = {
            "title": "",
            "description": "",
            "file": "",
        }
        widgets = {
            "title": forms.HiddenInput(),
            "description": forms.HiddenInput(),
            "file": forms.FileInput(attrs={"accept": "application/pdf"}),
        }


# accept="image/png, image/gif, image/jpeg"
