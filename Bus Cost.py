import json, random
from qgis.core import QgsVectorLayer, QgsProject, QgsApplication, QgsSimpleMarkerSymbolLayerBase
from urllib.request import urlopen
from qgis.utils import iface
from qgis.core import QgsVectorLayer, QgsFeatureRequest, QgsGeometry
from qgis.core import QgsCoordinateReferenceSystem 
import processing
import decimal
from decimal import Decimal
from qgis.PyQt.QtCore import QVariant

layer = iface.activeLayer()
#data = layer.dataProvider();
#data.addAttributes([QgsField('BusCost', QVariant.Double)])
#layer.updateFields()
layer.startEditing()
count = 0
for f in layer.getFeatures():
    cool = f['HubName']
    stop = f['stop_name']
    print(cool)
    print(stop)
    Cooling = processing.run("native:extractbyattribute", {'INPUT':'C:/Users/s-lch/OneDrive - Lake Washington School District/Extra curricular/Summer Programs/2023 Summer/temp2.shp','FIELD':'Street','OPERATOR':0,'VALUE':cool,'OUTPUT':'TEMPORARY_OUTPUT'})
    Stops = processing.run("native:extractbyattribute", {'INPUT':'C:/Users/s-lch/Documents/Stops.geojson','FIELD':'stop_name','OPERATOR':0,'VALUE':stop,'OUTPUT':'TEMPORARY_OUTPUT'})
    for g in Cooling['OUTPUT'].getFeatures():
        lo= g.geometry().asPoint().x()
        la= g.geometry().asPoint().y()
    for g in Stops['OUTPUT'].getFeatures():
        lol= g.geometry().asPoint().x()
        lal= g.geometry().asPoint().y()
    print(lo)
    print(la)
    print(lol)
    print(lal)
    result = shortest_path(lo,la,lol,lal,0.15,0.15,0,0)
    print(result)
    layer.changeAttributeValue(f.id(),16,result)
   
layer.commitChanges()
