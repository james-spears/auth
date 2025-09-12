from logging import getLogger
from django.utils.translation import gettext_lazy as _
from django.core.cache import caches
from django.conf import settings
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.core.signing import Signer
from django.utils.crypto import get_random_string
from django.views.generic import RedirectView
from accounts.serializers import UserSerializer
from django.views.generic import RedirectView

signer = Signer(salt=settings.SIGNER_SALT)
log = getLogger(__name__)


class RootView(RedirectView):
    url = '/accounts/'


class AuthView(View):
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return response

        # Check if X-Authorization-Key stored in the sesison cache.
        x_authorization_key = request.session.get(settings.X_AUTHORIZATION_KEY)

        # If there is no X-Authorization-Key stored in the sesison cache,
        if not x_authorization_key:
            # generate a random key,
            x_authorization_key = get_random_string(length=32)
            # and store it in the session.
            request.session[settings.X_AUTHORIZATION_KEY] = x_authorization_key

        try:
            # Attempt to serialize the user data,
            serialized_data = UserSerializer(request.user).data
            # sign it,
            signed_data = signer.sign_object(serialized_data)
            # and store it in the auth cache.
            caches['auth'].set(x_authorization_key, signed_data)
        except BaseException:
            log.error('unable to set user data in auth cache')

        # Finally, set the X-Authorization-Key header
        # on the response to forward downstream.
        response['X-Authorization-Key'] = x_authorization_key
        return response

    def get(self, request) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401, content_type='text/plain')
        return HttpResponse('OK', content_type='text/plain')
