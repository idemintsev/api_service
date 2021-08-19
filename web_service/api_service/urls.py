from django.urls import path
from api_service.api import DealsView, FileUploadView


urlpatterns = [
    path('deals/', DealsView.as_view(), name='deals'),
    path('upload/', FileUploadView.as_view())
]
