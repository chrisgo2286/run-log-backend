from django.shortcuts import render
from rest_framework import viewsets
from .serializers import RunSerializer
from .models import Run
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
# Create your views here.

class RunView(viewsets.ModelViewSet):
    serializer_class = RunSerializer
    queryset = Run.objects.all()
    user = User(id=1)
    
    def perform_create(self, serializer):    
        return serializer.save(owner=self.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.user)

@api_view(('GET',))
def calendar_view(request):
    user = User(id=1)
    runs = Run.objects.filter(owner=user)
    cur_month = int(request.query_params['month'])
    cur_year = int(request.query_params['year'])
    data = RunData(runs, cur_month, cur_year)
    data.compile()
    return Response(data.data)
