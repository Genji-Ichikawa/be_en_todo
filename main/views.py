from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from main.forms import LoginForm, SignUpForm, TodoCreateForm, TodoUpdateForm
from main.models import Category, Todo


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


class CategoryListView(ListView):
    template_name = "main/home.html"
    model = Category
    context_object_name = "category_list"

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user).order_by("name")
        return queryset


class TodoListView(ListView):
    template_name = "main/todo_list.html"
    model = Todo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs["category_id"]
        context["category"] = get_object_or_404(
            Category,
            id=category_id,
            user=self.request.user,
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs["category_id"]
        queryset.filter(category__id=category_id)
        return queryset

    # memo
    # todo作成機能はここにつける


class TodoCreateView(CreateView):
    form_class = TodoCreateForm
    model = Todo
    template_name = "main/todo_create.html"

    def get_success_url(self):
        reverse_lazy(
            "todo_list",
            kwargs={"category_id": self.kwargs["category_id"]},
        )


class TodoDetailView(DetailView):
    model = Todo
    template_name = "main/todo.html"


class TodoUpdateView(UpdateView):
    form_class = TodoUpdateForm
    model = Todo
    template_name = "main/todo_update.html"

    def get_success_url(self):
        reverse_lazy(
            "todo_detail",
            kwargs={
                "category_id": self.kwargs["category_id"],
                "todo_id": self.kwargs["todo_id"],
            },
        )
