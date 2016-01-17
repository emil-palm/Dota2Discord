class Steamid(object):
    def __init__(self,*args,**kwargs):
        for (k,v) in iter(kwargs.items()):
            setattr(self,k,v)

 

    def _convert(self):
        if len(self.steamid) == 17:
            return int(self.steamid[3:]) - 61197960265728
        else:
            return '765' + str(self.steamid + 61197960265728)


    def id32(self):
        if len(self.steamid) == 17:
            return self._convert()
        else:
            return self.steamid
    
    def id64(self):
        if len(self.steamid) == 17:
            return self.steamid
        else:
            return self._convert()
