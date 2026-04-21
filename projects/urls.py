from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('create-project/', views.project_create, name='project_create'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('<int:project_id>/complete/', views.project_complete, name='project_complete'),
    path('<int:project_id>/toggle-participate', views.toggle_participate, name='toggle_participate'),
]
