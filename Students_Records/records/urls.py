from django.urls import path
from . import views

urlpatterns =[
    path('',views.login_view, name='login'),
    path('Dashboard/', views.records, name='records'),
    path('home/',views.add_task, name='add new record'),
    path('add_task/',views.add_task, name='add_task'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('edit_task/<int:id>/',views.edit_task, name='edit_task'),
    path('delete_task/<int:id>/',views.delete_task, name='delete_task'),
    path('testing',views.filter_records,name='testing'),
]