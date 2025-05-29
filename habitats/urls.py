from django.urls import path
from . import views

app_name = 'habitats'

urlpatterns = [
    path('', views.habitat_list, name='habitat_list'),
    path('add/', views.habitat_add, name='habitat_add'),
    path('<str:nama_habitat>/', views.habitat_detail, name='habitat_detail'),
    path('<str:nama_habitat>/edit/', views.habitat_edit, name='habitat_edit'),
    path('<str:nama_habitat>/delete/', views.habitat_delete, name='habitat_delete'),
]