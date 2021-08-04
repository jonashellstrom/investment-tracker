from django.contrib.auth import get_user_model


class ForceAuthenticationMixin:
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(username="foo", password="bar")
