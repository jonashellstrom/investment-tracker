from rest_framework.permissions import IsAuthenticated


class AuthMixin:
    permission_classes = (IsAuthenticated,)
