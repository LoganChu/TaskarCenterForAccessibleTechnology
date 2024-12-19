#This will go through each feature in the hub distance and find the features for each line in the centroid of 
#Residential areas layer and stops layer. Getting the latitudes and longitudes of those points, we will use the 
#Shortest Path script to find the shortest path and it's cost. 

from qgis.utils import iface
from qgis.core import QgsVectorLayer, QgsFeatureRequest, QgsGeometry
from qgis.core import QgsCoordinateReferenceSystem 
import processing
import ShortestPath

layer = iface.activeLayer()

for f in layer.getFeatures():
    Addy1 = f['ADDRESS']
    Addy2 = f['HubName']
    Cooling = processing.run("native:extractbyattribute", {'INPUT':'C:/Users/s-lch/OneDrive - Lake Washington School District/Extra curricular/Summer Programs/2023 Summer/temp1.shp','FIELD':'Street','OPERATOR':0,'VALUE':Addy2,'OUTPUT':'TEMPORARY_OUTPUT'})
    Residential = processing.run("native:extractbyattribute", {'INPUT':'Centroids of Residential Areas.geojson','FIELD':'ADDRESS','OPERATOR':0,'VALUE':Addy1,'OUTPUT':'TEMPORARY_OUTPUT'})
    for f in Cooling['OUTPUT'].getFeatures():
        geom = f.geometry()
        lon= geom.asPoint().x()
        lat= geom.asPoint().y()
    for f in Residential['OUTPUT'].getFeatures():
        geom = f.geometry()
        lon1= geom.asPoint().x()
        lat1= geom.asPoint().y()
    result = ShortestPath.shortest_path(lon1=-122.33382843985366,
    lat1=47.60721229035356,
    lon2=-122.32559266931791,
    lat2=47.6090337327238,
    uphill=0.1,
    downhill=0.1,
    avoidCurbs=1,
    streetAvoidance=1)
        #Shortest Path with the latitudes and longitudes and add that value to the layer