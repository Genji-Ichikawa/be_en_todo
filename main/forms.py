from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from main.models import Category, Todo, User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class LoginForm(AuthenticationForm):
    pass


class TodoCreateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = (
            "title",
            "description",
            "deadline_time",
            "parent_todo",
        )


class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = (
            "title",
            "description",
            "deadline_time",
            "hour_spent",
            "is_finished",
            "parent_todo",
        )
