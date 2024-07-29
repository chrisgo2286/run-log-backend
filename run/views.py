from django.shortcuts import render
from rest_framework import viewsets
from .serializers import RunSerializer
from .models import Run
from .misc.run_data import RunData
from .misc.monthly_stats import MonthlyStats
from .misc.yearly_stats import YearlyStats
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
# Create your views here.

class RunView(viewsets.ModelViewSet):
    serializer_class = RunSerializer
    queryset = Run.objects.all()
    
    def perform_create(self, serializer):    
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

@api_view(('GET',))
def calendar_view(request):
    runs = Run.objects.filter(owner=request.user)
    month = int(request.query_params['month'])
    year = int(request.query_params['year'])
    data = RunData(runs, month, year)
    data.compile()
    return Response(data.data)

@api_view(('GET',))
def monthly_stats_view(request):
    runs = Run.objects.filter(owner=request.user)
    month = int(request.query_params['month'])
    year = int(request.query_params['year'])
    monthly_stats = MonthlyStats(month, year, runs)
    monthly_stats.compile()
    return Response(monthly_stats.data)

@api_view(('GET',))
def yearly_stats_view(request):
    runs = Run.objects.filter(owner=request.user)
    year = int(request.query_params['year'])
    yearly_stats = YearlyStats(year, runs)
    yearly_stats.compile()
    return Response(yearly_stats.data)