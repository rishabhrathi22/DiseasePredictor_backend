from django.urls import path
from . import views

four_input_prediction = views.DiabetesViewSet.as_view({'post': 'fourInput'})
eight_input_prediction = views.DiabetesViewSet.as_view({'post': 'eightInput'})

urlpatterns = [
    path('predict4/', four_input_prediction),
    path('predict8/', eight_input_prediction),
]