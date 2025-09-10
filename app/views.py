from django.views.generic import RedirectView


class RootView(RedirectView):
    url = '/accounts/'
