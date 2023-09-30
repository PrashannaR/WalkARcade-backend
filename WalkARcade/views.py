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
        

     