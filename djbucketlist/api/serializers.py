from rest_framework import serializers
from .models import Bucketlist

class BucketlistSerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Bucketlist
        fields = '__all__'
        read_only_fields = ('date_created','date_modified')
