import sys
class Model(object):
    def __init__(self,*args,**kwargs):
        for (k,v) in iter(kwargs.items()):
            try:
                setattr(self,k,v)
            except Exception as e:
                print(k,v)
               

    @classmethod
    def schema(cls,*args,**kwargs):
        #x = getattr(sys.modules[cls.__module__],"%sSchema" % (cls.__name__))(*args,**kwargs)
        #print(dir(cls))
        #from pprint import pprint
        #pprint(x._declared_fields)
        #print(dir(x))
        #print(getattr(sys.modules[cls.__module__],"%sSchema" % (cls.__name__)))
        #print(sys.modules[cls.__module__],"%sSchema" % (cls.__name__))
        return getattr(sys.modules[cls.__module__],"%sSchema" % (cls.__name__))(*args,**kwargs)

