"""
URL mappings for the user API
"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    # .as_view() method to get view function
    # changes class based function (drf) into django supported view
    # not entirely sure what that means
    # name is for reverse in testing
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me')
]
