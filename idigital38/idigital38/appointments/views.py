from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AppointmentForm


class AppointmentView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_permissions(self):
        method = self.request.method
        return [] if method == 'GET' else [IsAuthenticated()]

    def post(self, request):
        new_appointment = AppointmentForm(request.data)
        if new_appointment.is_valid():
            new_appointment.save()
            response_status = status.HTTP_200_OK
        else:
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(
            {'message': ''},
            status=response_status,
            content_type='application/json'
        )
