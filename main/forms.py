from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from main.models import Category, Todo, User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class LoginForm(AuthenticationForm):
    pass


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class TodoCreateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = (
            "title",
            "description",
            "deadline_time",
        )
        widgets = {
            "deadline_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }


class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = (
            "title",
            "description",
            "deadline_time",
            "hour_spent",
            "is_finished",
        )
        widgets = {
            "deadline_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                # format="%Y-%m-%dT%H:%M",
            ),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["deadline_time"].input_formats = ["%Y-%m-%dT%H:%M"]
