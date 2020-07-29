from django.contrib.auth.views import PasswordChangeView
from django.views.generic import UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render

from customer_service.models import Profile, CustomerServes
from customer_service.forms import profile


class ProfileOverView(DetailView):
    model = Profile
    template_name = 'customer_service/overview.html'


class CSEditProfile(UpdateView):
    model = Profile
    form_class = profile.EditProfileForm
    template_name = 'customer_service/edit_profile.html'

    def get_success_url(self):
        return reverse_lazy('customer_service:profile_overview', kwargs={'pk': self.object.pk})


class ChangePasswordView(PasswordChangeView):
    model = CustomerServes
    template_name = 'customer_service/change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        return reverse_lazy('customer_service:profile_overview', kwargs={'pk': self.object.pk})


class ChangeDepartmentView(UpdateView):
    model = Profile
    form_class = profile.EditDepartmentForm
    template_name = 'customer_service/change_department.html'

    def dispatch(self, request, *args, **kwargs):
        center = self.request.session.get('center', None)
        if request.user.role != 3 and center:
            return super(ChangeDepartmentView, self).dispatch(request, *args, **kwargs)
        return render(request, '404.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'center': self.request.session.get('center')})
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Customer Service details updated!')
        return reverse_lazy('customer_service:profile_overview', kwargs={'pk': self.object.pk})
