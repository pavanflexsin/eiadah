from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from customer_service.forms import manage
from customer_service.models import Profile, CustomerServes


class ListCSAccountsView(ListView):
    model = Profile
    template_name = 'customer_service/manage/list.html'
    paginate_by = 10

    def get_queryset(self):
        center = self.request.session.get('center')
        self.queryset = Profile.objects.available(branch__center=center)
        return super().get_queryset()


class InactiveListCSAccountsView(ListView):
    model = Profile
    template_name = 'customer_service/manage/list.html'
    paginate_by = 10

    def get_queryset(self):
        center = self.request.session.get('center')
        self.queryset = Profile.objects.inactive().filter(branch__center=center)
        return super().get_queryset()


class CreateCSAccount(CreateView):
    model = CustomerServes
    template_name = 'customer_service/manage/creat_account.html'
    form_class = manage.CSAccountForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'center': self.request.session.get('center')})
        return kwargs

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('customer_service:edit_profile', kwargs={'pk': self.object.pk})


class CSEditAccount(UpdateView):
    model = Profile
    form_class = manage.EditCSAccountForm
    template_name = 'customer_service/manage/edit_account.html'

    def get_form(self,):
        form = super().get_form()
        user = self.object.user
        form.fields['username'].initial = user.username
        form.fields['phone_number'].initial = user.phone_number
        return form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'center': self.request.session.get('center')})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('customer_service:profile_overview', kwargs={'pk': self.object.pk})
