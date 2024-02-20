from rest_framework import serializers
from .models import Note, NoteUpdate
from django.contrib.auth.models import User

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'  # Include all fields of the Note model

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class NoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteUpdate
        fields = ['timestamp', 'updated_by', 'updated_sentence', 'line_position']
        