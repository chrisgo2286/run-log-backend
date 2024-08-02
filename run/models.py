from django.db import models
from django.contrib.auth.models import User

# Create your models here.

RUN_CHOICES = (
    ('Easy Run', 'Easy Run'),
    ('Long Run', 'Long Run'),
    ('Intervals', 'Intervals'),
    ('Tempo Run', 'Tempo Run')
)

class Run(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    run_type = models.CharField(
        blank=False, 
        null=False, 
        max_length=20, 
        choices=RUN_CHOICES, 
        default='Easy Run'
    )
    distance = models.DecimalField(
        blank=False, 
        null=False, 
        max_digits=10, 
        decimal_places=2
    )
    time = models.DecimalField(
        blank=False, 
        null=False,
        max_digits=10,
        decimal_places=2
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.owner.username} - {self.date:%m-%d-%Y} - {self.distance}KM'