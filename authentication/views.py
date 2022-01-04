from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsOwner
from .serializers import RegisterSerializer

# Create your views here.

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class DeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = User.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "user_id"

class BlacklistTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
