from abc import ABC, abstractmethod
import pandas as pd

def get_nested_attr(obj, attr_path):
    """Greift rekursiv auf verschachtelte Attribute zu, z.B. 'storage1.name'"""
    attrs = attr_path.split(".")
    for attr in attrs:
        obj = getattr(obj, attr)
    return obj

class Component(ABC):
    _series_map = {}
    _counter = 0  # Klassenattribut für Zähler

    def __init__(self, name=None):
        cls = type(self)  # Unterklasse
        if not hasattr(cls, "_counter"):
            cls._counter = 0  # Initialisierung für die Unterklasse
        cls._counter += 1

        if name is None:
            # automatischer Name: Klassenname + Zähler
            self.name = f"{cls.__name__}{cls._counter}"
        else:
            self.name = name
            
    def toPDSeries(self) -> pd.Series:
        # data = {col: getattr(self, attr) for col, attr in self._series_map.items()}
        # return pd.Series(data)
        data = {}
        for col_name, attr_name in self._series_map.items():
            if callable(attr_name):
                # Methode / Lambda aufrufen
                value = attr_name(self)
            else:
                value = get_nested_attr(self, attr_name)

            # Wenn der Wert eine Liste von Objekten ist, die auch ein Attribut 'name' haben
            if isinstance(value, list) and value and all(hasattr(v, "name") for v in value):
                # Wir speichern die Namen der Objekte als Liste
                data[col_name] = [v.name for v in value]
            else:
                data[col_name] = value
        return pd.Series(data)
    # @abstractmethod
    # def updateFromPDSeries(self, pdSeries):
    #     pass
    
class Components:
    def __init__(self,name,items=None):
        self.name=name
        self.items:list[Component]=items or []
        pass
    def __iter__(self):
        return iter(self.items)
    def __len__(self):
        return len(self.items)
    def add_component(self, item:Component):
        if item is not None:
            self.items.append(item)
    def add_components(self, items:list[Component]):
        if items is not None:
            self.items.extend(items)
    def set_simulation_parameter(self,method,stepsize):
        for item in self.items:
            item.set_simulation_parameter(method,stepsize)
    
    def toDataFrame(self) -> pd.DataFrame:
        series_list = [c.toPDSeries() for c in self.items]
        return pd.DataFrame(series_list)