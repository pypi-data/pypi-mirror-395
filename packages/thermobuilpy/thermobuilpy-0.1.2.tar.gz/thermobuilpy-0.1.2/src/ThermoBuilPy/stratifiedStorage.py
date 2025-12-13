from .storage import ThermalStorage,ExtStorage
from .connection import Conduction,FreeConvection
from .component import Component
CP_Water = 4.186/3.6 # Specific heat capacity of water in Wh/kg (?)#TODO
import matplotlib.pyplot as plt
class StratifiedStorage(Component):
    _series_map = {
        'Name': 'name',
        'Layers': 'layers',
        'Conductions': 'conductions',
        'FreeConvections': 'freeConvections',
        'Losses':'losses',
        'Surrounding':'surrounding'
    }
    def __init__(self,name):
        Component.__init__(self,name)
        self.layers:list[ThermalStorage] = []
        self.conductions:list[Conduction] = []
        self.freeConvections:list[FreeConvection] = []
        self.losses:list[Conduction]=[]
        self.surrounding:ExtStorage
    
    @classmethod
    def newStratifiedStorageByMasses(cls, layerMasses:list,layerTemperatures:list,conductionCoeff:list[float]|float,freeConvectionMassFlow:list[float]|float=0,lossConductionCoeff:list[float]|float=0,temp_surrounding:float=20,cpFluid=CP_Water, name=None): #TODO name: Stratified or MultiLayer?
        storage = cls(name)
        if not isinstance(conductionCoeff,list):
            conductionCoeff = [conductionCoeff] * (len(layerMasses) - 1)
        if not isinstance(freeConvectionMassFlow,list):
            freeConvectionMassFlow = [freeConvectionMassFlow] * (len(layerMasses) - 1)
        if not isinstance(lossConductionCoeff,list):
            lossConductionCoeff = [lossConductionCoeff]*len(layerMasses)
        if not len(layerMasses) == len(layerTemperatures) == len(lossConductionCoeff) == len(conductionCoeff)+1 == len(freeConvectionMassFlow)+1:
            raise ValueError("layerVolumes and layerTemperatures must have the same length.")
        
        storage.surrounding = ExtStorage('StratStor_surrounding',temp_surrounding)

        for i in range(len(layerMasses)):
            layer=ThermalStorage.newStorageByMass(layerMasses[i], cpFluid, layerTemperatures[i])
            storage.layers.append(layer)

            storage.losses.append(Conduction(layer,storage.surrounding,lossConductionCoeff[i]))

        for i, cond_coeff in enumerate(conductionCoeff):
            storage.conductions.append(
                Conduction(
                    storage1=storage.layers[i],
                    storage2=storage.layers[i+1],
                    coeff=cond_coeff
                )
            )
        for i, mFlow in enumerate(freeConvectionMassFlow):
            storage.freeConvections.append(
                FreeConvection.newFreeConvection(
                    storage1=storage.layers[i],
                    storage2=storage.layers[i+1],
                    massFlow=mFlow,
                    cpFluid=cpFluid
                    )
                )
        return storage
    
    @classmethod
    def newStratifiedStorageByCapacities(cls, layerCapacities:list,layerTemperatures:list,conductionCoeff:list[float]|float,freeConvectionMassFlow:list[float]|float=0,lossConductionCoeff:list[float]|float=0,temp_surrounding:float=20,cpFluid=CP_Water, name=None): #TODO name: Stratified or MultiLayer?
        storage = cls(name)
        if not isinstance(conductionCoeff,list):
            conductionCoeff = [conductionCoeff] * (len(layerCapacities) - 1)
        if not isinstance(freeConvectionMassFlow,list):
            freeConvectionMassFlow = [freeConvectionMassFlow] * (len(layerCapacities) - 1)
        if not isinstance(lossConductionCoeff,list):
            lossConductionCoeff = [lossConductionCoeff]*len(layerCapacities)
        if not len(layerCapacities) == len(layerTemperatures) == len(lossConductionCoeff) == len(conductionCoeff)+1 == len(freeConvectionMassFlow)+1:
            raise ValueError("layerCapacities and layerTemperatures must have the same length.")
        
        storage.surrounding = ExtStorage('StratStor_surrounding',temp_surrounding)


        for i in range(len(layerCapacities)):
            layer = ThermalStorage.newStorage(layerCapacities[i],layerTemperatures[i])
            storage.layers.append(layer)

            storage.losses.append(Conduction(layer,storage.surrounding,lossConductionCoeff[i]))

        for i, cond_coeff in enumerate(conductionCoeff):
            storage.conductions.append(
                Conduction(
                    storage1=storage.layers[i],
                    storage2=storage.layers[i+1],
                    coeff=cond_coeff
                )
            )
        for i, mFlow in enumerate(freeConvectionMassFlow):
            storage.freeConvections.append(
                FreeConvection.newFreeConvection(
                    storage1=storage.layers[i],
                    storage2=storage.layers[i+1],
                    massFlow=mFlow,
                    cpFluid=cpFluid
                    )
                )
        return storage
    
    def updateConductionCoeffs(self, conductionCoeff:list[float]|float):
        if not isinstance(conductionCoeff,list):
            conductionCoeff = [conductionCoeff] * (len(self.layers) - 1)
        if not len(conductionCoeff) == len(self.layers) - 1:
            raise ValueError("conductionCoeff must have length equal to number of layers - 1.")
        for i,cond in enumerate(self.conductions):
            cond.coeff = conductionCoeff[i]
    
    
    def getLayers(self, start:int, end:int):
        if start < 0 or end >= len(self.layers) :
            raise IndexError("Invalid layer indices.")
        if start<end:
            return self.layers[start:end+1]
        else:
            return list(reversed(self.layers[end:start+1]))
        
    def getLayer(self, i:int):
        if i<0 or i> len(self.layers)-1:
            raise ValueError(f'Storage has {len(self.layers)} layers. Index must be 0<=i<{len(self.layers)}')
        return self.layers[i]
    
    def get_losses_total(self):
        losses = 0
        for loss in self.losses:
            losses += loss.get_heatflow_res()
        return losses  
    
    def get_temps_res(self):
        lst=[]
        [lst.append(l.get_temp_res()) for l in self.layers]
        return lst
    
    def get_temps(self):
        lst=[]
        for l in self.layers:
            lst.append(l.get_temp())
        return lst

    def get_temp_mean(self):
        temps = self.get_temps()
        temp_avg = sum([t*layer.cap for t,layer in zip(temps,self.layers)])/sum([layer.cap for layer in self.layers])
        return temp_avg


    def plot_temp_res(self):
        for i,layer in enumerate(self.layers):
            plt.plot(layer.get_temp_res(), label=layer.name)
        plt.title(f'Temperature of {self.name} Layers Over Time')
        plt.xlabel('Time Step')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.show()

    def plot_losses_res(self):
        for i,cond in enumerate(self.losses):
            plt.plot(cond.get_heatflow_res(),label=cond.name)
        plt.title(f'Thermal Losses of {self.name} Layers Over Time')
        plt.xlabel('Time Step')
        plt.ylabel('Heatflow in W')
        plt.legend()
        plt.show()            