from rest_framework.views import APIView
from rest_framework.response import Response

from backend import models
from backend import serializer

class GetReport(APIView):

    def get(self, request):
        report_id = request.query_params.get("report_id", "")
        if report_id != "":
            if not models.ReportGeneration.objects.filter(id=report_id).exists():
                return Response({"status": "Running"})
            else:
                return Response(serializer.ReportFileSerializer(models.ReportGeneration.objects.get(id=report_id)).data)