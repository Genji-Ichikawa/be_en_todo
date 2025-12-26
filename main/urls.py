from django.urls import path

from main import views

urlpatterns = [
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("home", views.CategoryListView.as_view(), name="home"),
    path("category/<int:category_id>", views.TodoListView.as_view(), name="todo_list"),
    path(
        "category/<int:category_id>/todo/create",
        views.TodoCreateView.as_view(),
        name="todo_create",
    ),
    path(
        "category/<int:category_id>/todo/<int:todo_id>",
        views.TodoDetailView.as_view(),
        name="todo_detail",
    ),
    path(
        "category/<int:category_id>/todo/<int:todo_id>/update",
        views.TodoUpdateView.as_view(),
        name="todo_update",
    ),
    path(
        "category/<int:category_id>/todo/<int:todo_id>/delete",
        views.TodoDeleteView.as_view(),
        name="todo_delete",
    ),
    path("calendar", views.CalendarView.as_view(), name="calendar"),
    path("mypage", views.MypageView.as_view(), name="mypage"),
]
