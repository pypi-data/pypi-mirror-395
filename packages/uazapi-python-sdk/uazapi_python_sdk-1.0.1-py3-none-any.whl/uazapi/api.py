import os
from fmconsult.http.api import ApiBase

class UazapiApi(ApiBase):

  def __init__(self):
    try:
      self.api_token = os.environ['uazapi.api.token']
      self.base_url = os.environ['uazapi.api.url']
      self.headers = {
        'token': self.api_token
      }
    except:
      raise