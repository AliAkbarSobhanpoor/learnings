from django import forms
from . import models

class ChatMessageCreateForm(forms.ModelForm):
    class Meta:
        model = models.RoomMessage
        fields = ["body"]

        widgets = {
            "body": forms.TextInput(
                attrs={
                    "placeholder": "add message ...",
                    "class": "p-4 text-block",
                    "maxlength": "300",
                    "autofocus": True,
                }
            )
        }