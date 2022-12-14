from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.forms import inlineformset_factory

from django.forms.widgets import NumberInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from rest_framework import serializers

from .models import *

from django import forms


class UserCreationForm(UserCreationForm):
    # email = EmailField(label=_("Email address"), required=True,
    #                    help_text=_("Required."))
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('Ten adres email jest już zarejestrownay. Spróbuj innego.')
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('osoba', 'zawody',)


# class ProfileForm2(forms.ModelForm):
#     class Meta:
#         model = ProfileZawodnik
#         fields = ('wiek' 'telefon' 'email' 'adres' 'team')


class WojForm(forms.ModelForm):
    class Meta:
        model = Wojewodztwo
        fields = ('id', 'woj_nazwa')


class AcodeForm2(forms.ModelForm):
    class Meta:
        model = Acode
        fields = ('ZIP', 'Miasto', 'Woj')


class AcodeForm3(forms.ModelForm):
    class Meta:
        model = Acode
        exclude = ()


class AdresForm(forms.ModelForm):
    # category_name = serializers.ReadOnlyField(source='Acode.Miasto')

    class Meta:
        model = Adres
        exclude = ()
        # fields = "__all__"


cos = inlineformset_factory(Acode, Adres, form=AdresForm, fields=['Ulica', 'NrDomu', 'NrLokalu'], extra=1, max_num=1)
cos2 = inlineformset_factory(Adres, Acode, form=AcodeForm3, fields=['Miasto', 'ZIP', 'Woj'], extra=1, max_num=1)


class AcodeForm(forms.ModelForm):

    class Meta:
        model = Acode
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(AcodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('Miasto'),
                Field('ZIP'),
                Field('Woj'),
                Fieldset('Adres 2',
                         Formset('titles')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )


class AdresForm2(forms.ModelForm):
    # category_name = serializers.ReadOnlyField(source='Acode.Miasto')

    class Meta:
        model = Adres
        fields = "__all__"


class AdresForm3(forms.ModelForm):

    class Meta:
        model = Adres
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(AdresForm3, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Fieldset('',
                         Formset('titles')),
                HTML("<br>"),
                HTML("Adres 2"),
                Field('Ulica'),
                Field('NrDomu'),
                Field('NrLokalu'),
                ButtonHolder(Submit('submit', 'save')),
            )
        )


class StadionForm(forms.ModelForm):
    class Meta:
        model = Stadion
        fields = 'stadion_nazwa', 'pojemnosc_trybun', 'niepelnosprawni', 'stadion_adres', 'stadion_zdjecie'


class ZawodyForm(forms.ModelForm):
    class Meta:
        model = Zawody
        fields = 'zawody_nazwa', 'zawody_data', 'aff_url', 'stadion',


class VoteForm(forms.ModelForm):
    nawierzchnia = forms.IntegerField(
        widget=NumberInput(attrs={'placeholder': '5', 'type': 'range', 'min': '1', 'max': '10', 'class': 'nawierzchnia', }))
    szatnie = forms.IntegerField(
        widget=NumberInput(attrs={'placeholder': '5', 'type': 'range', 'min': '1', 'max': '10', 'class': 'szatnie', }))
    organizacja = forms.IntegerField(
        widget=NumberInput(attrs={'placeholder': '5', 'type': 'range', 'min': '1', 'max': '10', 'class': 'organizacja', }))

    class Meta:
        model = Vote
        fields = ('nawierzchnia', 'szatnie', 'organizacja')


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'


class OsobaForm(forms.ModelForm):
    class Meta:
        model = Osoba
        fields = '__all__'
        # fields = 'imie', 'nazwisko', 'data_urodzenia', 'telefon', 'email', 'zdjecie', 'adres', 'status', 'team'


class LZForm(forms.ModelForm):
    class Meta:
        model = Lista_Zawodnikow
        fields = '__all__'


class DyscForm(forms.ModelForm):
    class Meta:
        model = Dyscyplina
        fields = 'dyscyplina_nazwa',


class SzatniaForm(forms.ModelForm):
    class Meta:
        model = Szatnia
        fields = '__all__'
