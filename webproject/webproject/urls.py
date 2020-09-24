"""webproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from mainapp import views as mainviews
from downloadapp import views as downloadviews
from visitapp import views as visitviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainviews.index, name='index'),
    path('generic', mainviews.generic, name='generic'),
    path('elements', mainviews.elements, name='elements'),
    path('download', downloadviews.download, name='download'),
    path('visit', visitviews.visit, name='visit'),
]
