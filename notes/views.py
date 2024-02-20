from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import Note, NoteUpdate
from .serializers import NoteSerializer, UserSerializer, NoteUpdateSerializer
from django.contrib.auth import authenticate


@api_view(['POST'])
def user_signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(username=serializer.validated_data['username'],
                                             email=serializer.validated_data.get('email', ''),
                                             password=serializer.validated_data['password'])
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'access_token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'access_token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def note_create(request):
    if request.method == 'POST':
        current_user = request.user
        request.data['author'] = current_user.id
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def share_note(request):
    try:
        note_id = request.data.get('note_id')
        note = Note.objects.get(pk=note_id)
        if note.author != request.user:
            return Response({'message': 'You do not have permission to share this note.'}, status=status.HTTP_403_FORBIDDEN)
        
        user_ids = request.data.get('user_ids', [])
        users = User.objects.filter(pk__in=user_ids)
        for user in users:
            note.shared_users.add(user)

        return Response({'message': 'Note shared successfully.'}, status=status.HTTP_200_OK)
    
    except Note.DoesNotExist:
        return Response({'message': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_note_by_id(request, note_id):
    try:
        note = Note.objects.get(pk=note_id)
        
        if request.user == note.author or request.user in note.shared_users.all():
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You do not have permission to view this note.'}, status=status.HTTP_403_FORBIDDEN)
    
    except Note.DoesNotExist:
        return Response({'message': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_note_by_id(request, note_id):
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return Response({'message': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != note.author and request.user not in note.shared_users.all():
        return Response({'message': 'You do not have permission to update this note'}, status=status.HTTP_403_FORBIDDEN)
    
    updated_content = request.data.get('content')
    
    if updated_content:
        old_sentences = note.content.split(".")
        new_sentences = updated_content.split(".")

        line_position = 1
        for sentence in new_sentences:
            if sentence not in old_sentences:
                NoteUpdate.objects.create(
                    note=note,
                    line_position=line_position,
                    updated_sentence=sentence,
                    updated_by=request.user
            )
            line_position += 1
        
        note.content = updated_content
        note.save()
            
        return Response({'message': 'Note updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_note_version_history(request, id):
    try:
        note = Note.objects.get(pk=id)
        
        if request.user != note.author and request.user not in note.shared_users.all():
            return Response({'message': 'You do not have permission to view this note version history'}, status=status.HTTP_403_FORBIDDEN)
        
        updates = NoteUpdate.objects.filter(note_id=id)
        serializer = NoteUpdateSerializer(updates, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except NoteUpdate.DoesNotExist:
        return Response({'message': 'Note version history not found'}, status=status.HTTP_404_NOT_FOUND)


