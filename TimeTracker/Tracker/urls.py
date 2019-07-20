from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('user_login/', views.user_login, name="user_login"),
    # path('back_to_home/', views.back_to_home, name="back_to_home"),
    path('user_logout/', views.user_logout, name="user_logout"),

    path('add_worker/', views.add_worker, name="add_worker"),
    path('change_worker/', views.change_worker, name="change_worker"),
    path('get_workers/', views.get_workers, name="get_workers"),
    path('block_worker/', views.block_worker, name="block_worker"),
    path('remove_worker/', views.remove_worker, name="remove_worker"),
    # path('change_avatar/', views.change_avatar, name="change_avatar"),
    path('remove_worker/', views.remove_worker, name="remove_worker"),

    path('add_project/', views.add_project, name="add_project"),
    path('project_detail/', views.project_detail, name="project_detail"),
    path('change_project/', views.change_project, name="change_project"),
    path('complet_project/', views.complet_project, name="complet_project"),
    path('open_project/', views.open_project, name="open_project"),
    path('remove_project/', views.remove_project, name="remove_project"),

    path('add_task/', views.add_task, name="add_task"),
    path('save_task/', views.save_task, name="save_task"),
    path('change_task/', views.change_task, name="change_task"),
    path('start_task/', views.start_task, name="start_task"),
    path('end_task/', views.end_task, name="end_task"),
    path('completed_task/', views.completed_task, name="completed_task"),
    path('open_task/', views.open_task, name="open_task"),
    path('remove_task/', views.remove_task, name="remove_task"),

    path('add_comment/', views.add_comment, name="add_comment"),
    path('show_comments/', views.show_comments, name="show_comments"),

    path('get_time_logs/', views.get_time_logs, name="get_time_logs"),
    path('show_time_logs/', views.show_time_logs, name="show_time_logs"),
    path('remove_time_log/', views.remove_time_log, name="remove_time_log"),

    path('get_messages/', views.get_messages, name="get_messages"),
    path('show_message/', views.show_message, name="show_message"),
    path('remove_message/', views.remove_message, name="remove_message"),
]
