from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..schemas import schemas
from ..models import models
from ..database.database import get_db

router = APIRouter()

@router.get("/dashboard", response_model=schemas.Dashboard)
def get_dashboard_data(db: Session = Depends(get_db)):
    try:
        total_customers = db.query(func.count(models.Customer.id)).scalar()
        total_orders = db.query(func.count(models.PurchaseOrder.id)).scalar()
        total_items = db.query(func.count(models.InventoryItem.id)).scalar()
        total_sales = db.query(func.sum(models.PurchaseOrder.price)).scalar()

        return schemas.Dashboard(
            total_customers=total_customers,
            total_orders=total_orders,
            total_items=total_items,
            total_sales=total_sales
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))