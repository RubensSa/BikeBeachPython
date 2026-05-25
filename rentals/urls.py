from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('', views.home, name='home'),
    path('bikes/', views.bike_list, name='bike_list'),
    path('bikes/create/', views.bike_create, name='bike_create'),
    path('bikes/<int:pk>/', views.bike_detail, name='bike_detail'),
    path('bikes/<int:pk>/edit/', views.bike_edit, name='bike_edit'),
    path('bikes/<int:pk>/delete/', views.bike_delete, name='bike_delete'),
    path('bikes/<int:pk>/rent/', views.rent_bike, name='rent_bike'),
    path('alugueis/', views.my_rentals, name='my_rentals'),
    path('alugueis/<int:pk>/return/', views.return_bike, name='return_bike'),
]
