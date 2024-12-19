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
for f in layer.getFeatures():
    #index  = float(f['PIN_2'])
    #percent = f['Dissolve_1']
    #index+=index*percent/100;
    #index = f['PCT_PEOPLE']
    #index = f['PCT_ENGLIS']
    #index = f['SOCIOECO_2']
    index = f['PCT_POP_UN']*100
    print(index)