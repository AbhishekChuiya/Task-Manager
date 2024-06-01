from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, Task

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text="Required")
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'is_completed']