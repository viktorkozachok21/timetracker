from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *

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

def project_detail(request, id):
    worker = get_object_or_404(Worker, user=request.user)
    project = get_object_or_404(Project, id=id)
    task_list = Task.objects.all().filter(project=project).order_by("is_completed")

    context = {
        'project': project,
        'worker': worker,
        'task_list': task_list,
    }

    return render(request, 'Tracker/project.html', context)

def add_comment(request, id):
    if request.method == 'POST' and request.is_ajax:
        comment = request.POST['comment']
        author = request.POST['author']
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)
        new_comment = Comment.objects.create(task=task, comments=comment, author=author)

        comments = Comment.objects.filter(task=task)

        comments_html = loader.render_to_string(
            'Tracker/comments.html',
            {'comments': comments, 'task': task_key}
        )

        return JsonResponse({"comments_html": comments_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def show_comments(request, id):
    if request.method == "GET" and request.is_ajax:
        task_key = request.GET['task']
        task = get_object_or_404(Task, id=task_key)

        comments = Comment.objects.filter(task=task)

        if comments:
            comments_html = loader.render_to_string(
                'Tracker/comments.html',
                {'comments': comments, 'task': task_key}
            )
        else:
            comments_html = "No comments"

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

def save_task(request, id):
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
            'Tracker/message_list.html',
            {'messages': messages}
        )

        changed_task = {
            'summary': task.summary,
            'messages_html': messages_html
        }

        return JsonResponse({"task":changed_task}, status=200)
    return JsonResponse({"success":False}, status=400)

def start_task(request, id):
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

def end_task(request, id):
    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        worker_key = request.POST['worker']
        task = get_object_or_404(Task, id=task_key)
        worker = get_object_or_404(Worker, id=worker_key)

        task.worker = None
        task.is_active = False
        task.save()

        timelog = TimeLog.objects.filter(task=task, worker=worker).order_by('-id')[0]

        comment = worker.last_name + " " + worker.first_name + " finished working!"
        timelog.end_comment = comment
        timelog.get_end()

        changed_task = {
            'task': task.id,
        }

        return JsonResponse({"task":changed_task}, status=200)
    return JsonResponse({"success":False}, status=400)

def completed_task(request, id):
    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)

        task.complete()
        return JsonResponse({"url": reverse("project_detail", args=[id])}, status=200)
    return JsonResponse({"success":False}, status=400)

def open_task(request, id):
    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)

        task.open()
        return JsonResponse({"url": reverse("project_detail", args=[id])}, status=200)
    return JsonResponse({"success":False}, status=400)

def get_time_logs(request, id):
    if request.method == "GET" and request.is_ajax:
        task_key = request.GET['task']
        task = get_object_or_404(Task, id=task_key)

        timelogs = TimeLog.objects.filter(task=task)

        timelogs_html = loader.render_to_string(
            'Tracker/timelogs.html',
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
            'Tracker/message_list.html',
            {'messages': messages}
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
            'Tracker/message_list.html',
            {'messages': messages}
        )

        return JsonResponse({"messages_html": messages_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def show_message(request, id):
    worker = get_object_or_404(Worker, user=request.user)
    message = get_object_or_404(Message, id=id, receiver=worker)

    message.status = ""
    message.save()

    context = {
        'message': message,
        'worker': worker
    }

    return render(request, 'Tracker/show_message.html', context)
