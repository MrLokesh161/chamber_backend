from django.contrib import admin
from django.urls import path, include
from chamber.views import CustomAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('obtainAuthToken/',CustomAuthToken.as_view()),
    path('api/', include('chamber.urls')),
]
