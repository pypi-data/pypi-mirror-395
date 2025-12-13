import logging, jsonpickle
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from uazapi.api import UazapiApi
from uazapi.dtos.message import Message

class MessageChannel(UazapiApi):

  def send_text_message(self, data: Message):
    logging.info(f'sending SMS text message...')
    try:
      url = UrlUtil().make_url(self.base_url, ['send', 'text'])
      res = self.call_request(
        http_method=HTTPMethod.POST, 
        request_url=url, 
        payload=data.to_dict()
      )
      return jsonpickle.decode(res)
    except:
      raise