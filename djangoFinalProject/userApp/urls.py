from django.urls import path
from . import views

urlpatterns = [
    path('prediction/', views.prediction, name='prediction'),
    path('predict_crop/', views.predict_crop, name='predict_crop'),
]
