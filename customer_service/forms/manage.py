from django import forms
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField

from center.models import Branch, Department
from customer_service.models import CustomerServes, Profile

Users = get_user_model()


class CSAccountForm(forms.ModelForm):
    GENDER_TYPE = (
        (1, _('Male')),
        (2, _('Female')),
    )

    phone_number = PhoneNumberField(initial='+966')
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    first_name_en = forms.CharField(required=True)
    first_name_ar = forms.CharField(required=True)
    last_name_en = forms.CharField(required=True)
    last_name_ar = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    birth_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        center = kwargs.pop("center")     # client is the parameter passed from views.py
        super().__init__(*args, **kwargs)
        self.fields['branch'] = forms.ModelChoiceField(queryset=Branch.objects.filter(center=center).distinct())
        self.fields['department'] = forms.ModelMultipleChoiceField(
            queryset=Department.objects.filter(branches__center=center, parent__isnull=True).distinct(),
            required=True,
            widget=forms.CheckboxSelectMultiple()
        )

    class Meta:
        model = CustomerServes
        fields = 'password', 'phone_number', 'username'

    def save(self):
        doctor_profile = {
            'first_name_en': self.cleaned_data.pop('first_name_en'),
            'first_name_ar': self.cleaned_data.pop('first_name_ar'),
            'last_name_en': self.cleaned_data.pop('last_name_en'),
            'last_name_ar': self.cleaned_data.pop('last_name_ar'),
            # 'email': self.cleaned_data.pop('email'),
            'gender': self.cleaned_data.pop('gender'),
            'birth_date': self.cleaned_data.pop('birth_date'),
            'branch': self.cleaned_data.pop('branch'),
        }
        department = self.cleaned_data.pop('department')
        instance = CustomerServes.objects.create_user(**self.cleaned_data)
        profile, created = Profile.objects.update_or_create(user=instance, **doctor_profile)
        profile.department.add(*department)
        return profile


class EditCSAccountForm(forms.ModelForm):
    username = forms.CharField()
    phone_number = PhoneNumberField()

    class Meta:
        model = Profile
        fields = 'branch', 'department', 'active',

    def __init__(self, *args, **kwargs):
        center = kwargs.pop("center")     # client is the parameter passed from views.py
        super().__init__(*args, **kwargs)
        self.fields['branch'] = forms.ModelChoiceField(queryset=Branch.objects.filter(center=center).distinct())
        self.fields['department'] = forms.ModelMultipleChoiceField(
            queryset=Department.objects.filter(branches__center=center, parent__isnull=True).distinct(),
            required=True,
            widget=forms.CheckboxSelectMultiple()
        )

    def clean_phone_number(self):
        field = self.cleaned_data['phone_number']
        if Users.objects.exclude(pk=self.instance.user.pk).filter(phone_number=field).exists():
            raise ValidationError('Phone already exists')
        return field

    def clean_username(self):
        field = self.cleaned_data['username']
        if Users.objects.exclude(pk=self.instance.user.pk).filter(username=field).exists():
            raise ValidationError('User Name already exists')
        return field

    def save(self):
        active = self.cleaned_data.get('active')
        user_data = {
            'username': self.cleaned_data.pop('username'),
            'phone_number': self.cleaned_data.pop('phone_number'),
            'is_active': True if active else False
        }
        Users.objects.update_or_create(agent=self.instance, defaults=user_data)
        return super().save()
