from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer, UserBookingStatsSerializer
from bookings.models import Booking
from datetime import datetime

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def booking_stats(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        booking_filter = {}
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                booking_filter['check_in_datetime__date__range'] = [start_date, end_date]
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, 
                                 status=status.HTTP_400_BAD_REQUEST)
        bookings_with_counts = Booking.objects.filter(**booking_filter) \
            .values('user').annotate(booking_count=Count('user'))

        user_ids = [entry['user'] for entry in bookings_with_counts]
        users_with_details = User.objects.filter(id__in=user_ids)

        result = []
        for user in users_with_details:
            booking_count = next((entry['booking_count'] for entry in bookings_with_counts if entry['user'] == user.id), 0)
            result.append({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'booking_count': booking_count
            })

        return Response(result)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Profile.objects.filter(user_id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            profile = Profile.objects.get(user_id=request.user.id)
            for attr, value in serializer.validated_data.items():
                setattr(profile, attr, value)
            profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user_id=request.user.id, **serializer.validated_data)
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def booking_count(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response({"error": "Both start_date and end_date are required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        booking_count = Booking.objects.filter(
            user=request.user,
            check_in_datetime__date__range=[start_date, end_date]
        ).count()
        
        return Response({"booking_count": booking_count})