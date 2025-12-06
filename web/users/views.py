from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import MethodNotAllowed

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")
