import os
import yaml
import numpy as np
from operator import itemgetter


class Configuration(dict):

    def __init__(self, data):
        if isinstance(data, dict):
            super().__init__(data)
        elif isinstance(data, str) and os.path.exists(data):
            with open(data) as f:
                super().__init__(yaml.load(f, Loader=yaml.FullLoader))
        else:
            raise TypeError('Wrong configuration data type', type(data), data)

    def __getattr__(self, attr):
        return lambda: self[attr]

    def gasMixture(self):
        return self.get('GasMixture', 99.99)

    def getMeasurements(self, voltage='all', angle='all')
        itemList = []
        itemList.append(voltage)
        if voltage == "all":
            itemList = ['Voltage_m20', 'Voltage_m10', 'Voltage_nominal', 'Voltage_p10', 'Voltage_p20']
        tupla = itemgetter(*itemList)(self.Measurements())
        return tupla
        #def _getAngle(element, angle):
        #    itemList = [] 
        #    itemList.append(angle)
        #    if angle == "all":
        #        itemList = ["angle_0", "angle_15"]
        #    return itemgetter(*itemlist)(element.get("angle_scan"))
        #
        #return _getAngle(tupla, angle)
