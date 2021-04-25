from django.urls import path
from . import views

prediction = views.PneumoniaViewSet.as_view({'post': 'predict'})

urlpatterns = [
    path('predict/', prediction)
]