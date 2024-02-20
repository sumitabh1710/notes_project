from django.urls import path
from .views import note_create, user_signup, user_login, share_note, get_note_by_id, update_note_by_id, get_note_version_history

urlpatterns = [
    path('signup', user_signup, name='user-signup'),
    path('login', user_login, name='user-login'),
    path('notes/create', note_create, name='note-create'),
    path('notes/share', share_note, name='note-share'),
    path('notes/<int:note_id>', get_note_by_id, name='get_note_by_id'),
    path('notes/<int:note_id>/update', update_note_by_id, name='update_note_by_id'),
    path('notes/version-history/<int:id>', get_note_version_history, name='note-version-history'),
]
