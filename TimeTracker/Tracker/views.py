from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *

import json
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
    task_list = Task.objects.all().filter(project=project)

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

        comments_html = loader.render_to_string(
            'Tracker/comments.html',
            {'comments': comments, 'task': task_key}
        )

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
    return HttpResponseRedirect('/')

def save_task(request, id):
    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        new_summary = request.POST['summary']
        task = get_object_or_404(Task, id=task_key)

        task.summary = new_summary
        task.save()

        changed_task = {
            'summary':task.summary
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

        changed_task = {
            'task': task.id,
            'worker': task.worker.last_name + " " + task.worker.first_name
        }

        return JsonResponse({"task":changed_task}, status=200)
    return JsonResponse({"success":False}, status=400)

def end_task(request, id):
    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)

        task.worker = None
        task.is_active = False
        task.save()

        changed_task = {
            'task': task.id,
        }

        return JsonResponse({"task":changed_task}, status=200)
    return JsonResponse({"success":False}, status=400)
