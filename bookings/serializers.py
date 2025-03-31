from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Booking
        fields = ('id', 'user', 'user_email', 'hotel_name', 'check_in_datetime', 
                  'check_out_datetime', 'num_persons', 'created_at')
        read_only_fields = ('user', 'created_at')
    
    def validate(self, data):
        if data['check_in_datetime'] >= data['check_out_datetime']:
            raise serializers.ValidationError("Check-out must be after check-in")
        return data
        
    def create(self, validated_data):
        # Get the user ID directly and create the booking
        user = self.context['request'].user
        booking = Booking.objects.create(
            user_id=user.id,
            hotel_name=validated_data['hotel_name'],
            check_in_datetime=validated_data['check_in_datetime'],
            check_out_datetime=validated_data['check_out_datetime'],
            num_persons=validated_data['num_persons']
        )
        return booking