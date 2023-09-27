import datetime

from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status


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
                login(request, user)
                response = Response({'message': 'Успешный вход!'}, status=status.HTTP_200_OK)
                return response
            
        return Response({'message': 'Неверный логин или пароль!'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        username = request.user.username if type(request.user) != AnonymousUser else None
        return Response({'username': username}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def get(self, request):
        # Удаление токена из кук
        response = Response({'message': 'Вы вышли из системы!'}, status=status.HTTP_200_OK)
        logout(request)
        return response
