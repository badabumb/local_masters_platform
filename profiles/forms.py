from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'city', 'about', 'is_master']
        labels = {
            'name': 'Имя',
            'city': 'Город',
            'about': 'Описание профиля',
            'is_master': 'Я мастер',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_master': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
