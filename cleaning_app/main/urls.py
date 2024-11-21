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
from django.urls import path
from .views import *
#from .views import upload_image
from . import views
from . import views


app_name = 'main'

urlpatterns = [
    path("", homepage, name="homepage"),
    path('api/verify_firebase_token/', VerifyFirebaseToken.as_view(), name='verify-firebase-token'),
    path("create-user/", CreateUserFromFirebase.as_view(), name='create-user'),
    path("users/", UserList.as_view(), name='user-list'),
    path("users/<int:pk>/", UserDetails.as_view(), name='user-details'),
    path("customers/", CustomerList.as_view(), name='customer-list'),
    path("customers/<int:pk>/", CustomerDetails.as_view(), name='customer-details'),
    path("specialties/", SpecialtyList.as_view(), name='specialty-list'),
    path("specialties/<int:pk>/", SpecialtyDetails.as_view(), name='specialty-details'),
    path("service-providers/", Service_ProviderList.as_view(), name='service-provider-list'),
    path("service-providers/<int:pk>/", Service_ProviderDetails.as_view(), name='service-provider-details'),
    path("service-providers/<int:pk>/job-history", JobHistoryList.as_view(), name='service-provider-job-history'),
    path("nearby-providers/<int:home_id>/", NearbyProvidersView.as_view(), name="nearby-providers"),
    path("homes/", HomeList.as_view(), name="home-list"),
    path("homes/<int:pk>/", HomeDetails.as_view(), name="home-details"),
    path("homes/<int:pk>/job-history", HomeHistoryList.as_view(), name='home-job-history'),
    path("rooms/", RoomList.as_view(), name='room-list'),
    path("rooms/<int:pk>/", RoomDetails.as_view(), name='room-details'),
    path("jobs/", JobList.as_view(), name="job-list"),
    path("jobs/<int:pk>/", JobDetails.as_view(), name="job-details"),
    path("availabilities/", AvailabilityList.as_view(), name="availability-list"),
    path("availabilities/<int:pk>/", AvailabilityDetails.as_view(), name="availability-details"),
    path("payments/", PaymentList.as_view(), name="payment-list"),
    path("payments/<int:pk>/", PaymentDetails.as_view(), name="payment-details"),
    path("services/", ServiceList.as_view(), name="service-list"),
    path("services/<int:pk>/", ServiceDetails.as_view(), name="service-details"),
    path("tasks/", TaskList.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetails.as_view(), name="task-details"),
    path("reviews/", ReviewList.as_view(), name="review-list"),
    path("reviews/<int:pk>/", ReviewDetails.as_view(), name="review-details"),
    path("payment-methods/", Payment_MethodList.as_view(), name="payment-method-list"),
    path("payment-methods/<int:pk>/", Payment_MethodDetails.as_view(), name="payment-method-details"),
    path("bank-accounts/", Bank_AccountList.as_view(), name="bank-account-list"),
    path("bank-accounts/<int:pk>/", Bank_AccountDetails.as_view(), name="bank-account-details"),
    path('upload/', views.upload_image, name='upload_image'),
]

