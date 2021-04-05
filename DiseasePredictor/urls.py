from django.contrib import admin
from django.urls import path, include
from . import views

register_user = views.UserViewSet.as_view({'post': 'register'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user),
    path('diabetes/', include('diabetes.urls')),
]