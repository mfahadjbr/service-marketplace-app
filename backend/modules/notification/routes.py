from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from ..auth.services import get_current_user
from ..auth.models import User
from ..database import get_session
from .models import Notification, NotificationCreate, NotificationRead, NotificationSearchParams, NotificationType
from .services import (
    create_notification,
    get_notification,
    mark_notification_read,
    delete_notification,
    search_notifications,
    get_user_notifications
)

router = APIRouter()

@router.post("/", response_model=NotificationRead)
def create_notification_endpoint(
    notification_data: NotificationCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Only admins or system can create notifications for others
    if current_user.role not in ["admin", "system"] and notification_data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create notification for this user")
    return create_notification(session, notification_data)

@router.get("/", response_model=List[NotificationRead])
def get_my_notifications_endpoint(
    unread_only: bool = Query(False),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_user_notifications(session, current_user.id, unread_only)

@router.get("/search/", response_model=List[NotificationRead])
def search_notifications_endpoint(
    user_id: Optional[int] = None,
    is_read: Optional[bool] = None,
    type: Optional[NotificationType] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Only admins can search for other users' notifications
    if user_id and user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to search notifications for this user")
    params = NotificationSearchParams(user_id=user_id, is_read=is_read, type=type)
    return search_notifications(session, params)

@router.get("/{notification_id}", response_model=NotificationRead)
def get_notification_endpoint(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    notification = get_notification(session, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this notification")
    return notification

@router.post("/{notification_id}/read", response_model=NotificationRead)
def mark_notification_read_endpoint(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    notification = get_notification(session, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to mark this notification as read")
    return mark_notification_read(session, notification_id)

@router.delete("/{notification_id}")
def delete_notification_endpoint(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    notification = get_notification(session, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this notification")
    if delete_notification(session, notification_id):
        return {"message": "Notification deleted successfully"}
    raise HTTPException(status_code=500, detail="Failed to delete notification") 