from complycube.model import ComplyCubeObject

class ComplyCubeCollection(ComplyCubeObject):

    def __iter__(self):
        return getattr(self, "items", []).__iter__()

    def __len__(self):
        return getattr(self, "items", []).__len__()

    def __reversed__(self):
        return getattr(self, "items", []).__reversed__()

