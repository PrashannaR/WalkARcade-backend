from django.http import JsonResponse
from .models import UserPoints
from .serializers import UserPointsSerilizers
 

def leaderboards(request):
    #users = UserPoints.objects.order_by('-points')
    users = UserPoints.objects.all()
    serializer = UserPointsSerilizers(users, many=True)
    return JsonResponse({"users": serializer.data}, safe=False)

     