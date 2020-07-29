from django.urls import path, include

from customer_service.views import manage, profile

app_name = 'customer_service'

urlpatterns = [
    path('manage/', include([
        path('<int:pk>/edit/', manage.CSEditAccount.as_view(), name='manage_edit_account'),
        path('add/', manage.CreateCSAccount.as_view(), name='manage_create_account'),
        path('inactive/', manage.InactiveListCSAccountsView.as_view(), name='manage_inactive_list'),
        path('', manage.ListCSAccountsView.as_view(), name='manage_list')
    ])),
    path('<int:pk>/', include([
        path('password/', profile.ChangePasswordView.as_view(), name='edit_password'),
        path('departments/', profile.ChangeDepartmentView.as_view(), name='edit_department'),
        path('edit-profile/', profile.CSEditProfile.as_view(), name='edit_profile'),
        path('', profile.ProfileOverView.as_view(), name='profile_overview'),
    ])),
]
