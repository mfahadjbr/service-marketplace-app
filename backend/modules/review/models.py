from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class ReviewBase(SQLModel):
    service_id: int = Field(foreign_key="service.id")
    customer_id: int = Field(foreign_key="customerprofile.id")
    provider_id: int = Field(foreign_key="providerprofile.id")
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    is_public: bool = Field(default=True)

class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ReviewCreate(ReviewBase):
    pass

class ReviewRead(ReviewBase):
    id: int
    created_at: datetime
    updated_at: datetime 