from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

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
diabetes_past_records = views.UserViewSet.as_view({'post': 'getDiabetesPastRecords'})
pneumonia_past_records = views.UserViewSet.as_view({'post': 'getPneumoniaPastRecords'})
single_diabetes_past_record = views.UserViewSet.as_view({'post': 'getDiabetesSinglePastRecord'})
single_pneumonia_past_record = views.UserViewSet.as_view({'post': 'getPneumoniaSinglePastRecord'})

urlpatterns = [
   path('admin/', admin.site.urls),
   path('register/', register_user),

   path('diabetesRecords/', diabetes_past_records),
   path('singleDiabetesRecord/', single_diabetes_past_record),

   path('pneumoniaRecords/', pneumonia_past_records),
   path('singlePneumoniaRecord/', single_pneumonia_past_record),

   path('diabetes/', include('diabetes.urls')),
   path('pneumonia/', include('pneumonia.urls')),

   url('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]