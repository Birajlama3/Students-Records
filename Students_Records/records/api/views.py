from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from models import Records
from ..serializer import RecordsSerializer

api_view(['GET'])
def get_records(request):
    records = Records.objects.all()
    serializer = RecordsSerializer(records, many=True)
    return Response(serializer.data)