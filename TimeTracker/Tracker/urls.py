from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('back_to_home/', views.back_to_home, name="back_to_home"),
    path('get_messages/', views.get_messages, name="get_messages"),
    path('to_trash/', views.to_trash, name="to_trash"),
    path('show_message/', views.show_message, name="show_message"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('project_detail/', views.project_detail, name="project_detail"),
    path('add_comment/', views.add_comment, name="add_comment"),
    path('show_comments/', views.show_comments, name="show_comments"),
    path('save_task/', views.save_task, name="save_task"),
    path('start_task/', views.start_task, name="start_task"),
    path('end_task/', views.end_task, name="end_task"),
    path('completed_task/', views.completed_task, name="completed_task"),
    path('open_task/', views.open_task, name="open_task"),
    path('get_time_logs/', views.get_time_logs, name="get_time_logs"),
]
