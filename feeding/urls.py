from django.urls import path
from . import views

urlpatterns = [
    path('', views.feeding_list, name='feeding_list'),  # Tampilkan daftar pemberian pakan
    path('add/', views.add_feeding, name='add_feeding'),  # Tambah jadwal
    path('edit/<str:feeding_id>/', views.edit_feeding, name='edit_feeding'),  # Edit jadwal
    path('delete/<str:feeding_id>/', views.delete_feeding, name='delete_feeding'),  # Hapus jadwal
    path('mark_as_done/<str:feeding_id>/', views.mark_as_done, name='mark_as_done'),  # Tandai selesai
]
