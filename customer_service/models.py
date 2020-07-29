from django.db import models
from django.urls import reverse

from account.models import UserManager, Users
from utility.models import PersonalInformation, BaseModel


class CustomerServiceManager(UserManager):
    """
    Custom manager to deal with all Customer Service entity
    """

    def get_queryset(self):
        """
        override default queryset
        """
        return super(CustomerServiceManager, self).get_queryset().filter(role=3)

    def create_user(self, **extra_fields):
        """
        set role for this entity
        and make entity staff
        """
        extra_fields.setdefault('role', 3)
        extra_fields.setdefault('is_staff', True)
        return super(CustomerServiceManager, self).create_user(**extra_fields)


class CustomerServes(Users):
    """
    Customer Serves Proxy class
    """

    objects = CustomerServiceManager()

    class Meta:
        proxy = True


class Profile(PersonalInformation, BaseModel):
    user = models.OneToOneField('customer_service.CustomerServes', on_delete=models.CASCADE, related_name='agent')
    branch = models.ForeignKey('center.Branch', on_delete=models.CASCADE, related_name='agent')
    department = models.ManyToManyField('center.Department', related_name='agent')

    def get_absolute_url(self):
        return reverse("customer_service:profile_overview", kwargs={"pk": self.pk})
