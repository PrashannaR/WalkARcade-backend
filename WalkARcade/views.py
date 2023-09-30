from django.http import JsonResponse
from .models import UserPoints
from .serializers import UserPointsSerilizers
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status


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
