import json, random
from qgis.core import QgsVectorLayer, QgsProject, QgsApplication, QgsSimpleMarkerSymbolLayerBase
from urllib.request import urlopen
from qgis.utils import iface
from qgis.core import QgsVectorLayer, QgsFeatureRequest, QgsGeometry
from qgis.core import QgsCoordinateReferenceSystem 
import processing
from qgis.PyQt.QtCore import QVariant

def shortest_path(lon1, lat1, lon2, lat2, uphill, downhill, avoidCurbs, streetAvoidance):
    url = 'http://incremental-alpha.westus.cloudapp.azure.com/api/v1/routing/shortest_path/custom.json?&lon1='+str(lon1)+'&lat1='+str(lat1)+'&lon2='+str(lon2)+'&lat2='+str(lat2)+'&uphill='+str(uphill)+'&downhill='+str(downhill)+'&avoidCurbs='+str(avoidCurbs)+'&streetAvoidance='+str(streetAvoidance)+'&timestamp=0'
    
    downloaded_file_prefix = 'c:/temp/temp'
    downloaded_file = downloaded_file_prefix+str(random.randrange(100000))+'.json'

    layer_name = 'Shortest Path'

    r = urlopen(url)
    data = json.loads(r.read())
    
    if not "routes" in data:
        print('No results were returned from AccessMap: ' + str(data))
        return
    
    return str(data["routes"][0]["total_cost"])
   

layer = iface.activeLayer()
#data = layer.dataProvider();
#data.addAttributes([QgsField('Cost', QVariant.Double)])
#layer.updateFields()
count = 0
layer.startEditing()

for f in layer.getFeatures():
    count +=1
    Addy1 = f['ADDRESS']
    Addy2 = f['HubName']
    Residential = processing.run("native:extractbyattribute", {'INPUT':'Centroid of Residential Areas.geojson','FIELD':'ADDRESS','OPERATOR':0,'VALUE':Addy1,'OUTPUT':'TEMPORARY_OUTPUT'})
    Cooling = processing.run("native:extractbyattribute", {'INPUT':'Cooling Center 2.geojson','FIELD':'Street','OPERATOR':0,'VALUE':Addy2,'OUTPUT':'TEMPORARY_OUTPUT'})
    #QgsProject.instance().addMapLayer(Cooling['OUTPUT'])
    #QgsProject.instance().addMapLayer(Residential['OUTPUT'])
    lo,la,lol,lal = "","","",""
    for g in Cooling['OUTPUT'].getFeatures():
        geom = g.geometry()
        lo= geom.asPoint().x()
        la= geom.asPoint().y()
    for g in Residential['OUTPUT'].getFeatures():
        centroid = g.id()
        geom = g.geometry()
        lol= geom.asPoint().x()
        lal= geom.asPoint().y()
    print(Addy1)
    print(Addy2)
    print(lo)
    print(la)
    print(lol)
    print(lal)
    result = shortest_path(lo,la,lol,lal,0.05,0.05,1,0)
    print(result)
    id = f.id()
    print(id)
    layer.changeAttributeValue(id,75,result)
    print(count) 

layer.commitChanges()
   


