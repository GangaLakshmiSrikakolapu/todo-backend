from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('profile/', views.profile),

    path('tasks/', views.get_tasks),
    path('tasks/add/', views.add_task),
    path('tasks/delete/<int:pk>/', views.delete_task),
    path('tasks/complete/<int:pk>/', views.complete_task),
]