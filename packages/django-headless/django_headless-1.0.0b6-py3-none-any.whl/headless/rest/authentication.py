from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

from headless.settings import headless_settings


class SecretKeyAuthentication(BaseAuthentication):
    """
    An authentication class that uses a secret key for authentication.
    """

    def authenticate(self, request):
        secret_key_header = request.headers.get(
            headless_settings.AUTH_SECRET_KEY_HEADER, None
        )

        if not secret_key_header:
            return None  # No secret key provided, allow other authentication methods to try

        # Get your configured secret key.
        # It's crucial to store this securely, e.g., in environment variables.
        configured_secret_key = headless_settings.AUTH_SECRET_KEY

        if not configured_secret_key:
            raise AuthenticationFailed("HEADLESS.AUTH_SECRET_KEY is not configured.")

        if secret_key_header == configured_secret_key:
            # Since it's not user-based, we just return a dummy user.
            return User(), None
        else:
            raise AuthenticationFailed("Invalid secret key.")

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the WWW-Authenticate header in a 401 response.
        """
        return f'{headless_settings.AUTH_SECRET_KEY_HEADER} realm="API"'
