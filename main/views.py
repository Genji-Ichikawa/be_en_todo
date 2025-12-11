from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from main.forms import LoginForm, SignUpForm
from main.models import Category, Todo, User


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "main/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LoginView(LoginView):
    authentication_form = LoginForm
    template_name = "main/login.html"


class LogoutView(LogoutView):
    pass


class CategoryList(ListView):
    template_name = "main/home.html"
    model = Category
    context_object_name = "category_list"

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user).order_by("name")
        return queryset
