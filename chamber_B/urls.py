from django.contrib import admin
from django.urls import path, include
from chamber.views import CustomAuthToken
from . import settings
from django.conf.urls.static import static
from chamber.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('obtainAuthToken/',CustomAuthToken.as_view()),
    path('api/', include('chamber.urls')),
    path('', home_page, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)