from django import forms

from .models import Osoba, Telefon, Email

class TelefonForm(forms.ModelForm):

    class Meta:
        model = Telefon
        fields = ('telefon',)

class EmailForm(forms.ModelForm):

    class Meta:

        model = Email
        fields = ('email',)

class KontaktForm(forms.ModelForm):

    class Meta:
        model = Osoba
        #fields = ('imie', 'nazwisko', 'telefon', 'email',)
        fields = ('imie', 'nazwisko',)