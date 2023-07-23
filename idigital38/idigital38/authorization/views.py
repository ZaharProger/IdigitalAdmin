
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from django.http import HttpResponse

class LoginView(APIView):
    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username:
                return Response({'message': 'Введите логин'}, status=status.HTTP_400_BAD_REQUEST)
            if not password:
                return Response({'message': 'Введите пароль'}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response = HttpResponse('Успешный вход!',status=200)
                # Установка токена в куки с флагом httponly=True
                response.set_cookie(key='access_token', value=access_token, httponly=True)
                response
                # Вернуть HTTP-ответ с кукой в заголовках
                return response
            
        return Response({'message': 'Неверный логин или пароль!'}, status=status.HTTP_401_UNAUTHORIZED)
