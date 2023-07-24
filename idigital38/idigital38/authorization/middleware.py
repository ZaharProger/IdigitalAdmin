import logging

class AddTokenToHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get('access_token')
        logging.info(f'Token from cookies: {access_token}')  # Добавьте этот вывод
        
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'JWT {access_token}'
            logging.info('Token added to Authorization header.')

        response = self.get_response(request)
        return response
