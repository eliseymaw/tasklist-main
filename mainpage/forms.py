from django import forms
from .models import Task, Geoposition, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'date_start', 'deadline', 'repeat_type', 'repeat_i', 'geop']

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Название"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="Описание"
    )
    date_start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        label="Дата начала"
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        label="Дата окончания"
    )
    repeat_type = forms.ChoiceField(
        choices=Task.PERIODS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Тип повторения"
    )
    repeat_i = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Количество повторов"
    )
    geop = forms.ModelChoiceField(
        queryset=Geoposition.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Геопозиция"
    )

class GeopositionForm(forms.ModelForm):
    class Meta:
        model = Geoposition
        fields = ['lat', 'lon']

    lat = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Широта"
    )
    lon = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Долгота"
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'avatar']

    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Напишите немного о себе...'
        }),
        label="О себе",
        required=False
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше местоположение'
        }),
        label="Местоположение",
        required=False
    )
    avatar = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label="Аватар",
        required=False
    )