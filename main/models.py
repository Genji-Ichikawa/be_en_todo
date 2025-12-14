from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, Q


class User(AbstractUser):
    pass


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField("カテゴリ名", max_length=50)

    def __str__(self):
        return self.name


class Todo(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="todos"
    )
    title = models.CharField("タイトル", max_length=50)
    description = models.TextField("説明", blank=True, null=True)
    deadline_time = models.DateTimeField("締め切り日時")
    hour_spent = models.IntegerField("所要時間数(h)", default=0)
    is_finished = models.BooleanField("完了済み", default=False)
    parent_todo = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="child_todo",
        blank=True,
        null=True,
    )
    rank = models.IntegerField(
        "階層の深さ",
        default=1,
    )

    def __str__(self):
        return f"{self.title} ({self.category.name})"

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(rank__gte=1) & Q(rank__lte=3),
                name="rank_range_check",
            )
        ]
