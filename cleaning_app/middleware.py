class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("DEBUG: Request path:", request.path)
        print("DEBUG: Request method:", request.method)
        print("DEBUG: Request headers:", request.headers)
        print("DEBUG: Request META:", request.META)
        return self.get_response(request)