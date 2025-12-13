from .connection import Connection,Conduction,ForcedConvection,GeneralHeatTransfer,FreeConvection
from .storage import ExtStorage, ThermalStorage
from .stratifiedStorage import StratifiedStorage
from .component import Component,Components
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
import pandas as pd
from MilPython import LPObject,LPMain,LPInputdata
from types import MethodType

class SimulationMethod(Enum):
    EXPLICIT_EULER = 1
    IMPLICIT_EULER = 2
    CRANK_NICOLSON = 3

def expl_euler(M_old, Q0, b_old,dt):
    M_expl = np.eye(M_old.shape[0]) + M_old * dt
    rhs = M_expl.dot(Q0) + b_old*dt
    Q1_expl = rhs
    return Q1_expl

def impl_euler(M, Q0, b,dt):
    M_impl = np.eye(M.shape[0]) - M * dt
    M_impl_inv = np.linalg.inv(M_impl)
    rhs = Q0 + b*dt
    Q1_impl = M_impl_inv.dot(rhs)
    return Q1_impl

def crank_nicolson(M,M_old, Q0, b,b_old,dt):
    M1 = np.eye(M.shape[0]) - M * dt / 2
    M2 = np.eye(M_old.shape[0]) + M_old * dt / 2
    M_1_inv = np.linalg.inv(M1)
    rhs = M2.dot(Q0) + (b+b_old)*dt/2
    Q1_CN = M_1_inv.dot(rhs)
    return Q1_CN

class ThermalSystem:
    def __init__(self,name):
        self.storages:Components = Components('Thermal Storages')
        self.conductions:Components = Components('Conductions')
        self.forcedConvections:Components = Components('Forced Convections')
        self.freeConvections:Components = Components('Free Convections')
        self.stratfiedStorages:Components = Components('Stratified Storages')
        self.generalHeatTransfers:Components = Components('General Heat Transfers')
        self.ext_storages:Components = Components('External Storages')
        self.__componentsLst=[self.storages,self.conductions,self.forcedConvections,self.freeConvections,self.ext_storages,self.stratfiedStorages,self.generalHeatTransfers]
        self.name = name

    def define_thermal_system(self, storages=None,conductions=None,forcedConvection=None,freeConvection=None,extStorages=None,stratifiedStorages=None,generalHeatTransfers=None,name=None):
        self.storages.add_components(storages)
        self.conductions.add_components(conductions)
        self.forcedConvections.add_components(forcedConvection)
        self.freeConvections.add_components(freeConvection)
        self.ext_storages.add_components(extStorages)
        self.generalHeatTransfers.add_components(generalHeatTransfers)
        if stratifiedStorages is not None:
            for stratifiedStorage in stratifiedStorages:
                self.add_stratifiedStorage(stratifiedStorage)
    
        
    @classmethod
    def newThermalSystem(cls, storages=None,conductions=None,forcedConvection=None,freeConvection=None,extStorages=None,stratifiedStorages=None,generalHeatTransfers=None,name=None):
        system = cls(name)
        system.storages.add_components(storages)
        system.conductions.add_components(conductions)
        system.forcedConvections.add_components(forcedConvection)
        system.freeConvections.add_components(freeConvection)
        system.ext_storages.add_components(extStorages)
        system.generalHeatTransfers.add_components(generalHeatTransfers)
        if stratifiedStorages is not None:
            for stratifiedStorage in stratifiedStorages:
                system.add_stratifiedStorage(stratifiedStorage)
        return system
    
    def add_storage(self, storage: ThermalStorage):
        self.storages.add_component(storage)
    
    def add_conduction(self, conduction: Conduction):
        self.conductions.add_component(conduction)
        
    def add_forcedConvection(self, florcedFlow:ForcedConvection):
        self.forcedConvections.add_component(florcedFlow)
        
    def add_freeConvection(self, freeConvection:FreeConvection):
        self.freeConvections.add_component(freeConvection)
        
    def add_extStorage(self, extStorage: ExtStorage):
        self.ext_storages.add_component(extStorage)
    
    def add_stratifiedStorage(self, stratifiedStorage: StratifiedStorage):
        self.stratfiedStorages.add_component(stratifiedStorage)
        self.storages.add_components(stratifiedStorage.layers)
        self.conductions.add_components(stratifiedStorage.conductions)
        self.conductions.add_components(stratifiedStorage.losses)
        self.freeConvections.add_components(stratifiedStorage.freeConvections)
        self.ext_storages.add_component(stratifiedStorage.surrounding)
        
    def prepare_simulation(self,stepsize,simulation_method=SimulationMethod.CRANK_NICOLSON):
        self.stepsize = stepsize
        self.simulation_method = simulation_method
        
        self.conductions.set_simulation_parameter(simulation_method,self.stepsize)
        self.forcedConvections.set_simulation_parameter(simulation_method,self.stepsize)
        self.freeConvections.set_simulation_parameter(simulation_method,self.stepsize)
        self.generalHeatTransfers.set_simulation_parameter(simulation_method,self.stepsize)
        
        for i,storage in enumerate(self.storages):
            storage.set_col(i)
            storage.sim_prep()
        for ext_storage in self.ext_storages:
            ext_storage.sim_prep()   
        self.dim=len(self.storages)
        self.M=np.zeros((self.dim, self.dim))
        self.b=np.zeros(self.dim)
        self.Q=np.zeros(self.dim)
        
        [self.Q.__setitem__(i, storage.get_Q()) for i, storage in enumerate(self.storages)]
        self.set_therm_storage_Qs(self.Q,0)
        self.__did_simstep()
        self.M_cond = np.zeros((self.dim, self.dim))
        
        for cond in self.conductions:

            if isinstance(cond.storage1,ThermalStorage):
                c1 = cond.coeff / cond.storage1.cap
                self.M_cond[cond.storage1.col, cond.storage1.col] += -c1
                if isinstance(cond.storage2,ThermalStorage):
                    c2 = cond.coeff / cond.storage2.cap
                    self.M_cond[cond.storage1.col, cond.storage2.col] += c2
                    self.M_cond[cond.storage2.col, cond.storage2.col] += -c2
                    self.M_cond[cond.storage2.col, cond.storage1.col] += c1
            else:
                # External storage case
                if isinstance(cond.storage2, ThermalStorage):
                    c2 = cond.coeff / cond.storage2.cap
                    self.M_cond[cond.storage2.col, cond.storage2.col] += -c2
                else:
                    raise TypeError("Conduction must connect two ThermalStorage objects or one ExtStorage and one ThermalStorage")
        self.__get_equations(0,False)
        self.__set_M_b_old()

    def do_simstep(self):
        self.__sim_step(t=None)
    
    def simulate(self,num_steps=1000,stepsize=1/60,simulation_method=SimulationMethod.CRANK_NICOLSON):
        self.num_steps=num_steps
        self.stepsize=stepsize#! stepsize als timedelta?
        self.simulation_method = simulation_method
        self.__sim_prep()
        for t in range(1,self.num_steps+1):
            self.__sim_step(t)
    
    def __sim_prep(self): #TODO ist das gleiche wie simulation_preparation()?
        
        self.conductions.set_simulation_parameter(self.simulation_method,self.stepsize)
        self.forcedConvections.set_simulation_parameter(self.simulation_method,self.stepsize)
        self.freeConvections.set_simulation_parameter(self.simulation_method,self.stepsize)
        self.generalHeatTransfers.set_simulation_parameter(self.simulation_method,self.stepsize)
        
        for i,storage in enumerate(self.storages):
            storage.set_col(i)
            storage.sim_prep(num_steps=self.num_steps)
        for ext_storage in self.ext_storages:
            ext_storage.sim_prep(num_steps=self.num_steps)   
        self.dim=len(self.storages)
        self.M=np.zeros((self.dim, self.dim))
        self.b=np.zeros(self.dim)
        self.Q=np.zeros(self.dim)
        
        [self.Q.__setitem__(i, storage.get_Q()) for i, storage in enumerate(self.storages)]
        self.set_therm_storage_Qs(self.Q,0)
        self.__did_simstep()
        self.M_cond = np.zeros((self.dim, self.dim))
        
        for cond in self.conductions:

            if isinstance(cond.storage1,ThermalStorage):
                c1 = cond.coeff / cond.storage1.cap
                self.M_cond[cond.storage1.col, cond.storage1.col] += -c1
                if isinstance(cond.storage2,ThermalStorage):
                    c2 = cond.coeff / cond.storage2.cap
                    self.M_cond[cond.storage1.col, cond.storage2.col] += c2
                    self.M_cond[cond.storage2.col, cond.storage2.col] += -c2
                    self.M_cond[cond.storage2.col, cond.storage1.col] += c1
            else:
                # External storage case
                if isinstance(cond.storage2, ThermalStorage):
                    c2 = cond.coeff / cond.storage2.cap
                    self.M_cond[cond.storage2.col, cond.storage2.col] += -c2
                else:
                    raise TypeError("Conduction must connect two ThermalStorage objects or one ExtStorage and one ThermalStorage")
        self.__get_equations(0,False)
        self.__set_M_b_old()
        
    def sim_step_control(self,t):
        pass
    
    def __sim_step(self,t):
        
        self.sim_step_control(t)
        self.__get_equations(t)

        self.M = self.M_forcedConvection+self.M_cond+self.M_generalHeatTransfer + self.M_freeConvection
        self.b = self.b_forcedConvection+self.b_cond+self.b_generalHeatTransfer

        match self.simulation_method:
            case SimulationMethod.EXPLICIT_EULER:
                self.Q = expl_euler(self.M_old,self.Q,self.b_old,self.stepsize)
            case SimulationMethod.IMPLICIT_EULER:
                self.Q = impl_euler(self.M,self.Q,self.b,self.stepsize)
            case SimulationMethod.CRANK_NICOLSON:
                self.Q = crank_nicolson(self.M,self.M_old, self.Q, self.b,self.b_old, self.stepsize) 
                
        self.__did_simstep()
        self.set_therm_storage_Qs(self.Q,t)

    def __get_equations(self,t,isSimStep=True):
        self.__get_conduction_equations()
        self.__get_generalHeatTransfer_equations(t)
        self.__get_freeConvection_equations()
        if isSimStep:
            self.__get_forcedConvection_equations(t)
        else:
            self.__get_forcedConvection_equations(t,False)

    def __get_conduction_equations(self):
        self.b_cond = np.zeros(self.dim)
        
        for cond in self.conductions:
            if isinstance(cond.storage1,ExtStorage):
                c = cond.coeff * cond.storage1.get_temp()
                self.b_cond[cond.storage2.col] += c
            elif isinstance(cond.storage2,ExtStorage):
                c = cond.coeff * cond.storage2.get_temp()
                self.b_cond[cond.storage1.col] += c

        return self.b_cond
    
    def __get_generalHeatTransfer_equations(self,t):
        self.M_generalHeatTransfer = np.zeros((self.dim, self.dim))
        self.b_generalHeatTransfer = np.zeros(self.dim)
        for ht in self.generalHeatTransfers:
            targetStorage = ht.targestStorage
            if isinstance(ht.b,list):
                coeff = ht.b[t]
            else:
                coeff = ht.b
            self.b_generalHeatTransfer[targetStorage.col] += coeff

    def __get_freeConvection_equations(self):
                # Free Convection
        self.M_freeConvection = np.zeros((self.dim, self.dim))
        for conv in self.freeConvections:
            if conv.storage1.get_temp() > conv.storage2.get_temp() + conv.tolerance:
                c1 = conv.get_mFlow() / conv.storage1.cap * conv.cpFluid
                c2 = conv.get_mFlow() / conv.storage2.cap * conv.cpFluid
                self.M_freeConvection[conv.storage1.col,conv.storage1.col] += -c1
                self.M_freeConvection[conv.storage1.col,conv.storage2.col] += c2
                self.M_freeConvection[conv.storage2.col,conv.storage1.col] += c2
                self.M_freeConvection[conv.storage2.col,conv.storage2.col] += -c2            
    
    def __get_forcedConvection_equations(self,t,isSimStep=True):
        self.M_forcedConvection = np.zeros((self.dim, self.dim))
        self.b_forcedConvection = np.zeros(self.dim)
        for conv in self.forcedConvections:
            mFlow = conv.get_mFlow()
            if mFlow is None:
                raise ValueError("mFlow must be set for ForcedFlow")
            
            for i in range(len(conv.storageList)-1):
                from_stor = conv.storageList[i]
                to_stor = conv.storageList[i+1]
                if isinstance(from_stor,ExtStorage):
                    coeff = mFlow * from_stor.get_temp() * conv.cpFluid
                    self.b_forcedConvection[to_stor.col] += coeff
                    if isSimStep: from_stor.add_q(-coeff, t)
                else:
                    coeff = mFlow / from_stor.cap * conv.cpFluid
                    self.M_forcedConvection[from_stor.col, from_stor.col] += -coeff
                    if isinstance(to_stor,ExtStorage):
                        if isSimStep: to_stor.add_q(coeff, t)#! das hier ist falsch: q_from fehlt
                    else:
                        self.M_forcedConvection[to_stor.col, from_stor.col] += coeff 
    
    
    def __did_simstep(self):
        self.__set_M_b_old()
        for ext_storage in self.ext_storages:
            ext_storage.save_temp()
        for forcedConv in self.forcedConvections:
            forcedConv.save_massFlow()
        for freeConv in self.freeConvections:
            freeConv.save_massFlow()
        for ght in self.generalHeatTransfers:
            ght.save_b()
    
    def __set_M_b_old(self):
        self.M_old = self.M.copy()
        self.b_old = self.b.copy()

    def set_therm_storage_Qs(self, Q,t):
        for i, storage in enumerate(self.storages):
            storage.set_Q(Q[i],t)
               
    def to_Excel(self, filename):
        # Placeholder for exporting to Excel logic
        with pd.ExcelWriter(filename) as writer:
            for comp in self.__componentsLst:
                sheet_name = comp.name if comp.name else 'Component'
                comp.toDataFrame().to_excel(writer, sheet_name=sheet_name, index=False)
    
    def plot_temps(self,storage_list:list[ThermalStorage],color_list:list[str]=None,xLabel='Steps',yLabel='Temp in °C'):
        _,ax = plt.subplots()
        for i,stor in enumerate(storage_list):
            if color_list:
                stor.plot_temp_res(ax,color_list[i])
            else:
                stor.plot_temp_res(ax)
        ax.legend()
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.show()

    def plot_heatflow(self,connection_list:list[Connection],color_list:list[str]=None,xLabel='Steps',yLabel='Flux in W'):
        _,ax = plt.subplots()
        for i,con in enumerate(connection_list):
            if color_list:
                con.plot_heatflow_res(ax,color_list[i])
            else:
                con.plot_heatflow_res(ax)
        ax.legend()
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.show()
                
    @classmethod
    def from_Excel(cls, filename):
        xls = pd.ExcelFile(filename)
        system = cls(filename)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            match sheet_name:
                case 'Thermal Storages':
                    storages = [ThermalStorage.fromPDSeries(row) for _, row in df.iterrows()]
                    system.storages.add_components(storages)
                case 'External Storages':
                    extStor = [ExtStorage.fromPDSeries(row) for _, row in df.iterrows()]
                    system.ext_storages.add_components(extStor)
                case _:
                    pass
                
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            match sheet_name:
                case 'Conductions':
                    conds=[]
                    for _,row in df.iterrows():
                        storage1 = next((st for st in system.storages.items if st.name==row['Storage1']),None)
                        if storage1 is None:
                            storage1 = next((st for st in system.ext_storages.items if st.name==row['Storage1']),None)
                        if storage1 is None:
                            raise ValueError(f"Can not find Storage1: {row['Storage1']} of {row['Name']} in {sheet_name}. Check if storage exists.")
                        
                        storage2 = next((st for st in system.storages.items if st.name==row['Storage2']),None)
                        if storage2 is None:
                            storage2 = next((st for st in system.ext_storages.items if st.name==row['Storage2']),None)
                        if storage2 is None:
                            raise ValueError(f"Can not find Storage2: {row['Storage2']} of {row['Name']} in {sheet_name}. Check if storage exists.")
                        conds.append(Conduction(storage1,storage2,row['Coeff'],row['Name']))
                    system.conductions.add_components(conds)
                case 'Forced Convections':
                    forcedConv=[]
                    for _,row in df.iterrows():
                        stors=[]
                        for storage in eval(row['StorageList']):
                            stor = next((st for st in system.storages.items if st.name==storage),None)
                            if stor is None:
                                stor = next((st for st in system.ext_storages.items if st.name==storage),None)
                            if stor is None:
                                raise ValueError(f"Can not find storage: {storage} of {row['Name']} in {sheet_name}. Check if storage exists.")
                            stors.append(stor)
                        forcedConv.append(ForcedConvection.newForcedConvection(stors,row['MassFlow'],row['Name'],row['CpFluid']))
                    system.forcedConvections.add_components(forcedConv)
                case 'Free Convections':
                    freeConvs=[]
                    for _,row in df.iterrows():
                        storage1 = next((st for st in system.storages.items if st.name==row['Storage1']),None)
                        if storage1 is None:
                            storage1 = next((st for st in system.ext_storages.items if st.name==row['Storage1']),None)
                        if storage1 is None:
                            raise ValueError(f"Can not find Storage1: {row['Storage1']} of {row['Name']} in {sheet_name}. Check if storage exists.")
                        
                        storage2 = next((st for st in system.storages.items if st.name==row['Storage2']),None)
                        if storage2 is None:
                            storage2 = next((st for st in system.ext_storages.items if st.name==row['Storage2']),None)
                        if storage2 is None:
                            raise ValueError(f"Can not find Storage2: {row['Storage2']} of {row['Name']} in {sheet_name}. Check if storage exists.")
                        freeConvs.append(FreeConvection.newFreeConvection(storage1,storage2,row['MassFlow'],row['CpFluid'],row['Tolerance'],row['Name']))
                    system.freeConvections.add_components(freeConvs)
                case 'General Heat Transfers':
                    raise NotImplementedError('This method is not yet implemented for General Heat Transfer') #TODO
                case _:
                    raise ValueError('An unknown type of heat transfer was selected')
            return system
        
    def makeLPSystem(self,lpInputdata):
        self.lpInputdata = lpInputdata
        self.lpTherm = LPThermSys(self.lpInputdata,self.name)

        for storage in self.storages.items:
            setattr(self.lpTherm,storage.name,storage.makeLPObject(self.lpInputdata))
        for ext_storage in self.ext_storages.items:
            setattr(self.lpTherm,ext_storage.name,ext_storage.makeLPObject(self.lpInputdata))
        for cond in self.conductions.items:
            setattr(self.lpTherm,cond.name,cond.makeLPObject(self.lpInputdata))
        for forcedConv in self.forcedConvections.items:
            setattr(self.lpTherm,forcedConv.name,forcedConv.makeLPObject(self.lpInputdata))
        for genht in self.generalHeatTransfers.items:
            setattr(self.lpTherm,genht.name,genht.makeLPObject(self.lpInputdata))


class LPThermSys(LPMain,LPObject):
    def __init__(self, inputdata, name='Thermal System', comment=''):
        LPObject.__init__(self,inputdata,name,comment)
        LPMain.__init__(self,inputdata)
    @classmethod
    def set_targetfun(cls,targetfun):
        cls.def_targetfun = targetfun

    def def_equations(self):
        self.__def_add_equations()

    def __def_add_equations(self):
        pass

    def set_add_equations(self,func):
        self.__def_add_equations = MethodType(func,self)        
            