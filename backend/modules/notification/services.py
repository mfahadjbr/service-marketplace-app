from sqlmodel import Session, select
from typing import List, Optional
from .models import Notification, NotificationCreate, NotificationSearchParams, NotificationType

def create_notification(session: Session, notification_data: NotificationCreate) -> Notification:
    db_notification = Notification(**notification_data.dict())
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

def get_notification(session: Session, notification_id: int) -> Optional[Notification]:
    statement = select(Notification).where(Notification.id == notification_id)
    return session.exec(statement).first()

def mark_notification_read(session: Session, notification_id: int) -> Optional[Notification]:
    notification = get_notification(session, notification_id)
    if notification:
        notification.is_read = True
        session.add(notification)
        session.commit()
        session.refresh(notification)
    return notification

def delete_notification(session: Session, notification_id: int) -> bool:
    notification = get_notification(session, notification_id)
    if notification:
        session.delete(notification)
        session.commit()
        return True
    return False

def search_notifications(session: Session, params: NotificationSearchParams) -> List[Notification]:
    query = select(Notification)
    if params.user_id:
        query = query.where(Notification.user_id == params.user_id)
    if params.is_read is not None:
        query = query.where(Notification.is_read == params.is_read)
    if params.type:
        query = query.where(Notification.type == params.type)
    return session.exec(query).all()

def get_user_notifications(session: Session, user_id: int, unread_only: bool = False) -> List[Notification]:
    statement = select(Notification).where(Notification.user_id == user_id)
    if unread_only:
        statement = statement.where(Notification.is_read == False)
    return session.exec(statement).all() 