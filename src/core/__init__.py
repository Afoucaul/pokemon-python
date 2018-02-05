from importlib import import_module

tileset = import_module("{}.tileset".format(__name__))
picklable = import_module("{}.picklable".format(__name__))
overworld = import_module("{}.overworld".format(__name__))
