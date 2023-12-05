"""WetlandsProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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


#Import this three: Views, settings and static.
from WetlandApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.map.as_view(), name='map'),
    path('MyField',views.MyField.as_view(),name='MyField'),
    path('Acres',views.Acres.as_view(),name='Acres'),
    path('Hectares',views.Hectares.as_view(),name='Hectares'),
    path('Kilometers',views.Kilometers.as_view(),name='Kilometers'),
    path('areameters',views.areameters.as_view(),name='areameters'),
    path('Sentinel_Imagery',views.Sentinel_Imagery.as_view(),name='Sentinel_Imagery'),
    path('Sentinel_Imagery_1',views.Sentinel_Imagery_1.as_view(),name='Sentinel_Imagery_1'),
    path('Landsat8_Imagery',views.Landsat8_Imagery.as_view(),name='Landsat8_Imagery'),
    path('Wetlands',views.Wetlands.as_view(),name='Wetlands'),
    path('NDVI',views.NDVI.as_view(),name='NDVI'),
    path('NDWI',views.NDWI.as_view(),name='NDWI'),
    path('MNDWI',views.MNDWI.as_view(),name='MNDWI'),
    path('JRC_Gloabal_Surface_Water',views.JRC_Gloabal_Surface_Water.as_view(),name="JRC_Gloabal_Surface_Water"),
    path('MyField2',views.MyField2.as_view(),name="MyField2"),
    path('MyField3',views.MyField3.as_view(),name="MyField3"),
    path('LULC',views.LULC.as_view(),name='LULC'),

    

]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)