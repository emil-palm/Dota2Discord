from types import MethodType

class ConfigObject(object):
    config_params = {}
    callbacks = []
    def __init__(self, _defaults=None,*args, **kwargs):
        for prefix,data in iter(kwargs.items()):
            if isinstance(data,dict) and prefix is not "__defaults":
                # Lets filter the dict to validate that the options provided are valid
                for k,v in iter(data.items()):
                    if prefix in self.__class__.config_params.keys():
                        if k not in self.__class__.config_params[prefix]:
                            del data[k]

                # Add the _defaults parameter
                __cls__ = None
                if prefix in self.__class__.config_params.keys():
                    if "__cls__" in self.__class__.config_params[prefix]:
                        __cls__ = self.__class__.config_params[prefix]["__cls__"]
                        del(self.__class__.config_params[prefix]["__cls__"])

                    data["__defaults"] = self.__class__.config_params[prefix]
                
                # Now create a config object from it
                configObj = ConfigObject(**data)
                
                # Last attach the config object to the provided class if any
                def register_to_cls(cls,name, configObj):

                    # Now add it as a unbound property to the instance
                    setattr(cls,name, property(lambda self: configObj))
                    # Set it accessible to the class 
                    setattr(cls,name, configObj)
 
                if __cls__:
                    register_to_cls(__cls__,"config", configObj)
                
                register_to_cls(Config().__class__, prefix, configObj)
                    
            else:
                if prefix is not "__defaults":
                    setattr(self, prefix, data)
                    if "__defaults" in kwargs.keys():
                        del(kwargs["__defaults"][prefix])
                    
                
        if "__defaults" in kwargs.keys():
            for key,value in iter(kwargs["__defaults"].items()):
                setattr(self, key, value)

def config(prefix,cls=None,override=False,cb=None):
    def config_wrap(fn):
        config = fn()
        if not isinstance(config,dict):
            raise ValueError("config method isnt returing a dict but: %s" % (type(config).__name__))

        _config_params = getattr(ConfigObject,'config_params')
        _callbacks = getattr(ConfigObject, 'callbacks')
        if prefix in _config_params.keys() and override is False:
            raise ValueError("someone has already registered prefix: %s, careful this can mean your overriding settings from other classes, if this desireable please provide 'override=True' as argument to decorator" % prefix)
        _config_params[prefix] = {}

        if cls is not None:
            _config_params[prefix]['__cls__'] = cls

        if cb:
            _callbacks.append(cb)

        for k,v in iter(config.items()):
            _config_params[prefix][k] = v
    
    return config_wrap

import json,os

_config = None
def Config(cls=None,filename=None):
    global _config
    if _config is None and filename and cls:
        _config = cls(filename)
        _config.read()
        
        for cb in getattr(ConfigObject,'callbacks'):
            cb()

    return _config

class ConfigFile(object):
    def __getattr__(self, key):
        return self.config.__getattribute__(key)

class JSONConfig(ConfigFile):
    def __init__(self, filename):
        self._filename = filename

    def read(self):
        if os.path.isfile(self._filename):
            try:
                with open(self._filename, "r") as input_file:
                    _data = json.load(input_file)
                    self.config = ConfigObject(**_data)
                    
            except Exception as e:
                raise ValueError("Problems reading the provided JSON file")
