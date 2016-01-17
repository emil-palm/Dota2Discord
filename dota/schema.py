from marshmallow import post_load, pre_load
from marshmallow import Schema as MarshmallowSchema
import sys

class Schema(MarshmallowSchema):
    @pre_load(pass_many=True)
    def remove_envelope(self, data, many):
        if many and isinstance(data,list):
            return data
        else:
            if data.get("result"):
                return data.get("result")
            else:
                return data

    @post_load
    def _a_make_instance(self, data):
        if callable(getattr(self.__class__,"_instance",None)):
            return self._instance()(**data)
        else:
            #print(getattr(sys.modules[self.__class__.__module__],self.__class__.__name__.replace('Schema','')))

            return getattr(sys.modules[self.__class__.__module__],self.__class__.__name__.replace('Schema',''))(**data)

