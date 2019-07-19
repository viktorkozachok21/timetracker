from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template import loader
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


    file_form = FileUploadForm()
    context['file_form'] = file_form

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
                'Tracker/content.html',
                {'projects_list': projects_list, 'worker': worker, 'page': page, 'user': request.user}
            )

        return JsonResponse({"home_html": home_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def user_login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('user_login'))

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
            print(worker.first_name)
            return JsonResponse({"success":True}, status=200)
        username = request.POST['username']
        if User.objects.filter(username__iexact=username).exists():
            return JsonResponse({"success":False, "message":"User with this username already exists!"}, status=200)
        else:
            return JsonResponse({"success":False, "message":"You did not fill all the fields!"}, status=200)
    return JsonResponse({"success":False}, status=400)

def change_worker(self):

    if request.method == "GET" and request.is_ajax:
        worker_key = request.GET['project']
        project = get_object_or_404(Project, id=project_key)
        project_form = ProjectForm(instance=project)
        form_html = loader.render_to_string(
            'Tracker/forms.html',
            {'change_project_form': project_form}
        )
        return JsonResponse({"form_html": form_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def change_avatar(request):

    if request.method == "POST" and request.is_ajax:
        file_form = FileUploadForm(request.POST, request.FILES)
        if file_form.is_valid():
            worker_key = request.POST['worker']
            worker = get_object_or_404(Worker, id=worker_key)
            avatar = request.FILES['avatar']
            worker.avatar = avatar
            worker.save()
            return JsonResponse({"avatar": worker.avatar.url}, status=200)
    return JsonResponse({"success":False}, status=400)

def remove_worker(request):
    pass

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
            print(project.project_name)
            worker_list = request.POST.getlist('workers')
            project.workers.remove(*project.workers.all())
            for people in worker_list:
                project.workers.add(people)
            project.save()
            project_html = loader.render_to_string(
                'Tracker/content.html',
                {'new_solo_project': project}
            )
            print("end")
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
            print('end')
            project_html = loader.render_to_string(
                'Tracker/content.html',
                {'new_solo_project': project}
            )
            return JsonResponse({"success":True, "project_html": project_html, "project": project.id}, status=200)
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

    if request.method == "POST" and request.is_ajax:
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save()
            project_key = request.POST['project']
            project = get_object_or_404(Project, id=project_key)
            task.project = project
            task.is_active = False
            task.is_completed = False
            task.save()
            task.accessibility()
            task = get_object_or_404(Task, project=project)
            worker = get_object_or_404(Worker, user=request.user)
            task_block = loader.render_to_string(
                'Tracker/content.html',
                {'task': task, 'user': request.user, 'worker': worker}
            )
            return JsonResponse({"task_block": task_block}, status=200)
    return JsonResponse({"success":False}, status=400)

def save_task(request):

    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        worker_key = request.POST['worker']
        new_description = request.POST['description']
        task = get_object_or_404(Task, id=task_key)
        author_key = task.author
        worker = get_object_or_404(Worker, id=worker_key)
        author = get_object_or_404(Worker, user=author_key)
        old_description = task.description
        title = "Changed task description: " + task.project.project_name + " ~ " + task.title
        message_context = "<h3>Worker: " + worker.last_name + " " + worker.first_name + " changed task: " + task.title + "</h3>" + "<h5>Old description:</h5>" + old_description + "<h5>New description:</h5>" + new_description
        message_to_worker = Message.objects.create(receiver=worker, title=title, message=message_context)
        message_to_author = Message.objects.create(receiver=author, title=title, message=message_context)
        task.description = new_description
        task.save()
        timelog = TimeLog.objects.create(task=task, worker=worker, action="change task description", comment=None)
        messages = Message.objects.filter(receiver=worker)
        messages_html = loader.render_to_string(
            'Tracker/content.html',
            {'messages': messages}
        )
        changed_task = {
            'description': task.description,
            'messages_html': messages_html
        }
        return JsonResponse({"task":changed_task}, status=200)
    return JsonResponse({"success":False}, status=400)

def change_task(request):

    pass

def start_task(request):

    if request.method == "POST" and request.is_ajax:
        task_key = request.POST['task']
        worker_key = request.POST['worker']
        task = get_object_or_404(Task, id=task_key)
        worker = get_object_or_404(Worker, id=worker_key)
        task.worker = worker
        task.is_active = True
        task.is_single = False
        task.save()
        timelog = TimeLog.objects.create(task=task, worker=worker, action="start working", comment=None)
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
        task.end()
        task = get_object_or_404(Task, id=task_key)
        old_timelog = TimeLog.objects.filter(task=task, worker=worker, action="start working")[0]
        print(old_timelog.time_of_start)
        timelog = TimeLog.objects.create(task=task, worker=worker, action="finish working", comment=None)
        hour = timelog.time_of_start.hour - old_timelog.time_of_start.hour
        minute = timelog.time_of_start.minute - old_timelog.time_of_start.minute
        second = timelog.time_of_start.second - old_timelog.time_of_start.second
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
        spend_time = str(hours) + ":" + str(minutes) + ":" + str(seconds)
        timelog.spend_time = spend_time
        timelog.save()
        context = {
            'task': task.id
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
        task = get_object_or_404(Task, id=task_key)
        task_block = loader.render_to_string(
            'Tracker/content.html',
            {'task': task, 'user': request.user, 'worker': worker}
        )
        return JsonResponse({"task_block": task_block}, status=200)
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
        author = request.POST['author']
        worker_key = request.POST['worker']
        task_key = request.POST['task']
        task = get_object_or_404(Task, id=task_key)
        worker = get_object_or_404(Worker, id=worker_key)
        new_comment = Comment.objects.create(task=task, comments=post_comment, author=author)
        timelog = TimeLog.objects.create(task=task, worker=worker, action="add comment", comment=post_comment)
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

#time logs views block
def get_time_logs(request):

    if request.method == "GET" and request.is_ajax:
        task_key = request.GET['task']
        task = get_object_or_404(Task, id=task_key)
        timelogs = TimeLog.objects.filter(task=task)
        timelogs_html = loader.render_to_string(
            'Tracker/content.html',
            {'timelogs': timelogs, 'user': request.user}
        )
        return JsonResponse({"timelogs_html": timelogs_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def show_time_logs(request):

    if request.method == "GET" and request.is_ajax:
        if 'worker' in request.GET:
            worker_key = request.GET['worker']
            timelogs = TimeLog.objects.filter(worker=worker_key)
        else:
            timelogs = TimeLog.objects.all()
        timelogs_html = loader.render_to_string(
            'Tracker/content.html',
            {'timelogs': timelogs, 'user': request.user}
        )
        return JsonResponse({"timelogs_html": timelogs_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def remove_time_log(request):

    if request.method == "POST" and request.is_ajax:
        worker_key = request.POST['worker']
        log_key = request.POST['timelog']
        worker = get_object_or_404(Worker, id=worker_key)
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
        messages_html = loader.render_to_string(
            'Tracker/content.html',
            {'message_list': messages}
        )
        return JsonResponse({"messages_html": messages_html}, status=200)
    return JsonResponse({"success":False}, status=400)

def remove_message(request):

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
