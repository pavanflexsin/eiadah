from django import forms

from customer_service.models import Profile
from utility.forms import AvatarWidget
from center.models import Branch, Department


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=AvatarWidget)

    class Meta:
        model = Profile
        exclude = 'active', 'deleted', 'user', 'branch', 'department',
    
    def save(self):        
        email = self.cleaned_data.pop('email')
        instance = super().save()
        instance.user.email = email
        instance.user.save()
        return instance


class EditDepartmentForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = 'department',

    def __init__(self, *args, **kwargs):
        center = kwargs.pop("center")     # client is the parameter passed from views.py
        super().__init__(*args, **kwargs)
        self.fields['department'] = forms.ModelMultipleChoiceField(
            queryset=Department.objects.filter(branches__center=center, parent__isnull=True).distinct(),
            required=True,
            widget=forms.CheckboxSelectMultiple()
        )

    def save(self):
        department = self.cleaned_data.pop('department')
        profile = self.instance
        profile.department.set(department, clear=True)
        return profile



