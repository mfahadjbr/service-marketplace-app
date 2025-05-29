from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    BOOKING = "booking"
    MESSAGE = "message"
    SYSTEM = "system"
    PROMOTION = "promotion"

class NotificationBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    type: NotificationType
    title: str
    message: str
    is_read: bool = Field(default=False)

class Notification(NotificationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class NotificationCreate(NotificationBase):
    pass

class NotificationRead(NotificationBase):
    id: int
    created_at: datetime
    updated_at: datetime

class NotificationSearchParams(SQLModel):
    user_id: Optional[int] = None
    is_read: Optional[bool] = None
    type: Optional[NotificationType] = None 