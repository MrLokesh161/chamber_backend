from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import test_token, signupview, create_form1, create_form2
#  ,
urlpatterns = [
    path('test_token/', test_token, name="test_token"),
    path('signup/', signupview, name='signup'),
    path('form1/', create_form1, name='create_form1'),
    path('form2/<int:form1_instance_id>/', create_form2, name='create_form2'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    