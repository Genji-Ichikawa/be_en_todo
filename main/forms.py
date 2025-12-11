from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from main.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class LoginForm(AuthenticationForm):
    pass
