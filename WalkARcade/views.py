from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from .models import UserPoints
from .serializers import UserPointsSerilizers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response 
from rest_framework import status

from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


#get all the users
@api_view(['GET', 'POST']) 
def leaderboards(request):
    if request.method == 'GET':
        #users = UserPoints.objects.all()
        users = UserPoints.objects.order_by('-points')
        serializer = UserPointsSerilizers(users, many=True)
        return JsonResponse({"users": serializer.data}, safe=False)
    
    elif request.method == 'POST':
        serializer = UserPointsSerilizers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#get a single user
@api_view(['GET', 'PUT', 'DELETE'])
def getUser(request, username):

    try:
        user = UserPoints.objects.get(username=username)
    except UserPoints.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserPointsSerilizers(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserPointsSerilizers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#register user
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not (username and email and password):
        return Response({'error': 'Please provide username, email, and password.'}, status=status.HTTP_400_BAD_REQUEST)
    
    #check if the username is available
    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
    
    #create user
    user = User.objects.create_user(username = username, email = email, password = password)

    return Response({'success': 'User created successfully.'}, status=status.HTTP_201_CREATED)


from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not (username and password):
        return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)