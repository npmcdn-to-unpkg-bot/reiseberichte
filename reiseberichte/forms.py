from django import forms
from .models import Tag

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['reisetag', 'foto', 'ort', 'beschreibung', 'koordinaten', 'koordinateneckig',]