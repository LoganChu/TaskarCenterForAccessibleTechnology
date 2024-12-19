from qgis.utils import iface
from qgis.core import QgsVectorLayer, QgsFeatureRequest, QgsGeometry
from qgis.core import QgsCoordinateReferenceSystem 
import processing

layer = iface.activeLayer()
# We need to have a variable that is the combined versions of all the centroids

result = processing.run("native:extractbyattribute", {'INPUT': layer,'FIELD':'OBJECTID_2','OPERATOR':0,'VALUE':1,'OUTPUT':'TEMPORARY_OUTPUT'})
result1 = processing.run("native:dissolve", {'INPUT':result['OUTPUT'],'FIELD':[],'SEPARATE_DISJOINT':False,'OUTPUT':'TEMPORARY_OUTPUT'})
result2 = processing.run("native:centroids", {'INPUT': result1['OUTPUT'],'ALL_PARTS':False,'OUTPUT':'TEMPORARY_OUTPUT'})
constant = result2['OUTPUT']

for f in range(2,133): 
    result = processing.run("native:extractbyattribute", {'INPUT': layer,'FIELD':'OBJECTID_2','OPERATOR':0,'VALUE':f,'OUTPUT':'TEMPORARY_OUTPUT'})
    result1 = processing.run("native:dissolve", {'INPUT':result['OUTPUT'],'FIELD':[],'SEPARATE_DISJOINT':False,'OUTPUT':'TEMPORARY_OUTPUT'})
    result2 = processing.run("native:centroids", {'INPUT': result1['OUTPUT'],'ALL_PARTS':False,'OUTPUT':'TEMPORARY_OUTPUT'})
    mergelayer = processing.run("native:mergevectorlayers", {'LAYERS':[constant,result2['OUTPUT']],'CRS':QgsCoordinateReferenceSystem('EPSG:3857'),'OUTPUT':'TEMPORARY_OUTPUT'})
    constant = mergelayer['OUTPUT']
QgsProject.instance().addMapLayer(constant)
