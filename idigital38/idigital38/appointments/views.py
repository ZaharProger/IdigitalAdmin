from wsgiref.util import FileWrapper

import openpyxl
from django.http import HttpResponse
from openpyxl.styles import Font
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AppointmentForm
from .models import Appointment


class AppointmentView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        workbook = openpyxl.Workbook()

        workbook.create_sheet('Заявки')
        appointments_sheet = workbook['Заявки']

        appointments_sheet['A1'] = '№'
        appointments_sheet['B1'] = 'ФИО'
        appointments_sheet['C1'] = 'Контакты'
        appointments_sheet['D1'] = 'Организация'

        header_font = Font(color='00000000', bold=True)
        for cell in appointments_sheet['1:1']:
            cell.font = header_font

        appointments = Appointment.objects.all().values_list('name', 'contacts', 'organization', named=True)
        for i in range(len(appointments)):
            row_number = i + 2
            appointments_sheet.cell(row=row_number, column=1).value = i + 1
            appointments_sheet.cell(row=row_number, column=2).value = appointments[i][0]
            appointments_sheet.cell(row=row_number, column=3).value = appointments[i][1]
            appointments_sheet.cell(row=row_number, column=4).value = appointments[i][2]

        workbook.remove(workbook['Sheet'])
        workbook.save('export-data/Idigital38_Reports.xlsx')
        file = open('export-data/Idigital38_Reports.xlsx', 'rb')

        return HttpResponse(
            {'message': '', 'file': FileWrapper(file), 'name': 'Idigital38_Заявки.xlsx'},
            status=status.HTTP_200_OK,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

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
