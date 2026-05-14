from django.urls import path
from .import views

urlpatterns =[
    path('', views.records, name='records'),
    path('/dashboard/add_task/',views.add_task),
    path('dashboard/',views.dashboard),
]