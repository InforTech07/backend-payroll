# media serailizers
# utils
from rest_framework import serializers
from apps.media.models import PayrollImage, PayrollFile

# Create your serializers here.


class PayrollImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollImage
        fields = '__all__'

class PayrollFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollFile
        fields = '__all__'