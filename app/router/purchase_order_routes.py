from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter()

@router.get("/purchase-orders", response_model=list[schemas.PurchaseOrder])
def read_purchase_orders(db: Session = Depends(get_db)):
    try:
        return db.query(models.PurchaseOrder).all()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al obtener las órdenes de compra: {str(e)}")

@router.post("/purchase-orders", response_model=schemas.PurchaseOrder)
def create_purchase_order(order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    try:
        db_order = models.PurchaseOrder(**order.dict())
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la orden de compra: {str(e)}")

@router.put("/purchase-orders/{order_id}", response_model=schemas.PurchaseOrder)
def update_purchase_order(order_id: int, order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    try:
        db_order = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == order_id).first()
        if db_order is None:
            raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
        for key, value in order.dict().items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
        return db_order
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar la orden de compra: {str(e)}")

@router.delete("/purchase-orders/{order_id}", response_model=schemas.PurchaseOrder)
def delete_purchase_order(order_id: int, db: Session = Depends(get_db)):
    try:
        db_order = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == order_id).first()
        if db_order is None:
            raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
        db.delete(db_order)
        db.commit()
        return db_order
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar la orden de compra: {str(e)}")
