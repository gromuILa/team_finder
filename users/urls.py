from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('list/', views.participants, name='participants'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('skills/', views.skills_autocomplete, name='skills_autocomplete'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('<int:user_id>/skills/add', views.skill_add, name='skill_add'),
    path('<int:user_id>/skills/<int:skill_id>/remove/', views.skill_remove, name='skill_remove'),
]
