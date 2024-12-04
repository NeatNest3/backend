"""
URL configuration for cleaning_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'main'

router = DefaultRouter()

router.register('user', UserList)
router.register('customer', CustomerList)
router.register('specialty', SpecialtyList)
router.register('service_provider', Service_ProviderList)
router.register('home', HomeList)
router.register('room', RoomList)
router.register('job', JobList)
router.register('review', ReviewList)
router.register('task', TaskList)


urlpatterns = [
    path('', include(router.urls)),
    
    path("service-providers/<int:pk>/job-history", JobHistoryList.as_view(), name='service-provider-job-history'),
    path("nearby-providers/<int:home_id>/", NearbyProvidersView.as_view(), name="nearby-providers"),
    path("homes/<int:pk>/job-history", HomeHistoryList.as_view(), name='home-job-history'),
    path('upload/', upload_image, name='upload_image'),
 ]

