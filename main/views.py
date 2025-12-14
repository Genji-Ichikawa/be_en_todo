import calendar
from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_prev_link"] = False
        return context


class LoginView(LoginView):
    authentication_form = LoginForm
    template_name = "main/login.html"


class LogoutView(LogoutView):
    pass


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "main/home.html"
    model = Category
    context_object_name = "category_list"

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user).order_by("name")
        return queryset


class TodoListView(LoginRequiredMixin, ListView):
    template_name = "main/todo_list.html"
    model = Todo
    context_object_name = "todo_list"

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
        queryset = queryset.filter(category=category_id)
        return queryset

    # memo
    # category作成機能はここにつける


class TodoCreateView(LoginRequiredMixin, CreateView):
    form_class = TodoCreateForm
    model = Todo
    template_name = "main/todo_create.html"

    def form_valid(self, form):
        form.instance.category_id = self.kwargs["category_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "todo_list",
            kwargs={"category_id": self.kwargs["category_id"]},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_id"] = self.kwargs["category_id"]
        return context


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = "main/todo_detail.html"
    pk_url_kwarg = "todo_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_id"] = self.kwargs["category_id"]
        return context


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TodoUpdateForm
    model = Todo
    template_name = "main/todo_update.html"
    pk_url_kwarg = "todo_id"

    def get_success_url(self):
        return reverse_lazy(
            "todo_detail",
            kwargs={
                "category_id": self.kwargs["category_id"],
                "todo_id": self.kwargs["todo_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_id"] = self.kwargs["category_id"]
        context["todo_id"] = self.kwargs["todo_id"]
        return context


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    pk_url_kwarg = "todo_id"

    def get_success_url(self):
        return reverse_lazy(
            "todo_list",
            kwargs={"category_id": self.kwargs["category_id"]},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_id"] = self.kwargs["category_id"]
        context["todo_id"] = self.kwargs["todo_id"]
        return context


class CalendarView(TemplateView):
    template_name = "main/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.localdate()
        year = int(self.request.GET.get("year", today.year))
        month = int(self.request.GET.get("month", today.month))
        selected_day = self.request.GET.get("day")

        calendar_weeks = self.get_month_calendar(year, month)
        context["calendar_weeks"] = calendar_weeks
        context["year"] = year
        context["month"] = month
        context["today"] = today

        if month == 1:
            prev_year, prev_month = year - 1, 12
        else:
            prev_year, prev_month = year, month - 1

        if month == 12:
            next_year, next_month = year + 1, 1
        else:
            next_year, next_month = year, month + 1

        context["prev_year"] = prev_year
        context["prev_month"] = prev_month
        context["next_year"] = next_year
        context["next_month"] = next_month

        todos = None
        if selected_day:
            day_date = datetime.strptime(selected_day, "%Y-%m-%d").date()
            todos = Todo.objects.filter(
                deadline_time__date=day_date, category__user=self.request.user
            )
        context["selected_day"] = selected_day
        context["todos"] = todos

        return context

    def get_month_calendar(self, year, month):
        cal = calendar.Calendar(firstweekday=6)  # 日曜始まり
        return cal.monthdatescalendar(year, month)
