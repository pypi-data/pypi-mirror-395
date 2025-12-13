import calendar
import datetime
import inspect
import time
import humps

class ComplyCubeObject(object):

    def __init__(self, *args, **params):
        self.from_dict(params)

    def from_dict(self, a_dict):
        for attribute, value in list(a_dict.items()):
            if humps.decamelize(attribute) == "metadata" and isinstance(value, dict):
                setattr(self, humps.decamelize(attribute), value)
                continue
            if type(value) is dict:
                setattr(self, humps.decamelize(attribute), ComplyCubeObject(**value))
                continue
            if type(value) is list:
                setattr(self, humps.decamelize(attribute),[(ComplyCubeObject(**item) if type(item) is dict else item) for item in value])
                continue
            setattr(self, humps.decamelize(attribute), value)   
        return self

    def to_dict(self):
        a_dict = {}
        for name in list(self.__dict__.keys()):
            current_item = self.__dict__[name]
            if issubclass(type(current_item),ComplyCubeObject):
                a_dict[humps.camelize(name)] = current_item.to_dict()
                continue
            if type(current_item) is list:
                a_dict[humps.camelize(name)] = [item.to_dict() if is_sub(item) else item for item in current_item]
                continue
            a_dict[humps.camelize(name)] = current_item
        return a_dict

    def __str__(self):
        return self.to_dict().__str__()


def is_sub(obj):
    return issubclass(type(obj),ComplyCubeObject)