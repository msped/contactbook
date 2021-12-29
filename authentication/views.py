from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

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
    