from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api_service.api import DealsView, Logout, LoginView

urlpatterns = [
    path('auth/', obtain_auth_token, name='token'),
    path('logout/', Logout.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),

    path('deals/', DealsView.as_view(), name='deals'),
]
