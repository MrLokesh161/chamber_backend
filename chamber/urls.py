from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import create_form1

urlpatterns = [
    path('form1/', create_form1, name='create-form1'),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
