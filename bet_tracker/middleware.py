from django.http import HttpResponsePermanentRedirect


class RedirectNonWwwMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is made to 'betview.net' (non-www) and redirect to 'www.betview.net'
        if request.get_host() == "betview.net":
            # Ensure the request is redirected to the 'www' version with https
            return HttpResponsePermanentRedirect(
                f"https://www.betview.net{request.get_full_path()}"
            )

        # If the domain is already www.betview.net, proceed with normal request handling
        response = self.get_response(request)
        return response
