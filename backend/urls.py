"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from run import views

router = routers.DefaultRouter()
router.register(r'runs', views.RunView, 'run')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/calendar/', views.calendar_view),
    path('api/monthly_stats/', views.monthly_stats_view),
    path('api/yearly_stats/', views.yearly_stats_view),
    path('api/monthly_chart/', views.monthly_chart_view),
    path('api/weekly_chart/', views.weekly_chart_view),
    path('api/run_type_chart/', views.run_type_chart_view),
    path('api/', include('dj_rest_auth.urls')),
    path('api/registration/', include('dj_rest_auth.registration.urls'))
]
