from django.urls import path
from . import views
from .views import AddCity, SubmitCity


urlpatterns = [
    path('', views.index, name='index'),
    path('cities/', views.cities, name='cities'),
    path('add-city/', AddCity.as_view(), name='add-city'),
    path('submit-city/', SubmitCity.as_view(), name='submit-city')
]
