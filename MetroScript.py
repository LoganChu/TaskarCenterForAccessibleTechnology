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

#select features by ID, find closest to the cooling center
#Do this bus stops within a certain range from the centroid
#cooling center is not limited to closest one to the centroid as buses are air conditioned
#Base bus stop distance on whether it is less than the walking distance to the nearest cooling center

def shortest_path(lon1, lat1, lon2, lat2, uphill, downhill, avoidCurbs, streetAvoidance):
    url = 'http://incremental-alpha.westus.cloudapp.azure.com/api/v1/routing/shortest_path/custom.json?&lon1='+str(lon1)+'&lat1='+str(lat1)+'&lon2='+str(lon2)+'&lat2='+str(lat2)+'&uphill='+str(uphill)+'&downhill='+str(downhill)+'&avoidCurbs='+str(avoidCurbs)+'&streetAvoidance='+str(streetAvoidance)+'&timestamp=0'
    try:
        r = urlopen(url)
    except HTTPError as e:
        if e.code == 422:
            print('Validation error: ' + e.read().decode())
            return
        else:
            raise e
    
    data = json.loads(r.read())
    
    if not "routes" in data:
        print('No results were returned from AccessMap: ' + str(data))
        return
    
    return str(data["routes"][0]["total_cost"])
   
layer = iface.activeLayer()
layer.startEditing()
#data = layer.dataProvider();
stops = QgsVectorLayer("C:/Users/s-lch/Documents/Stops.geojson", "stops", "ogr")
#data.addAttributes([QgsField('BusCost', QVariant.Double)])

for f in layer.getFeatures():
    cost = f['Cost_2']
    ID = f['OBJECTID']
    print(ID)
    x = f.geometry().asPoint().x()
    y = f.geometry().asPoint().y()
    print(x)
    print(y)
    #output = processing.run("native:extractbyexpression", {'INPUT': 'C:/Users/s-lch/Documents/Stops.geojson', 'EXPRESSION': float(shortest_path('x(@geometry)','y(@geometry)',x,y,0.15,0.15,0,0))<float(cost), 'OUTPUT': 'TEMPORARY_OUTPUT'})
    #QgsProject.instance().addMapLayer(stops)
    myset = set()
    Single = processing.run("native:extractbyattribute", {'INPUT':'C:/Users/s-lch/Documents/Centroid of Residential Areas.geojson','FIELD':'OBJECTID','OPERATOR':0,'VALUE':ID,'OUTPUT':'TEMPORARY_OUTPUT'})
    options = processing.run("native:extractwithindistance", {'INPUT':'C:/Users/s-lch/Documents/Stops.geojson','REFERENCE':Single['OUTPUT'],'DISTANCE':0.025,'OUTPUT':'TEMPORARY_OUTPUT'})
    #QgsProject.instance().addMapLayer(Single['OUTPUT'])
    #QgsProject.instance().addMapLayer(options['OUTPUT'])
    for g in options['OUTPUT'].getFeatures():
        if(float(shortest_path(g.geometry().asPoint().x(),g.geometry().asPoint().y(),x,y,0.15,0.15,0,0))<cost):
            id = g['route_ids']
            print(id)
            #ids = id.split(", ")
            for i in id:
                myset.add(i)
    print(myset)

    #adds all unique routes to myset to be processed
    min = float("inf")
    for i in myset:
        output =  processing.run("native:extractbyattribute", {'INPUT':'Stops-Cooling Distance.geojson','FIELD':'route_ids','OPERATOR':7,'VALUE':'4','OUTPUT':'TEMPORARY_OUTPUT'})
        for g in output['OUTPUT'].getFeatures():
            #Access cost of each stop 
            min = min(min,g['BusCost'])
            
    print(min)
    break
    layer.changeAttributeValue(f.id(),74,min)
    layer.commitChanges()
    #Selects bus stops whose travel costs are less than that of walking
    break
    #Selects those features that contain the route id and thus are on the bus route
layer.commitChanges()
    
    
    
    
    