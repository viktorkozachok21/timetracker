from django import forms
from .models import Project, Task, Worker
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

    username = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(min_length=8, max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class WorkerForm(forms.ModelForm):

    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(format=('%d.%m.%Y'), attrs={'class' : 'picker date', 'placeholder': 'Choice your birth date'}))

    class Meta:
        model = Worker
        fields = ['last_name', 'first_name', 'date_of_birth', 'post', 'avatar']
        widgets = {
            'post': forms.Select(choices=Worker.POSTS,attrs={'class': 'form-control'})
        }

class ProjectForm(forms.ModelForm):

    project_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Project name', 'validate': ''}))
    summary = forms.CharField(widget=forms.Textarea(attrs={'class': 'mceEditor'}))

    class Meta:
        model = Project
        fields = ['project_name', 'summary', 'workers']
