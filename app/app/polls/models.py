from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Poll(models.Model):
    name = models.TextField()
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return self.name

class PollAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if hasattr(obj, 'date_start') and obj.date_start:
            return ['date_start']
        return []

admin.site.register(Poll, PollAdmin)

class Question(models.Model):
    question_text = models.TextField()
    question_type = models.CharField(max_length=4, choices=[
        ('text', 'text'),
        ('solo', 'solo'),
        ('mult', 'multiple')
    ])
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.poll}] q_id:{self.id} {self.question_text} [{self.question_type}]"

    class Meta:
        ordering = ["poll", "id"]

admin.site.register(Question)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ["user", "question__poll", "question"]

    def __str__(self):
        return f"[{self.user}] {self.question}: {self.answer}"

admin.site.register(Answer)

