import numpy as np
import matplotlib.pyplot as plt
from abc import abstractmethod
from MilPython import LPObject,LPInputdata,LPStateVar_timedep
from .component import Component
from types import MethodType
CP_Water = 4.186/3.6 # Specific heat capacity of water in Wh/kg (?)#TODO

def temp_to_Q(temp,cap):
        return temp * cap

class StorageLP(LPObject):
    def __init__(self, inputdata, name, comment=''):
        super().__init__(inputdata, name, comment)
        self.temp:LPStateVar_timedep = None
    def addHeatTransfer(self,heatTransfer,sign):
        pass

class Storage(Component):
    def __init__(self,name):
        self.lpObject:StorageLP = None
    @abstractmethod
    def get_temp(self):
        pass
    @abstractmethod
    def get_temp_res(self):
        pass
    
class ThermalStorage(Storage):
    _series_map = {
        'Name': 'name',
        'Capacity': 'cap',
        'Temperature': lambda self: self.get_temp(),
        }
    def __init__(self,name):
        Component.__init__(self,name)
        self.col=None
        self.cap=None
        self.temp=None
        self.tempMin=None
        self.tempMax=None
        self.__Q=None
        self.mass=None  # Volume, if applicable
    @classmethod
    def fromPDSeries(cls, pdSeries):
        return cls.newStorage(
            cap=pdSeries['Capacity'],
            temp=pdSeries['Temperature'],
            name=pdSeries['Name'])
    @classmethod    
    def newStorage(cls,cap,temp,name=None,tempMin=0,tempMax=np.inf):
        storage = cls(name)
        storage.cap = cap
        storage.tempMin = tempMin
        storage.tempMax = tempMax
        storage.__Q = temp_to_Q(temp, cap)
        return storage
    
    @classmethod
    def newStorageByMass(cls,mass,cp,temp,name=None,tempMin=0,tempMax=np.inf):
        storage = cls(name)
        storage.cap = mass * cp
        storage.mass=mass
        storage.tempMin = tempMin
        storage.tempMax = tempMax
        storage.__Q = temp_to_Q(temp, storage.cap)
        return storage
    
    def sim_prep(self, num_steps=None):
        if num_steps:
            self.__Q_res = np.zeros(num_steps+1)
        else:
            self.__Q_res = []
    
    def set_col(self,col:int):
        self.col = col
    
    def set_Q(self, Q, t):
        self.__Q = Q
        if isinstance(self.__Q_res,np.ndarray):
            self.__Q_res[t] = Q
        else:
            self.__Q_res.append(Q)
    
    def set_temp(self,temp):
        self.__Q = temp_to_Q(temp, self.cap)
    
    def get_Q(self):
        return self.__Q
    
    def get_temp(self):
        return self.__Q / self.cap 
    
    def get_temp_res(self):
        return np.array(self.__Q_res) / self.cap
    
    def get_Q_res(self):
        try:
            return self.__Q_res
        except:
            raise Exception('First run the simulation, then get get results.')
    
    def plot_temp_res(self,ax,color=None):
        temp_res = self.get_temp_res()
        if color:
            ax.plot(temp_res,label=self.name,color=color)
        else:
            ax.plot(temp_res,label=self.name)

    def makeLPObject(self,inputdata:LPInputdata):
        self.lpObject = ThermalStorageLP(inputdata,self.name,self.cap,self.tempMin,self.tempMax,temp0=self.get_temp())
        return self.lpObject




class ThermalStorageLP(StorageLP):
    def __init__(self, inputdata, name,cap,tempMin,tempMax,temp0, comment=''):
        super().__init__(inputdata, name, comment)
        self.tempMin = tempMin
        self.tempMax = tempMax
        # self.Q0 = temp_to_Q(temp0,cap)
        self.temp_0=temp0
        self.cap = cap
        self.heatTransferLst=[]
        self.Q = self.add_time_var(name+'_Q')
        self.temp = self.add_time_var(name+'_temp','',lb=tempMin,ub=tempMax)
        
    def addHeatTransfer(self, q,sign):
        self.heatTransferLst.append([q,sign])
    
    def def_equations(self):
        # Q-T-Zusammenhang
        self.add_eq([[self.Q,1],
                     [self.temp,-self.cap]])
        step0_eq_lst=[[self.Q,1,0]]
        step0_eq_lst.extend([q,-sign*self.inputdata.dt_h,0] for q,sign in self.heatTransferLst)
        self.add_eq(step0_eq_lst,
                    b=temp_to_Q(self.temp_0,self.cap))

        for t in range(1,self.inputdata.steps):
            eq_lst = [[self.Q,1,t],
                        [self.Q,-1,t-1]]
            #! das geht so nur für conduction
            eq_lst.extend([q,-sign*self.inputdata.dt_h,t] for q,sign in self.heatTransferLst)
            self.add_eq(eq_lst)

        self.__def_add_equations()

    def __def_add_equations(self):
        pass

    def set_add_equations(self,func):
        self.__def_add_equations = MethodType(func,self)

class ExtStorage(Storage):
    _series_map = {
        'Name': 'name',
        'Temperature': lambda self: self.get_temp(),
        }
    def __init__(self,name,temp):
        Component.__init__(self,name)
        self.__temp = temp
        self.__temp_res = []
    @classmethod
    def newExtStorage(cls,name=None,temp=None):
        storage = cls(name,temp)
        return storage
    
    def sim_prep(self, num_steps=None):
        self.Q_sum = 0
        if num_steps:
            self.__q_res = np.zeros(num_steps+1)
        else:
            self.__q_res = []
    
    def add_q(self, q, t=None):
        self.Q_sum += q #! das ist glaube ich noch iene Leistung
        if t:
            self.__q_res[t] = q
    def set_temp(self,temp):
        self.__temp = temp
    def get_temp(self):
        return self.__temp
    def get_q_res(self):
        return self.__q_res
    def save_temp(self):
        self.__temp_res.append(self.__temp)
    def get_temp_res(self):
        return np.array(self.__temp_res)
    @classmethod
    def fromPDSeries(cls, pdSeries):
        return cls.newExtStorage(
            temp=pdSeries['Temperature'],
            name=pdSeries['Name'])
    
    def makeLPObject(self,inputdata:LPInputdata):
        self.lpObject = ExtStorageLP(inputdata,self.name,temp=self.get_temp())
        return self.lpObject


class ExtStorageLP(StorageLP):
    def __init__(self, inputdata:LPInputdata, name,temp, comment=''):
        super().__init__(inputdata, name, comment)
        self.temp_arr = None
        if self.name in inputdata.data:
            self.temp_arr = inputdata.data[self.name]
        elif temp is not None:
            self.temp_arr = np.full(inputdata.steps,temp)
        else:
            raise ValueError(f'No temperature data provided for external storage {self.name}.')

        self.heatTransferLst=[]
        self.temp = self.add_time_var(name+'_temp','',lb=-np.inf)
        
    def addHeatTransfer(self, q,sign):
        self.heatTransferLst.append([q,sign])
    
    def def_equations(self):
        self.add_eq([[self.temp,1]],
                    b=self.temp_arr)
        self.__def_add_equations()

    def __def_add_equations(self):
        pass

    def set_add_equations(self,func):
        self.__def_add_equations = MethodType(func,self)