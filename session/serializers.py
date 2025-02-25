from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import Session
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'



class SessionSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['formatted_date'] = instance.session_date_posted.strftime("%Y-%m-%d %H:%M:%S")
        return data
    def run_validation(self, data):
        data = super().run_validation(data)
        if data['session_status'] == 'C' and not data.get('admin_user_comment'):
            raise serializers.ValidationError("Admin comment required for completed session.")
        return data

class ReadOnlySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
        read_only_fields = fields

class SessionDetailView(APIView):
    def get(self, request, pk):
        session = Session.objects.get(pk=pk)
        serializer = SessionSerializer(session)
        return Response(serializer.data)
    


class CheapItemSessionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheapItemSessionData
        fields = '__all__'

class ExpensiveItemSessionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensiveItemSessionData
        fields = '__all__'

class CompletedRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedRecord
        fields = '__all__'
