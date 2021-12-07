from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from .serializer import *


# Create your views here.


class ClientView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        clients = Client.objects.all()
        data = ConnectedData.objects.all()
        serializer = ClientSerializer(clients, many=True)

        return Response(serializer.data)


