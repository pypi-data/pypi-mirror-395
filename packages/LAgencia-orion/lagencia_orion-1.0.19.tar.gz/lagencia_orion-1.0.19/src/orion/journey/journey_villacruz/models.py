from typing import List, Optional

from pydantic import BaseModel


class AddData(BaseModel):
    customer_name: Optional[str]
    customer_phone: Optional[str]
    adviser_name: Optional[str]
    adviser_phone: Optional[str]


class RequestToSendNotifications(BaseModel):
    phone: str
    code: Optional[str] = None
    token: Optional[str] = None
    price: Optional[int] = None
    old_price: Optional[int] = None
    week: Optional[int] = None
    option: Optional[str] = None
    recipients: Optional[List[str]] = None
    add_data: Optional[AddData]= None
