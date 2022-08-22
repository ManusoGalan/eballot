"""ballot_mgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from rest_framework import routers
from api import views

from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'ballot', views.BallotBoxView, basename='ballot')
router.register(r'candidates/(?P<bk>\d+)', views.CandidateView, basename='candidates')
router.register(r'contract', views.ContractView, basename='contract')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)