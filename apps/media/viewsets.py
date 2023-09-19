# media viewsets
# utils
from rest_framework import viewsets
from apps.media.models import PayrollFile, PayrollImage
from apps.media.serializers import PayrollFileSerializer, PayrollImageSerializer

# Create your viewsets here.


class PayrollImageViewSet(viewsets.ModelViewSet):
    queryset = PayrollImage.objects.all()
    serializer_class = PayrollImageSerializer

class PayrollFileViewSet(viewsets.ModelViewSet):
    queryset = PayrollFile.objects.all()
    serializer_class = PayrollFileSerializer
