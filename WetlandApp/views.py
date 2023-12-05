from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView 

import matplotlib.pyplot as plt
colormaps=plt.cm.datad.keys()

#Importation of variAous Libraries or packages...
from os import path as op
import geemap
import ee
import folium
import geemap.foliumap as geemap
# import matplotlib.pyplot as plt
from django.http import HttpResponse
from folium import plugins
from folium.plugins import Draw

from .forms import DateForm
from datetime import datetime

# Create your views here.        
#HomeMap
class map(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()   
        Map = geemap.Map()
        Map.add_to(figure)
        Map.set_center(36.4335, -0.1131, 12)
        
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
 

        global basemaps
        basemaps = {
        'Google Maps': folium.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Maps',
                overlay = False,
                control = True
                ),
                'Esri Satellite': folium.TileLayer(
                tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr = 'Esri',
                name = 'Esri Satellite',
                overlay = True,
                control = True
                ),'Google Satellite Hybrid': folium.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Satellite',
                overlay = False,
                control = True
                ), 
                }     
        basemaps['Google Satellite Hybrid'].add_to(Map)
        basemaps['Esri Satellite'].add_to(Map)
             
        Map.add_child(folium.LayerControl())
        figure.render()
        context['map'] = figure
        return context
    
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

#ROI: MyField: Ewaso Nyiro
class MyField(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            boundary = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/ewaso")
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")

            legend_dict = {
                        'ROI Boundary': '000000',
            }
            Map.add_legend(title="Region of Intrest", legend_dict=legend_dict)  
                    
            Total_studyArea = boundary.geometry().area()
            Total_AreaSqKm = ee.Number(Total_studyArea).round()
            print('Estimated Total areas', Total_AreaSqKm.getInfo())
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded Ewaso  Nyiro ROI"
                context['sucess_message'] = sucess_message
            
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['MyField'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

#ROI: MyField2
class MyField2(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            boundary = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/Siaya")
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")
            legend_dict = {
                        'ROI Boundary': '000000',
            }
            Map.add_legend(title="Region of Intrest", legend_dict=legend_dict)  
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded Siaya ROI"
                context['sucess_message'] = sucess_message
                

        Map.add_child(folium.LayerControl())
        figure.render()
        
        context['MyField2'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
#ROI: MyField2
class MyField3(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            boundary = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/Homa_Bay")
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")
            legend_dict = {
                        'ROI Boundary': '000000',
            }
            Map.add_legend(title="Region of Intrest", legend_dict=legend_dict)  
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded  Homa Bay ROI"
                context['sucess_message'] = sucess_message

        Map.add_child(folium.LayerControl())
        figure.render()
        
        context['MyField3'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
# Area Estimation: Meters
class areameters(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        Map.center_object(boundary,9);
        Map.addLayer(boundary,{},"MyField")
          
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated crop areas(Acres)', Total_AreaSqKm.getInfo())
        
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['areameters'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)

# Area Estimation: Acres
class Acres(TemplateView):
    ee.Initialize()
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        Map.center_object(boundary,9);
        Map.addLayer(boundary,{},"MyField") 
         
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).divide(4046.86).round()
        print('Estimated crop areas(Acres)', Total_AreaSqKm.getInfo())
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Acres'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)

# Area Estimation: Hectares
class Hectares(TemplateView):
    ee.Initialize()
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        Map.center_object(boundary,9);
        Map.addLayer(boundary,{},"MyField")
          
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).divide(10000).round()
        print('Estimated crop areas(Hectares)', Total_AreaSqKm.getInfo())
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Hectares'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)

# Area Estimation: Kilometers
class Kilometers(TemplateView):
    ee.Initialize()
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        Map.center_object(boundary,9);
        Map.addLayer(boundary,{},"MyField")
          
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).divide(1000000).round()
        print('Estimated crop areas(KM)', Total_AreaSqKm.getInfo())
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Kilometers'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
            
#Sentinel 2A Data.
class Sentinel_Imagery(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")

            Map.addLayer(boundary,{},"Boundary")
        
            Map.center_object(boundary,9);
            
            global season
            season = ee.Filter.date(start_date,end_date);#Filter image based on the time frame(start_date and end_date)
 #-------------SENTINEL_2A DATA----------------------#  
            global sentinel_2A
            sentinel_2A = ee.ImageCollection('COPERNICUS/S2')\
            .filterBounds(boundary)\
            .filter(season)\
            .median()\
            .select('B1','B2', 'B3', 'B4', 'B5', 'B6', 'B7','B8', 'B10', 'B11')\
            .clip(boundary)
            
            sentinel_2Avispar={"min":0, "max":4000,"bands": ['B4','B3','B2']}#Visualization parameters used.

            Map.addLayer(sentinel_2A,sentinel_2Avispar,"Sentinel Imagery")
                    
        
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded Sentinel 2A for your region"
                context['sucess_message'] = sucess_message
            
        
        Map.add_child(folium.LayerControl())
        figure.render()
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated Total areas', Total_AreaSqKm.getInfo())
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Sentinel_Imagery'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

#Sentinel 1 Data.
class Sentinel_Imagery_1(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")

            global season
            season = ee.Filter.date(start_date,end_date);#Filter image based on the time frame(start_date and end_date)

            #-------------SENTINEL 1(SAR) DATA------------------#
            sentinel_1= ee.ImageCollection('COPERNICUS/S1_GRD');
            sCollection=sentinel_1\
            .filterBounds(boundary) \
            .filter(season) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW'))
            desc=sCollection.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'));
            asc=sCollection.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));

            composite = ee.Image.cat([
            asc.select('VH').mean(),
            asc.select('VV').mean(),
            desc.select('VH').mean()
            ]).focal_median();
            # composite.getInfo()

            Map.addLayer(composite.clip(boundary), {'min': [-25, -20, -25], 'max': [0, 10, 0]}, 'composite')

                      
            Total_studyArea = boundary.geometry().area()
            Total_AreaSqKm = ee.Number(Total_studyArea).round()
            print('Estimated Total areas', Total_AreaSqKm.getInfo())
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded Sentinel 1 for your region ROI"
                context['sucess_message'] = sucess_message
            
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['Sentinel_Imagery_1'] = areaestimate1
        context['MyField'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

#Landsat8 Data.
class Landsat8_Imagery(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")
            # start_date="2020-01-01"#Set start_date(yy/mon/day)
            # end_date="2020-03-31"#Set End_date(yy/mon/day)
            global season
            season = ee.Filter.date(start_date,end_date);#Filter image based on the time frame(start_date and end_date)

            Landsat8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
            .filter(season)\
                    .filterMetadata("CLOUD_COVER", "less_than", 5);

            # Applies scaling factors.
            def applyScaleFactors(image):
                    opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
                    thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
                    return image.addBands(opticalBands, None, True) \
                                .addBands(thermalBands, None, True)

            Landsat8 = Landsat8.map(applyScaleFactors)

            Landsat8_Imagery=Landsat8.mean().clip(boundary)
            visualization = {
            'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
            'min': 0.0,
            'max': 0.3,
            }

            Map.addLayer(Landsat8_Imagery, visualization, 'Landsat 8')  
                
            Total_studyArea = boundary.geometry().area()
            Total_AreaSqKm = ee.Number(Total_studyArea).round()
            print('Estimated Total areas', Total_AreaSqKm.getInfo())
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded Landsat 8 for Your region"
                context['sucess_message'] = sucess_message
            
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Landsat8_Imagery'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

#Normalized Difference Vegetation Index: NDVI.
class NDVI(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")

            global NDVI
            NDVI = sentinel_2A.normalizedDifference(['B8', 'B4'])#normalized difference is computed as (first − second) / (first + second).
            ndvivis_parametres = {'min':0, 'max':1, 'palette': ['FFFFFF','FF0000','FFFF00','008000', '006400','00FFFF','0000FF'] }#NDVI visualization parameters
            Map.addLayer(NDVI, ndvivis_parametres, 'NDVI(Normalized Difference Vegetation Index)')#Add Normalized Difference Vegetation Index to the layers
        
            vis_params = {
                'min': 0,
                'max': 1,
                'palette':['FFFFFF','FF0000','FFFF00','008000', '006400','00FFFF','0000FF'],
            }
            colors = vis_params['palette']
            vmin = vis_params['min']
            vmax = vis_params['max']
            Map.add_colorbar(vis_params,label='Crop Health Analysis')
            legend_dict = {
                    'Non-crops(0 to 0.18)': 'FF0000',
                    'Unhealthly crops(0.18 to 0.41)': 'A52A2A',
                    'Moderately healthy crops(0.41 to 0.0.69)': 'FFFF00',
                    'Very healthy crops(0.69 to 1.0)': '008000',}
            Map.add_legend(title="NDVI Legend", legend_dict=legend_dict)  
                    
            Total_studyArea = boundary.geometry().area()
            Total_AreaSqKm = ee.Number(Total_studyArea).round()
            print('Estimated Total areas', Total_AreaSqKm.getInfo())
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded NDVI for your ROI"
                context['sucess_message'] = sucess_message
            
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['NDVI'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

#Normalized Difference Water Index: NDWI.
class NDWI(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")

            landsat = ee.ImageCollection('LANDSAT/LC08/C01/T1_32DAY_NDWI') \
                   .filter(season)\
                   .first() \
                  .clip(boundary)
            NDWI = landsat.select('NDWI')
            NDWIVis = {
            'min': 0.0,
            'max': 1.0,
            'palette': ['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff'],
            }
            Map.centerObject(boundary,7)
            Map.addLayer(NDWI, NDWIVis, 'NDWI')
            
            vis_params = {
                'min': 0,
                'max': 1,
                'palette':['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff'],
            }
            colors = vis_params['palette']
            vmin = vis_params['min']
            vmax = vis_params['max']
            Map.add_colorbar(vis_params,label='NDWI Readings')
            legend_dict = {
                'Highly Wet': 'ffffff',
                'Moderately Wet': 'ff0000',
                'Low Wetness': 'ffff00',
                'Moderately Dry': '00ffff',
                'Highly Dry': '0000ff',
                }
            Map.add_legend(title="NDWI Legend", legend_dict=legend_dict)  
                    
            Total_studyArea = boundary.geometry().area()
            Total_AreaSqKm = ee.Number(Total_studyArea).round()
            print('Estimated Total areas', Total_AreaSqKm.getInfo())
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded Ewaso  NDWI ROI"
                context['sucess_message'] = sucess_message
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['NDWI'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

#Modified Normalized Difference Water Index: MNDWI.
class MNDWI(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")

            l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
 # Function to cloud mask and generate MNDWI
            def preprocess(image):
                    qa = image.select('QA_PIXEL')
                    dilated = 1 << 1
                    cirrus = 1 << 2
                    cloud = 1 << 3
                    shadow = 1 << 4
                    mask = qa.bitwiseAnd(dilated).eq(0) \
                    .And(qa.bitwiseAnd(cirrus).eq(0)) \
                    .And(qa.bitwiseAnd(cloud).eq(0)) \
                    .And(qa.bitwiseAnd(shadow).eq(0))

    # Cloudfree image
                    masked = image.select(['SR_B.*'], ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']) \
                    .updateMask(mask) \
                    .multiply(0.0000275) \
                    .add(-0.2)
    # Band map
                    bandMap = {
                    'GREEN': masked.select('B3'),
                    'SWIR1': masked.select('B6')
                    }
    # Generate MNDWI
                    global mndwi
                    mndwi = masked.expression('(GREEN - SWIR1) / (GREEN + SWIR1)', bandMap) \
                    .rename('MNDWI')
    # Return the MNDWI and cloudmasked image
                    return image.select([]).addBands([masked, mndwi])
    # Filter collection and create MNDWI
            col = l8.filterBounds(boundary).filter(season).map(preprocess)

    # Vis parameters
            vis = { 'min': -1, 'max': 1, 'palette': ['0000ff', '00ffff', 'ffff00', 'ffffff'] }

            # Median composite
            median = col.median().clip(boundary)
            Map.addLayer(median.select('MNDWI'), vis, 'MNDWI')
            
            vis_params = {
                'min': 0,
                'max': 1,
                'palette':['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff'],
            }
            colors = vis_params['palette']
            vmin = vis_params['min']
            vmax = vis_params['max']
            Map.add_colorbar(vis_params,label='MNDWI Readings')
            legend_dict = {
                    'Non-aqueous surfaces': 'ffffff',
                'Moderate aqueous surfaces': '00ffff',
                'Flooding, humidity': 'ffff00',
                'Water surface': '0000ff',}
            Map.add_legend(title="MNDWI Legend", legend_dict=legend_dict) 
                    
            
            
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded Ewaso  MNDWI ROI"
                context['sucess_message'] = sucess_message
            
        
        Map.add_child(folium.LayerControl())
        figure.render()
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated Total areas', Total_AreaSqKm.getInfo())
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['MNDWI'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

#JRC Global Surface Water.
class JRC_Gloabal_Surface_Water(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")

          #Extraction of Perment water from Global Surface Water(GSW)
            blue_palette = ['0000FF']
            jrcGSW = ee.Image("JRC/GSW1_2/GlobalSurfaceWater")
            waterBodies = jrcGSW.select('occurrence').clip(boundary)
            vis_waterBodies = {min:0, max:100, "palette": blue_palette}
                    
            Map.addLayer(**{
                # mask waterBodies so as to not detect flood in the waterBodies.
                # .divide(100) causes the opacity/transparency of the pixels to
                # be set based on the waterBodies occurrence value.
                
                'ee_object': waterBodies.updateMask(waterBodies.divide(100)),\
                'name': "Permanent water bodies (BLUE)", \
                'vis_params': vis_waterBodies    
            })
            Map.addLayer( waterBodies.updateMask(waterBodies.divide(100)),vis_waterBodies,"Permanent water bodies (BLUE)")               
            
            legend_dict = {
                    'JRC Permanent water bodies': '0000FF',
                    'ROI Boundary': '000000',

                    }
            Map.add_legend(title=" Permanent Legend", legend_dict=legend_dict)
                
        
            
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully Extracted Permanent Water"
                context['sucess_message'] = sucess_message
            
        
        Map.add_child(folium.LayerControl())
        figure.render()
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated Total areas', Total_AreaSqKm.getInfo())
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['JRC_Gloabal_Surface_Water'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
        
#Land Use Land Cover.
class LULC(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")

    #-------------SENTINEL 1(SAR) DATA------------------#
            sentinel_1= ee.ImageCollection('COPERNICUS/S1_GRD');
            sCollection=sentinel_1\
            .filterBounds(boundary) \
            .filter(season) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW'))
            desc=sCollection.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'));
            asc=sCollection.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));

            global composite
            composite = ee.Image.cat([
            asc.select('VH').mean(),
            asc.select('VV').mean(),
            desc.select('VH').mean()
            ]).focal_median();

            #-------------SENTINEL_2A DATA----------------------#  
            global sentinel_2A
            sentinel_2A = ee.ImageCollection('COPERNICUS/S2')\
            .filterBounds(boundary)\
            .filter(season)\
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE",10))\
            .median()\
            .select('B1','B2', 'B3', 'B4', 'B5', 'B6', 'B7','B8', 'B10', 'B11')\
            .clip(boundary)

            sentinel_2Avispar={"min":0, "max":2500,"bands": ['B4','B3','B2']}#Visualization parameters used.

            Map.addLayer(sentinel_2A,sentinel_2Avispar, 'Sentinel-2')#Add sentinel_2A to the layer
                            
                            
            Fused_images = sentinel_2A.addBands(composite)#Creation of composite image of sentinel 1 and sentinel 2A
            fused_vis = {
            'min':0,
            'max'  : 2500,
            'bands' : ['B2', 'B3','B4']#Band selection.
            }
            
            feature_collection = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/Ewaso_training")
            training = ee.FeatureCollection(feature_collection)
            #Create a buffer:
            buffered_data = training.map(lambda f: f.buffer(5))
            # Map.addLayer(training1,{},"buffer")
            label = 'landcover'#Unique property(cropland) with different unique values..
            bands=["B4","B3","B2","VV","VH"]
            global Input
            Input=Fused_images.select(bands)
            trainImage=Input.sampleRegions(**{
            'collection':training,
            'properties':[label],
            'scale':30
            })

            trainingData=trainImage.randomColumn()

            trainSet=trainingData.filter(ee.Filter.lessThan('random',0.75))
            testdata=trainingData.filter(ee.Filter.greaterThanOrEquals('random',0.75))


            #visualization parameters applied on the Random forest classifier

            init_params = {"numberOfTrees":10, # the number of individual decision tree models
            "variablesPerSplit":None,  # the number of features to use per split
            "minLeafPopulation":1, # smallest sample size possible per leaf
            "bagFraction":0.5, # fraction of data to include for each individual tree model
            "maxNodes":None, # max number of leafs/nodes per tree
            "seed":0}  # random seed for "random" choices like sampling. Setting this allows others to reproduce your exact results even with stocastic parameters
            global classifier

            classifier = ee.Classifier.smileRandomForest(**init_params).train(trainImage, label, bands)
            # Classify the image.

            #Application of the random forest classifier for the purpose of image classification.
            global classified
            classified=Input.classify(classifier)
            palette = [
            '2E8B57','228B22','F5DEB3','808080','006400','87CEEB','8B4513'

            ];
            Map.addLayer(classified,
            {'min': 0, 'max': 6, 'palette': palette},
            'classification')


            legend_dict = {
            'Wetlands': '2E8B57',
            'Forest':'228B22',
            'Bareland':'F5DEB3',
            'Settlement':'808080',
            'Vegetation':'006400',
            'Water':'87CEEB',
            'Cultivation':'8B4513'

            }
            Map.add_legend(title="Classification", legend_dict=legend_dict)
                
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded LULC for your ROI"
                context['sucess_message'] = sucess_message
            
        Map.add_child(folium.LayerControl())
        figure.render()
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated Total areas', Total_AreaSqKm.getInfo())
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['LULC'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

#WetLands Detection.
class Wetlands(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")
            global season
            season = ee.Filter.date(start_date,end_date);

            Landsat8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
            .filter(season)
                
            
            l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
            Map.addLayer(boundary,{},"ROI")

            
            # Function to cloud mask and generate MNDWI
            def preprocess(image):
                qa = image.select('QA_PIXEL')
                dilated = 1 << 1
                cirrus = 1 << 2
                cloud = 1 << 3
                shadow = 1 << 4
                mask = qa.bitwiseAnd(dilated).eq(0) \
                .And(qa.bitwiseAnd(cirrus).eq(0)) \
                .And(qa.bitwiseAnd(cloud).eq(0)) \
                .And(qa.bitwiseAnd(shadow).eq(0))

                # Cloudfree image
                global masked
                masked = image.select(['SR_B.*'], ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']) \
                    .updateMask(mask) \
                    .multiply(0.0000275) \
                    .add(-0.2)

                # Band map
                bandMap = {
                'GREEN': masked.select('B3'),
                'SWIR1': masked.select('B6')
                }

                # Generate MNDWI
                mndwi = masked.expression('(GREEN - SWIR1) / (GREEN + SWIR1)', bandMap) \
                .rename('MNDWI')

                # Return the MNDWI and cloudmasked image
                return image.select([]).addBands([masked, mndwi])

            # Filter collection and create MNDWI
            col = l8.filterBounds(boundary).filter(season).map(preprocess)

            # Vis
            vis = { 'min': -1, 'max': 1, 'palette': ['red', 'white', 'blue'] }

            # Median composite
            median = col.median().clip(boundary)
        

            # Permanent water or river
            permanent = median.select('MNDWI').gt(0.4)
            Map.addLayer(permanent.selfMask(), { 'palette': 'blue' }, 'Permanent water or River')

            # Maximum composite
            max = col.reduce(ee.Reducer.percentile([98])).select('MNDWI_p98').clip(boundary)

            # Wetland
            wetland = max.gt(0).And(permanent.eq(0))
            Map.addLayer(wetland.selfMask(), { 'palette': '008080' }, 'Wetland')
            legend_dict = {
                    'Wetland': '008080',
                    'Permanent Water': '0000FF',
                    }
            Map.add_legend(title="Wetlands Legend", legend_dict=legend_dict)
            
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded Mapped Wetlands for your ROI"
                context['sucess_message'] = sucess_message
            
        Map.add_child(folium.LayerControl())
        figure.render()
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated Total areas', Total_AreaSqKm.getInfo())
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Wetlands'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

