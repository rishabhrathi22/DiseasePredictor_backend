from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

register_user = views.UserViewSet.as_view({'post': 'register'})

urlpatterns = [
   path('admin/', admin.site.urls),
   path('register/', register_user),
   path('diabetes/', include('diabetes.urls')),

   url('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]