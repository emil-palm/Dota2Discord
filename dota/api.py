from dota2py import api
_dotaApi = None
def Api(api_key=None):
    global _dotaApi
    if not _dotaApi and api_key:
        api.set_api_key(api_key)
        return api
    else:
        return api
