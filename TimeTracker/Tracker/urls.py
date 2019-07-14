from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('get_messages/', views.get_messages, name="get_messages"),
    path('to_trash/', views.to_trash, name="to_trash"),
    path('show_message/<id>', views.show_message, name="show_message"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('<id>/', views.project_detail, name="project_detail"),
    path('<id>/add_comment/', views.add_comment, name="add_comment"),
    path('<id>/show_comments/', views.show_comments, name="show_comments"),
    path('<id>/save_task/', views.save_task, name="save_task"),
    path('<id>/start_task/', views.start_task, name="start_task"),
    path('<id>/end_task/', views.end_task, name="end_task"),
    path('<id>/completed_task/', views.completed_task, name="completed_task"),
    path('<id>/open_task/', views.open_task, name="open_task"),
    path('<id>/get_time_logs/', views.get_time_logs, name="get_time_logs"),
]
