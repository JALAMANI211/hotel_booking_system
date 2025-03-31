from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', validated_data['email']),
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile
        fields = ('id', 'email', 'address', 'photo', 'gender')

class UserBookingStatsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='user.id')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    booking_count = serializers.IntegerField()