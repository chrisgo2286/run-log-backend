from django.shortcuts import render
from rest_framework import viewsets
from .serializers import RunSerializer
from .models import Run
from .misc.run_data import RunData
from .misc.runner_profile import RunnerProfile
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
    user = User.objects.get(id=request.user.id)
    runs = Run.objects.filter(owner=user)
    month = int(request.query_params['month'])
    year = int(request.query_params['year'])
    data = RunData(runs, month, year)
    data.compile()
    return Response(data.data)

@api_view(('GET',))
def profile_view(request):
    user = User.objects.get(id=request.user.id)
    runs = Run.objects.filter(owner=user)
    profile = RunnerProfile(runs)
    profile.compile()
    return Response(profile.data)
