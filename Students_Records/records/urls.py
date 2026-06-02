from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns =[
    path('',views.login_view, name='login'),
    path('Dashboard/', views.records, name='records'),
    path('home/',views.add_task, name='add new record'),
    path('add_task/',views.add_task, name='add_task'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('edit_task/<int:id>/',views.edit_task, name='edit_task'),
    path('delete_task/<int:id>/',views.delete_task, name='delete_task'),
    path('api/records/',views.api_records,name='api_records'),
    path('api/records/create_records',views.create_records,name='create_records'),
    path('api/records/records_details/<int:id>',views.records_details,name='records_details'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/posts/',views.post_list ,name ="post_list"),
    path('home_view/', views.home_view, name="home_view"),
]