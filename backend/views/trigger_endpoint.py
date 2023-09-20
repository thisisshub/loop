from backend import serializer
from loop.tasks import generate_report
from rest_framework.views import APIView
from rest_framework.response import Response


class TriggerReport(APIView):

    def post(self):
        
        # Trigger Report log
        report_serializer = serializer.ReportLogSerializer(data={})
        report_serializer.is_valid(raise_exception=True)
        report_serializer.save()
        
        # Call celery task
        generate_report.delay(report_id=report_serializer.data.get('id'))

        # Create a DataFrame to store the results.
        return Response({"report_id": f"{report_serializer.data.get('id')}"})