from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template import loader
from datetime import datetime
import time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):

    context = {}

    if request.user.is_authenticated:
        worker = get_object_or_404(Worker, user=request.user)
        context['worker'] = worker
    else:
        return HttpResponseRedirect(reverse('user_login'))

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

# def back_to_home(request):
#
#     if request.method == "GET" and request.is_ajax:
#         worker = get_object_or_404(Worker, user=request.user)
#         projects_list = Project.objects.all()
#
#         paginator = Paginator(projects_list, 5)
#         page = request.GET.get('page')
#         try:
#             projects_list = paginator.page(page)
#         except PageNotAnInteger:
#             projects_list = paginator.page(1)
#         except EmptyPage:
#             projects_list = paginator.page(paginator.num_pages)
#
#         home_html = loader.render_to_string(
#                 'Tracker/content.html',
#                 {'projects_list': projects_list, 'worker': worker, 'page': page, 'user': request.user}
#             )
#
#         return JsonResponse({"home_html": home_html}, status=200)
#     return JsonResponse({"success":False}, status=400)

def user_login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user.is_superuser:
            login(request,user)
            return JsonResponse({"success":True}, status=200)
        if user:
            worker = get_object_or_404(Worker, user=user)
            if worker.is_blocked:
                return JsonResponse({"success":False, "message":"You have blocked access, please contact the administrator for details."}, status=200)
            elif user.is_active:
                login(request,user)
                return JsonResponse({"success":True}, status=200)
        else:
            return JsonResponse({"success":False, "message":"Username or password is incorrect! Please try again."}, status=200)

    return render(request, 'Tracker/login.html', {})

def user_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse('user_login'))

#worker views block
def add_worker(request):

    if request.method == "GET" and request.is_ajax:
        user_form = UserForm()
        worker_form = WorkerForm()
        csrf_token_value = request.COOKIES['csrftoken']
        form_html = loader.render_to_string(
            'Tracker/forms.html',
            {'new_user_form': user_form, 'new_worker_form': worker_form, "csrf_token_value": csrf_token_value}
        )
        return JsonResponse({"form_html": form_html}, status=200)

    if request.method == "POST" and request.is_ajax:
        user_form = UserForm(request.POST)
        worker_form = WorkerForm(request.POST)
        if user_form.is_valid() and worker_form.is_valid():
            new_user_email = request.POST['email']
            if User.objects.filter(email__iexact=new_user_email).exists():
                return JsonResponse({"success":False, "message":"User with this email already exists!"}, status=200)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user = user_form.save()
            user.set_password(user.password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            worker = worker_form.save()
            worker.user = user
            worker.save()
            return JsonResponse({"success":True}, status=200)
        username = request.POST['username']
        if User.objects.filter(username__iexact=username).exists():
            return JsonResponse({"success":False, "message":"User with this username already exists!"}, status=200)
        else:
            return JsonResponse({"success":False, "message":"You did not fill all the fields!"}, status=200)
    return JsonResponse({"success":False}, status=400)

def get_workers(request):

    if request.method == "GET" and request.is_ajax:
        workers_list = Worker.objects.all()
        workers_html = loader.render_to_string(
            'Tracker/content.html',
            {'workers_list': workers_list}
        )
        return JsonResponse({"workers_html": workers_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def change_worker(request):

    if request.method == "GET" and request.is_ajax:
        worker_key = request.GET['worker']
        worker = get_object_or_404(Worker, id=worker_key)
        selected_worker = worker.id
        worker_form = WorkerForm(instance=worker)
        csrf_token_value = request.COOKIES['csrftoken']
        form_html = loader.render_to_string(
            'Tracker/forms.html',
            {'edit_worker_form': worker_form, "csrf_token_value": csrf_token_value, 'selected_worker': selected_worker, 'email': worker.user.email}
        )
        return JsonResponse({"form_html": form_html}, status=200)

    if request.method == "POST" and request.is_ajax:
        worker_form = WorkerForm(request.POST, request.FILES)
        if worker_form.is_valid():
            selected_worker = request.POST['selected_worker']
            worker = get_object_or_404(Worker, id=selected_worker)
            print("true")
            new_user_email = request.POST['email']
            if User.objects.filter(email__iexact=new_user_email).exclude(email=worker.user.email).exists():
                return JsonResponse({"success":False, "message":"User with this email already exists!"}, status=200)
            worker.user.email = new_user_email
            worker.user.first_name = worker.first_name = request.POST['first_name']
            worker.user.last_name = worker.last_name = request.POST['last_name']
            worker.date_of_birth = datetime.strptime(request.POST['date_of_birth'], '%d.%m.%Y').date()
            if 'avatar' in request.FILES:
                worker.avatar = request.FILES['avatar']
            worker.save()
            worker.user.save()
            worker_html = loader.render_to_string(
                'Tracker/content.html',
                {'new_worker': worker}
            )
            return JsonResponse({"success":True, "worker_html": worker_html, "worker": worker.id}, status=200)
        else:
            print(worker_form.errors)
            return JsonResponse({"success":False, "message":"You did not fill all the fields!"}, status=200)
    return JsonResponse({"success":False}, status=400)

def block_worker(request):

    if request.method == "POST" and request.is_ajax:
        worker_key = request.POST['worker']
        worker = get_object_or_404(Worker, id=worker_key)
        if worker.user.is_superuser:
            return JsonResponse({"success":False}, status=200)
        if request.POST['status'] == "block":
            worker.block()
        elif request.POST['status'] == "unblock":
            worker.unblock()
        return JsonResponse({"success":True}, status=200)
    return JsonResponse({"success":False}, status=400)

# def change_avatar(request):
#
#     if request.method == "POST" and request.is_ajax:
#         file_form = FileUploadForm(request.POST, request.FILES)
#         if file_form.is_valid():
#             worker_key = request.POST['worker']
#             worker = get_object_or_404(Worker, id=worker_key)
#             avatar = request.FILES['avatar']
#             worker.avatar = avatar
#             worker.save()
#             return JsonResponse({"avatar": worker.avatar.url}, status=200)
#     return JsonResponse({"success":False}, status=400)

def remove_worker(request):

    if request.method == "POST" and request.is_ajax:
        worker_key = request.POST['worker']
        worker = get_object_or_404(Worker, id=worker_key)
        user = get_object_or_404(User, username=worker.user.username)
        user.delete()
        return JsonResponse({"success":False}, status=200)
    return JsonResponse({"success":False}, status=400)

#project views block
def add_project(request):

    if request.method == "GET" and request.is_ajax:
        project_form = ProjectForm()
        csrf_token_value = request.COOKIES['csrftoken']
        form_html = loader.render_to_string(
            'Tracker/forms.html',
            {'new_project_form': project_form, "csrf_token_value": csrf_token_value}
        )
        return JsonResponse({"form_html": form_html}, status=200)

    if request.method == "POST" and request.is_ajax:
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            new_project = request.POST['project_name']
            if Project.objects.filter(project_name__iexact=new_project).exists():
                return JsonResponse({"success":False, "message":"Project with this name already exists!"}, status=200)
            project = project_form.save()
            worker_list = request.POST.getlist('workers')
            project.workers.remove(*project.workers.all())
            for people in worker_list:
                project.workers.add(people)
            project.save()
            project_html = loader.render_to_string(
                'Tracker/content.html',
                {'new_solo_project': project}
            )
            return JsonResponse({"success":True, "project_html": project_html}, status=200)
        else:
            return JsonResponse({"success":False, "message":"You did not fill all the fields!"}, status=200)
    return JsonResponse({"success":False}, status=400)

def project_detail(request):

    if request.method == "GET" and request.is_ajax:
        project_key = request.GET['project']
        worker = get_object_or_404(Worker, user=request.user)
        project = get_object_or_404(Project, id=project_key)
        full_task_list = Task.objects.all().filter(project=project)
        for task in full_task_list:
            task.accessibility()
        task_list = Task.objects.all().filter(project=project)
        project_html = loader.render_to_string(
                'Tracker/project.html',
                {'project': project, 'worker': worker, 'task_list': task_list, 'user': request.user}
            )
        return JsonResponse({"project_html": project_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def change_project(request):

    if request.method == "GET" and request.is_ajax:
        project_key = request.GET['project']
        project = get_object_or_404(Project, id=project_key)
        selected_project = project.id
        project_form = ProjectForm(instance=project)
        csrf_token_value = request.COOKIES['csrftoken']
        form_html = loader.render_to_string(
            'Tracker/forms.html',
            {'edit_project_form': project_form, "csrf_token_value": csrf_token_value, 'selected_project': selected_project}
        )
        return JsonResponse({"form_html": form_html}, status=200)

    if request.method == "POST" and request.is_ajax:
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            new_project = request.POST['project_name']
            selected_project = request.POST['selected_project']
            project = get_object_or_404(Project, id=selected_project)
            if Project.objects.filter(project_name__iexact=new_project).exclude(project_name=project.project_name).exists():
                return JsonResponse({"success":False, "message":"Project with this name already exists!"}, status=200)
            project.project_name = new_project
            project.summary = request.POST['summary']
            worker_list = request.POST.getlist('workers')
            project.workers.remove(*project.workers.all())
            for people in worker_list:
                project.workers.add(people)
            project.save()
            return JsonResponse({"success":True, "project": project.id, 'project_name': project.project_name, 'project_summary': project.summary}, status=200)
        else:
            return JsonResponse({"success":False, "message":"You did not fill all the fields!"}, status=200)
    return JsonResponse({"success":False}, status=400)

def complet_project(request):

    if request.method == "POST" and request.is_ajax:
        project_key = request.POST['project']
        project = get_object_or_404(Project, id=project_key)
        project.complete()
        project_block = loader.render_to_string(
            'Tracker/content.html',
            {'closed_solo_project': project, 'user': request.user}
        )
        return JsonResponse({"project_block": project_block}, status=200)
    return JsonResponse({"success":False}, status=400)

def open_project(request):

    if request.method == "POST" and request.is_ajax:
        project_key = request.POST['project']
        project = get_object_or_404(Project, id=project_key)
        worker = get_object_or_404(Worker, user=request.user)
        project.open()
        project_block = loader.render_to_string(
            'Tracker/content.html',
            {'new_solo_project': project, 'user': request.user}
        )
        return JsonResponse({"project_block": project_block}, status=200)
    return JsonResponse({"success":False}, status=400)

def remove_project(request):

    if request.method == "POST" and request.is_ajax:
        project_key = request.POST['project']
        project = get_object_or_404(Project, id=project_key)
        project.delete()
        return JsonResponse({"success":False}, status=200)
    return JsonResponse({"success":False}, status=400)

#task views block
def add_task(request):

    if request.method == "GET" and request.is_ajax:
        project_key = request.GET['project']
        project = get_object_or_404(Project, id=project_key)
        selected_task = project.id
        task_form = TaskForm()
        csrf_token_value = request.COOKIES['csrftoken']
        form_html = loader.render_to_string(
            'Tracker/forms.html',
            {'new_task_form': task_form, "csrf_token_value": csrf_token_value, 'selected_task': selected_task}
        )
        return JsonResponse({"form_html": form_html}, status=200)

    if request.method == "POST" and request.is_ajax:
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            project_key = request.POST['project']
            project = get_object_or_404(Project, id=project_key)
            new_task = request.POST['title']
            if Task.objects.filter(title__iexact=new_task, project=project).exists():
                return JsonResponse({"success":False, "message":"Task with this name already exists!"}, status=200)
            task = task_form.save()
            task.project = project
            task.accessibility()
            worker = get_object_or_404(Worker, user=request.user)
            task_html = loader.render_to_string(
                'Tracker/content.html',
                {'new_task': task}
            )
            return JsonResponse({"success":True, "task_html": task_html}, status=200)
        else:
            return JsonResponse({"success":False, "message":"You did not fill all the fields!"}, status=200)
    return JsonResponse({"success":False}, status=400)

def save_task(request):

    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        worker_key = request.POST['worker']
        task = get_object_or_404(Task, id=task_key)
        if task.description != request.POST['description']:
            worker = get_object_or_404(Worker, id=worker_key)
            author = get_object_or_404(Worker, user=task.author)
            worker_name = worker.full_name()
            message_title = "Worker: " + worker_name + " changed task: " + task.title
            message_context = "<h5 class='success-color p-1 text-center'>Old description</h5>" + task.description + "<h5 class='success-color p-1 text-center'>New description</h5>" + request.POST['description']
            message_to_worker = Message.objects.create(receiver=worker, title=message_title, message=message_context)
            message_to_author = Message.objects.create(receiver=author, title=message_title, message=message_context)
            task.description = request.POST['description']
            task.save()
            timelog = TimeLog.objects.create(task=task, worker=worker, action="change task description", comment=None)
        return JsonResponse({"success":True}, status=200)
    return JsonResponse({"success":False}, status=400)

def change_task(request):

    if request.method == "GET" and request.is_ajax:
        task_key = request.GET['task']
        task = get_object_or_404(Task, id=task_key)
        selected_task = task.id
        task_form = TaskForm(instance=task)
        csrf_token_value = request.COOKIES['csrftoken']
        form_html = loader.render_to_string(
            'Tracker/forms.html',
            {'edit_task_form': task_form, "csrf_token_value": csrf_token_value, 'selected_task': selected_task}
        )
        return JsonResponse({"form_html": form_html}, status=200)

    if request.method == "POST" and request.is_ajax:
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            new_task = request.POST['title']
            selected_task = request.POST['selected_task']
            task = get_object_or_404(Task, id=selected_task)
            worker = get_object_or_404(Worker, user=request.user)
            if Task.objects.filter(title__iexact=new_task, project=task.project).exclude(title=task.title).exists():
                return JsonResponse({"success":False, "message":"Task with this name already exists!"}, status=200)
            task.title = new_task
            task.description = request.POST['description']
            task.priority_of_task = request.POST['priority_of_task']
            task.type_of_task = request.POST['type_of_task']
            task.available_from = datetime.strptime(request.POST['available_from'], '%d.%m.%Y').date()
            task.available_to = datetime.strptime(request.POST['available_to'], '%d.%m.%Y').date()
            task.estimated_time = request.POST['estimated_time']
            task.accessibility()
            task_html = loader.render_to_string(
                'Tracker/content.html',
                {'new_task': task, 'worker': worker}
            )
            return JsonResponse({"success":True, "task_html": task_html, "task": task.id}, status=200)
        else:
            return JsonResponse({"success":False, "message":"You did not fill all the fields!"}, status=200)
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
        timelog = TimeLog.objects.create(task=task, worker=worker, action="start working", comment=None)
        return JsonResponse({"worker": worker.full_name()}, status=200)
    return JsonResponse({"success":False}, status=400)

def end_task(request):

    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        worker_key = request.POST['worker']
        task = get_object_or_404(Task, id=task_key)
        worker = get_object_or_404(Worker, id=worker_key)
        task.end()
        old_timelog = TimeLog.objects.filter(task=task, worker=worker, action="start working")[0]
        timelog = TimeLog.objects.create(task=task, worker=worker, action="finish working", comment=None)
        spend_time = time.strftime("%H:%M:%S", time.gmtime((timelog.time_of_start - old_timelog.time_of_start).total_seconds()))
        timelog.spend_time = spend_time
        timelog.save()
        return JsonResponse({"success":True}, status=200)
    return JsonResponse({"success":False}, status=400)

def completed_task(request):

    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)
        task.complete()
        task_html = loader.render_to_string(
            'Tracker/content.html',
            {'completed_task': task}
        )
        return JsonResponse({"task_html": task_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def open_task(request):

    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)
        task.open()
        task.accessibility()
        task_html = loader.render_to_string(
            'Tracker/content.html',
            {'new_task': task}
        )
        return JsonResponse({"task_html": task_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def remove_task(request):

    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)
        task.delete()
        return JsonResponse({"success":False}, status=200)
    return JsonResponse({"success":False}, status=400)

#comment views block
def add_comment(request):

    if request.method == 'POST' and request.is_ajax:
        post_comment = request.POST['comment']
        worker_key = request.POST['worker']
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)
        worker = get_object_or_404(Worker, id=worker_key)
        author = worker.full_name()
        new_comment = Comment.objects.create(task=task, comments=post_comment, author=author)
        timelog = TimeLog.objects.create(task=task, worker=worker, action="add comment", comment=post_comment)
        comments = Comment.objects.filter(task=task)[:15]
        comments_html = loader.render_to_string(
            'Tracker/content.html',
            {'comments': comments}
        )
        return JsonResponse({"comments_html": comments_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def show_comments(request):

    if request.method == "GET" and request.is_ajax:
        task_key = request.GET['task']
        task = get_object_or_404(Task, id=task_key)
        comments = Comment.objects.filter(task=task)[:15]
        if comments:
            comments_html = loader.render_to_string(
                'Tracker/content.html',
                {'comments': comments}
            )
            return JsonResponse({"success":True, "comments_html": comments_html}, status=200)
        else:
            return JsonResponse({"success":False}, status=200)
    return JsonResponse({"success":False}, status=400)

#time logs views block
def get_time_logs(request):

    if request.method == "GET" and request.is_ajax:
        task_key = request.GET['task']
        task = get_object_or_404(Task, id=task_key)
        timelogs = TimeLog.objects.filter(task=task)[:15]
        small = True
        if timelogs:
            timelogs_html = loader.render_to_string(
                'Tracker/content.html',
                {'timelogs': timelogs, "small": small}
            )
            return JsonResponse({"success":True, "timelogs_html": timelogs_html}, status=200)
        else:
            return JsonResponse({"success":False}, status=200)
    return JsonResponse({"success":False}, status=400)

def show_time_logs(request):

    if request.method == "GET" and request.is_ajax:
        if 'worker' in request.GET:
            worker_key = request.GET['worker']
            timelogs = TimeLog.objects.filter(worker=worker_key)[:15]
        else:
            timelogs = TimeLog.objects.all()[:15]
        if timelogs:
            small = False
            timelogs_html = loader.render_to_string(
                'Tracker/content.html',
                {'timelogs': timelogs, "small": small, 'user': request.user}
            )
            return JsonResponse({"success":True, "timelogs_html": timelogs_html}, status=200)
        else:
            return JsonResponse({"success":False}, status=200)
    return JsonResponse({"success":False}, status=400)

def remove_time_log(request):

    if request.method == "POST" and request.is_ajax:
        log_key = request.POST['timelog']
        timelog = get_object_or_404(TimeLog, id=log_key)
        timelog.delete()
        return JsonResponse({"success":True}, status=200)
    return JsonResponse({"success":False}, status=400)

#message views block
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

def get_messages(request):

    if request.method == "GET" and request.is_ajax:
        worker_key = request.GET['worker']
        worker = get_object_or_404(Worker, id=worker_key)
        messages = Message.objects.filter(receiver=worker)
        if messages:
            messages_html = loader.render_to_string(
                'Tracker/content.html',
                {'message_list': messages}
            )
            return JsonResponse({"success":True, "messages_html": messages_html}, status=200)
        else:
            return JsonResponse({"success":False}, status=200)
    return JsonResponse({"success":False}, status=400)

def remove_message(request):

    if request.method == "POST" and request.is_ajax:
        worker_key = request.POST['worker']
        message_key = request.POST['message']
        worker = get_object_or_404(Worker, id=worker_key)
        message = get_object_or_404(Message, id=message_key)
        message.delete()
        return JsonResponse({"success":True}, status=200)
    return JsonResponse({"success":False}, status=400)
