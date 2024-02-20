from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_notes')
    shared_users = models.ManyToManyField(User, related_name='shared_notes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NoteUpdate(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    line_position = models.IntegerField()
    updated_sentence = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

