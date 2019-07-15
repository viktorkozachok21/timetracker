from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *

from django.db.models import Sum

import json
from datetime import datetime
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    context = {}

    if request.user.is_authenticated:
        worker = get_object_or_404(Worker, user=request.user)
        context['worker'] = worker
    projects_list = Project.objects.all()

    paginator = Paginator(projects_list, 30)
    page = request.GET.get('page')
    try:
        projects_list = paginator.page(page)
    except PageNotAnInteger:
        projects_list = paginator.page(1)
    except EmptyPage:
        projects_list = paginator.page(paginator.num_pages)

    context['projects_list'] = projects_list
    context['page'] = page

    return render(request, 'Tracker/home.html', context)

def back_to_home(request):
    if request.method == "GET" and request.is_ajax:
        worker = get_object_or_404(Worker, user=request.user)
        projects_list = Project.objects.all()

        paginator = Paginator(projects_list, 30)
        page = request.GET.get('page')
        try:
            projects_list = paginator.page(page)
        except PageNotAnInteger:
            projects_list = paginator.page(1)
        except EmptyPage:
            projects_list = paginator.page(paginator.num_pages)

        home_html = loader.render_to_string(
                'Tracker/backtohome.html',
                {'projects_list': projects_list, 'worker': worker, 'page': page, 'user': request.user}
            )

        return JsonResponse({"home_html": home_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def project_detail(request):
    if request.method == "GET" and request.is_ajax:
        project_key = request.GET['project']
        worker = get_object_or_404(Worker, user=request.user)
        project = get_object_or_404(Project, id=project_key)

        task_list = Task.objects.all().filter(project=project)

        project_html = loader.render_to_string(
                'Tracker/project.html',
                {'project': project, 'worker': worker, 'task_list': task_list, 'user': request.user}
            )

        return JsonResponse({"project_html": project_html}, status=200)
    return JsonResponse({"success":False}, status=400)


    return render(request, 'Tracker/project.html', context)

def add_comment(request):
    if request.method == 'POST' and request.is_ajax:
        comment = request.POST['comment']
        author = request.POST['author']
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)
        new_comment = Comment.objects.create(task=task, comments=comment, author=author)

        comments = Comment.objects.filter(task=task)

        comments_html = loader.render_to_string(
            'Tracker/content.html',
            {'comments': comments, 'task': task_key}
        )

        return JsonResponse({"comments_html": comments_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def show_comments(request):
    if request.method == "GET" and request.is_ajax:
        task_key = request.GET['task']
        task = get_object_or_404(Task, id=task_key)

        comments = Comment.objects.filter(task=task)

        if comments:
            comments_html = loader.render_to_string(
                'Tracker/content.html',
                {'comments': comments, 'task': task_key}
            )
        else:
            comments_html = "<h5>No comments</h5>"

        return JsonResponse({"comments_html": comments_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('home'))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def save_task(request):
    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        worker_key = request.POST['worker']
        new_summary = request.POST['summary']
        task = get_object_or_404(Task, id=task_key)

        author_key = task.author
        worker = get_object_or_404(Worker, id=worker_key)
        author = get_object_or_404(Worker, user=author_key)
        old_summary = task.summary

        title = "Changed task summary: " + task.project.project_name + " ~ " + task.title


        message_context = "<h2>Worker: " + worker.last_name + " " + worker.first_name + " changed task: " + task.title + " ( " + task.project.project_name + " )</h2>" + "<h3>Old summary:</h3>" + old_summary + "<h3>New summary:</h3>" + new_summary

        message_to_worker = Message.objects.create(receiver=worker, title=title, message=message_context)
        message_to_author = Message.objects.create(receiver=author, title=title, message=message_context)

        task.summary = new_summary
        task.save()

        messages = Message.objects.filter(receiver=worker)

        messages_html = loader.render_to_string(
            'Tracker/content.html',
            {'messages': messages}
        )

        changed_task = {
            'summary': task.summary,
            'messages_html': messages_html
        }

        return JsonResponse({"task":changed_task}, status=200)
    return JsonResponse({"success":False}, status=400)

def start_task(request):
    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        worker_key = request.POST['worker']
        task = get_object_or_404(Task, id=task_key)
        worker = get_object_or_404(Worker, id=worker_key)

        task.worker = worker
        task.is_active = True
        task.save()

        comment = worker.last_name + " " + worker.first_name + " started working!"

        timelog = TimeLog.objects.create(task=task, worker=worker, start_comment=comment)

        changed_task = {
            'task': task.id,
            'worker': task.worker.last_name + " " + task.worker.first_name
        }

        return JsonResponse({"task":changed_task}, status=200)
    return JsonResponse({"success":False}, status=400)

def end_task(request):
    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        worker_key = request.POST['worker']
        task = get_object_or_404(Task, id=task_key)
        worker = get_object_or_404(Worker, id=worker_key)

        timelog = TimeLog.objects.filter(task=task, worker=worker)[0]

        comment = worker.last_name + " " + worker.first_name + " finished working!"
        timelog.end_comment = comment
        timelog.get_end()

        timelog_list = TimeLog.objects.filter(task=task, is_completed=True)

        hour, minute, second = 0, 0, 0

        for log in timelog_list:
            hour += log.spend_time.hour
            minute += log.spend_time.minute
            second += log.spend_time.second

        if hour < 10:
            hours = "0" + str(hour)
        else:
            hours = str(hour)

        if minute < 10:
            minutes = "0" + str(minute)
        else:
            minutes = str(minute)

        if second < 10:
            seconds = "0" + str(second)
        else:
            seconds = str(second)

        start_time = hours + ":" + minutes + ":" + seconds

        task.spend_time = start_time
        task.worker = None
        task.is_active = False
        task.save()

        context = {
            'task': task.id,
            'spend_time': task.spend_time
        }

        return JsonResponse({"context":context}, status=200)
    return JsonResponse({"success":False}, status=400)

def completed_task(request):
    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)

        task.complete()

        task_block = loader.render_to_string(
            'Tracker/content.html',
            {'task': task, 'user': request.user}
        )

        return JsonResponse({"task_block": task_block}, status=200)
    return JsonResponse({"success":False}, status=400)

def open_task(request):
    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)
        worker = get_object_or_404(Worker, user=request.user)

        task.open()

        task_block = loader.render_to_string(
            'Tracker/content.html',
            {'task': task, 'user': request.user, 'worker': worker}
        )

        return JsonResponse({"task_block": task_block}, status=200)
    return JsonResponse({"success":False}, status=400)

def get_time_logs(request):
    if request.method == "GET" and request.is_ajax:
        task_key = request.GET['task']
        task = get_object_or_404(Task, id=task_key)

        timelogs = TimeLog.objects.filter(task=task)

        timelogs_html = loader.render_to_string(
            'Tracker/content.html',
            {'timelogs': timelogs}
        )

        return JsonResponse({"timelogs_html": timelogs_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def get_messages(request):
    if request.method == "GET" and request.is_ajax:
        worker_key = request.GET['worker']
        worker = get_object_or_404(Worker, id=worker_key)

        messages = Message.objects.filter(receiver=worker)

        messages_html = loader.render_to_string(
            'Tracker/content.html',
            {'message_list': messages}
        )

        return JsonResponse({"messages_html": messages_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def to_trash(request):
    if request.method == "POST" and request.is_ajax:
        worker_key = request.POST['worker']
        message_key = request.POST['message']
        worker = get_object_or_404(Worker, id=worker_key)
        message = get_object_or_404(Message, id=message_key)

        message.delete()

        messages = Message.objects.filter(receiver=worker)

        messages_html = loader.render_to_string(
            'Tracker/content.html',
            {'message_list': messages}
        )

        return JsonResponse({"messages_html": messages_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def show_message(request):
    if request.method == "GET" and request.is_ajax:
        worker_key = request.GET['worker']
        message_key = request.GET['message']
        worker = get_object_or_404(Worker, id=worker_key)
        message = get_object_or_404(Message, id=message_key, receiver=worker)

        message.read()

        message_html = loader.render_to_string(
            'Tracker/content.html',
            {'new_message': message}
        )

        return JsonResponse({"message_html": message_html}, status=200)
    return JsonResponse({"success":False}, status=400)
