from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
import uvicorn
# Import routers from modules
from modules.auth.routes import router as auth_router
from modules.provider.routes import router as provider_router
from modules.customer.routes import router as customer_router
from modules.service.routes import router as service_router
from modules.booking.routes import router as booking_router
from modules.category.routes import router as category_router
from modules.location.routes import router as location_router
from modules.notification.routes import router as notification_router
from modules.analytics.routes import router as analytics_router
from modules.review.routes import router as review_router

app = FastAPI(title="Service Marketplace API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(provider_router, prefix="/providers", tags=["Providers"])
app.include_router(customer_router, prefix="/customers", tags=["Customers"])
app.include_router(service_router, prefix="/services", tags=["Services"])
app.include_router(booking_router, prefix="/bookings", tags=["Bookings"])
app.include_router(category_router, prefix="/categories", tags=["Categories"])
app.include_router(location_router, prefix="/locations", tags=["Locations"])
app.include_router(notification_router, prefix="/notifications", tags=["Notifications"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(review_router, prefix="/reviews", tags=["Reviews"]) 

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)