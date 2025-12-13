from .component import Component
from .storage import Storage,ThermalStorage,ExtStorage
import numpy as np
import matplotlib.pyplot as plt
from MilPython import LPObject,LPInputdata
from types import MethodType
CP_Water = 4.186/3.6 # Specific heat capacity of water in Wh/kg (?)#TODO
class Connection(Component):
    def get_heatflow_res(self):
        raise NotImplementedError("This method should be implemented in subclasses.")
    def set_simulation_parameter(self,method,stepsize):
        self.simulation_method = method
        self.stepsize = stepsize
    def plot_heatflow_res(self,ax,color=None):
        heatflow_res = self.get_heatflow_res()
        if color:
            ax.plot(heatflow_res,label=self.name,color=color)
        else:
            ax.plot(heatflow_res,label=self.name)
    def makeLPObject(self,lpInputdata):
        raise NotImplementedError("This method should be implemented in subclasses.")

class Conduction(Connection):
    _series_map = {
        'Name': 'name',
        'Storage1': 'storage1.name',
        'Storage2': 'storage2.name',
        'Coeff': 'coeff'}
    def __init__(self, storage1, storage2,coeff,name=None):
        Component.__init__(self,name)
        self.coeff=coeff
        self.storage1:Storage = storage1
        self.storage2:Storage = storage2
        self.storages = [storage1, storage2]
            
    @classmethod
    def newConduction(cls,storage1:Storage,storage2,coeff:float,name:str=None):
        cls=cls(storage1,storage2,coeff,name)
        return cls
    
    def get_heatflow_res(self):
        from .thermalSystem import SimulationMethod
        t1_res = self.storage1.get_temp_res()
        t2_res = self.storage2.get_temp_res()
        match self.simulation_method:
            case SimulationMethod.EXPLICIT_EULER:
                return self.coeff * (t1_res[:-1] - t2_res[:-1])
            case SimulationMethod.IMPLICIT_EULER:
                return self.coeff * (t1_res[1:] - t2_res[1:])
            case SimulationMethod.CRANK_NICOLSON:
                expl=self.coeff * (t1_res[:-1] - t2_res[:-1])
                impl=self.coeff * (t1_res[1:] - t2_res[1:])
                return 0.5 * (expl + impl)
    
    def makeLPObject(self,inputdata:LPInputdata):
        self.lpObject = ConductionLP(inputdata,self.name,self.storage1,self.storage2,self.coeff)
        return self.lpObject

class ConductionLP(LPObject):
    def __init__(self, inputdata, name,storage1:Storage,storage2:Storage,coeff:float,qMin=-np.inf,qMax=np.inf,comment=''):
        super().__init__(inputdata, name, comment)
        self.storage1=storage1
        self.storage2=storage2
        self.coeff=coeff
        self.q = self.add_time_var('q','',lb=qMin,ub=qMax)

        self.storage1.lpObject.addHeatTransfer(self.q,-1)
        self.storage2.lpObject.addHeatTransfer(self.q,1)
        
    def def_equations(self):
        # Standard erstmal impliziter Euler? #! TODO
        if True:
            self.add_eq([[self.q,1],
                         [self.storage1.lpObject.temp,-self.coeff],
                         [self.storage2.lpObject.temp,self.coeff]])
        self.__def_add_equations()

    def __def_add_equations(self):
        pass

    def set_add_equations(self,func):
        self.__def_add_equations = MethodType(func,self)
        
class GeneralHeatTransfer(Connection):
    '''
    ! This is only for cases where the other methods don't work.
    It only sets the equations for the targetStorage.
    If you want to set up a connection between multiple storages and can't use the other methods, you have to set up the connection for all storages individually.
    '''
    _series_map = {
        'Name': 'name',
        'TargetStorage': 'targestStorage.name',
        'StorageList': 'storageList',
        'CoeffList': 'coeffList',
        'b': 'b'
    }
    def __init__(self,name):
        Component.__init__(self,name)
        self.targestStorage:ThermalStorage = None
        self.b:float=None
        self.__b_res=[]
    def save_b(self):
        self.__b_res.append(self.b)
    def get_heatflow_res(self):
        return self.__b_res
    
    @classmethod
    def newGeneralHeatTransfer(cls, targetStorage:ThermalStorage,b:float=0, name=None):
        con = cls(name)
        con.targestStorage = targetStorage
        con.b = b
        return con
    
    def makeLPObject(self, lpInputdata):
        self.lpObject=GeneralHeatTransferLP(lpInputdata,self.name,self.targestStorage,self.b)
        return self.lpObject

class GeneralHeatTransferLP(LPObject):
    def __init__(self, inputdata, name, targetStorage:ThermalStorage,b:float=0,comment=''):
        super().__init__(inputdata, name,comment)

        self.targetStorage=targetStorage
        self.b=b
        self.q = self.add_time_var('q','',lb=-np.inf)

        self.targetStorage.lpObject.addHeatTransfer(self.q,1)

    def def_equations(self):
        if isinstance(self.b,list):
            for t in range(self.inputdata.steps):
                self.add_eq([[self.q,1,t]],b=self.b[t])
        else:
            self.add_eq([[self.q,1]],
                        b=self.b)
                        
        self.__def_add_equations()

    def __def_add_equations(self):
        pass

    def set_add_equations(self,func):
        self.__def_add_equations = MethodType(func,self)


class FreeConvection(Connection):
    '''
    Free convection in stratified storages between layer a and b where a is below b if temp(a) > temp(b) with given mass flow
    '''
    _series_map = {
        'Name': 'name',
        'Storage1': 'storage1.name',
        'Storage2': 'storage2.name',
        'MassFlow': lambda self: self.get_mFlow(),
        'CpFluid': 'cpFluid',
        'Tolerance': 'tolerance'
    }
    def __init__(self,name):
        Component.__init__(self,name)
        self.storage1:ThermalStorage = None
        self.storage2:ThermalStorage = None
        self.__massFlow:float = None
        self.__massFlow_res = []
        self.tolerance:float = None
        self.cpFluid = None
        
    @classmethod
    def newFreeConvection(cls, storage1:ThermalStorage, storage2:ThermalStorage, massFlow:float, cpFluid=CP_Water, tolerance=0.1,name=None):
        con = cls(name)
        con.storage1 = storage1
        con.storage2 = storage2
        con.__massFlow = massFlow
        con.cpFluid = cpFluid
        con.tolerance = tolerance
        return con
    
    def set_mFlow(self, mFlow):
        if mFlow<0:
            raise ValueError("mFlow must be non-negative. For flows in opposite direction set up a seperate ForcedFlow.")
        self.__massFlow = mFlow
    def get_mFlow(self):
        return self.__massFlow
    def save_massFlow(self):
        self.__massFlow_res.append(self.__massFlow)
    def get_massFlow_res(self):
        return self.__massFlow_res
    
class ForcedConvection(Connection):
    _series_map = {
        'Name': 'name',
        'StorageList': 'storageList',
        'MassFlow': lambda self: self.get_mFlow(),
        'CpFluid': 'cpFluid'
    }
    def __init__(self,name):
        Component.__init__(self,name)
        self.storageList = None
        self.__massFlow = None
        self.cpFluid = None
        self.__massFlow_res = []
        
    def set_mFlow(self, mFlow):
        if mFlow<0:
            raise ValueError("mFlow must be non-negative. For flows in opposite direction set up a seperate ForcedFlow.")
        self.__massFlow = mFlow
        
    def get_mFlow(self):
        return self.__massFlow
    
    def save_massFlow(self):
        self.__massFlow_res.append(self.__massFlow)
    def get_massFlow_res(self):
        return np.array(self.__massFlow_res)
    
    def get_heatflow_res(self):
        from .thermalSystem import SimulationMethod
        temp_res_list = [storage.get_temp_res() for storage in self.storageList]
        match self.simulation_method:
            case SimulationMethod.EXPLICIT_EULER:
                q_lst=[]
                for i in range(len(self.storageList)-1):
                    t1_res = temp_res_list[i][:-1]
                    q = self.get_massFlow_res()[:-1] * self.cpFluid * t1_res
                    q_lst.append(q)
                return q_lst
            case SimulationMethod.IMPLICIT_EULER:
                q_lst=[]
                for i in range(len(self.storageList)-1):
                    t1_res = temp_res_list[i][1:]
                    q = self.get_massFlow_res()[1:] * self.cpFluid * t1_res
                    q_lst.append(q)
                return q_lst
            case SimulationMethod.CRANK_NICOLSON:
                q_lst=[]
                for i in range(len(self.storageList)-1):
                    t1_res_expl = temp_res_list[i][:-1]
                    q_expl = self.get_massFlow_res()[:-1] * self.cpFluid * t1_res_expl
                    t1_res_impl = temp_res_list[i][1:]
                    q_impl = self.get_massFlow_res()[1:] * self.cpFluid * t1_res_impl
                    q_lst.append((q_expl+q_impl)/2)
                return q_lst
    
    @classmethod
    def newForcedConvection(cls,storageList:list[Storage], massFlow, name=None, cpFluid=CP_Water):
        flow = cls(name)
        flow.cpFluid = cpFluid
        storageList = [x for sub in storageList for x in (sub if isinstance(sub, list) else [sub])]
        if not isinstance(storageList, list):
            raise TypeError("storageList must be a list of ThermalStorage objects")
        if not all(isinstance(storage, Storage) for storage in storageList):
            raise TypeError("All elements in storageList must be instances of Storage")
        flow.storageList = storageList
        flow.__massFlow = massFlow
        return flow
    
    def makeLPObject(self,inputdata:LPInputdata):
        self.lpObject = ForcedConvectionLP(inputdata,self.name,self.storageList,self.get_mFlow(),self.cpFluid)
        return self.lpObject
    
class ForcedConvectionLP(LPObject):
    def __init__(self, inputdata, name,storageList:list[Storage],massFlow:float,cpFluid:float,comment=''):
        super().__init__(inputdata, name, comment)
        self.storageList=storageList
        self.massFlow_on=massFlow
        self.cpFluid=cpFluid
        self.q_lst = []
        self.temp_switch__prod_lst=[]
        self.massFlowSwitch = self.add_time_var(name+'massFlowSwitch',vtype='B')
        for i in range(len(self.storageList)-1):
            self.q_lst.append(self.add_time_var(name+f'_q_{i}_to_{i+1}', lb=-np.inf, ub=np.inf))
            self.temp_switch__prod_lst.append(self.add_time_var(name+f'_tempSwitchProd_{i}_to_{i+1}', lb=-np.inf, ub=np.inf))
            
            self.storageList[i].lpObject.addHeatTransfer(self.q_lst[i],-1)
            self.storageList[i+1].lpObject.addHeatTransfer(self.q_lst[i],1)
            

        
    def def_equations(self):
        # Standard erstmal impliziter Euler? #! TODO
        if True:
            for i in range(len(self.storageList)-1):
                # Product of mass flow switch and temperature of storage i
                stor_temp = self.storageList[i].lpObject.temp
                tm_prod = self.temp_switch__prod_lst[i]
                q = self.q_lst[i]
                self.add_product(self.massFlowSwitch,stor_temp,tm_prod)

                self.add_eq([[q,1],
                             [tm_prod,-self.cpFluid * self.massFlow_on]
                             ])
        self.__def_add_equations()

    def __def_add_equations(self):
        pass

    def set_add_equations(self,func):
        self.__def_add_equations = MethodType(func,self)