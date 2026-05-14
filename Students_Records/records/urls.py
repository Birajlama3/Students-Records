from django.urls import path
from . import views

urlpatterns =[
    path('', views.records, name='records'),
    path('add_task/',views.add_task, name='add_task'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('edit_task/<int:id>/',views.edit_task, name='edit-task'),
    path('delete_task/<int:id>/',views.delete_task, name='delete-task'),
]