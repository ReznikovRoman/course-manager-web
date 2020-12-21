from django.urls import path

from . import views


######################################################################################################################

app_name = 'accounts'

urlpatterns = [
    path('profile/create/', views.ProfileCreate.as_view(), name='profile-create'),
]





