from dataclasses import dataclass, asdict
from typing import Optional, List
from fmconsult.utils.enum import CustomEnum

class MessageType(CustomEnum):
  BUTTON = 'button'
  LIST = 'list'
  POLL = 'poll'
  CAROUSEL = 'carousel'

@dataclass
class Message(object):
  number: str
  text: str
  type: Optional[MessageType] = None
  footerText: Optional[str] = None
  listButtons: Optional[str] = None
  selectableCount: Optional[int] = None
  choices: Optional[List[str]] = None
  imageButton: Optional[str] = None
  linkPreview: Optional[bool] = False
  linkPreviewTitle: Optional[str] = None
  linkPreviewDescription: Optional[str] = None
  linkPreviewImage: Optional[str] = None
  linkPreviewLarge: Optional[str] = None
  replyid: Optional[str] = None
  mentions: Optional[List[str]] = None
  readchat: Optional[bool] = False
  readmessages: Optional[bool] = False
  delay: Optional[int] = 0
  forward: Optional[bool] = False
  track_source: Optional[str] = None
  track_id: Optional[str] = None

  def to_dict(self):
    data = asdict(self)
    return data