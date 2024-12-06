from rest_framework import serializers
from .models import Run, TrainingBlock

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = (
            'id', 
            'owner', 
            'run_type', 
            'date', 
            'distance', 
            'hours', 
            'minutes', 
            'seconds', 
            'comment'
        )

class TrainingBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingBlock
        fields = (
            'id', 
            'owner', 
            'athlete',
            'title',
            'startDate',
            'endDate',
            'cycleLength',
            'goals'
        )