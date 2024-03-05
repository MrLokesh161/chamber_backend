from django.urls import path
from .views import Form1ListCreateView

urlpatterns = [
    path('form1/', Form1ListCreateView.as_view(), name='form1-list-create'),
]
