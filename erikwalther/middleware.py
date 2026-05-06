# erikwalther/middleware.py

class TrustProxyMiddleware:
    """
    Force REMOTE_ADDR to be the value from X-Forwarded-For if present.
    This ensures that tools like django-axes see the real client IP.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded_for:
            # X-Forwarded-For kan meerdere IPs bevatten: client, proxy1, proxy2
            # We nemen de eerste (de echte client)
            request.META['REMOTE_ADDR'] = forwarded_for.split(',')[0].strip()
        
        # Ook X-Real-IP ondersteunen als fallback
        if not forwarded_for:
            real_ip = request.META.get('HTTP_X_REAL_IP')
            if real_ip:
                request.META['REMOTE_ADDR'] = real_ip.strip()

        return self.get_response(request)
