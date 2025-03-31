from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from .models import Booking
from .serializers import BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['check_in_datetime', 'created_at']
    
    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Booking.objects.filter(user_id=user_id)

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(check_in_datetime__date__range=[start_date, end_date])
            except ValueError:
                pass
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if (start_date and not end_date) or (end_date and not start_date):
            return Response(
                {"error": "Both start_date and end_date must be provided for date filtering"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().list(request, *args, **kwargs)
