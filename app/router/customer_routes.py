from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter()

@router.get("/customers", response_model=list[schemas.Customer])
def read_customers(db: Session = Depends(get_db)):
    try:
        return db.query(models.Customer).all()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al obtener los clientes: {str(e)}")

@router.post("/customers", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    try:
        db_customer = models.Customer(**customer.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el cliente: {str(e)}")

@router.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    try:
        db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if db_customer is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        for key, value in customer.dict().items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el cliente: {str(e)}")

@router.delete("/customers/{customer_id}", response_model=schemas.Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    try:
        db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if db_customer is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        db.delete(db_customer)
        db.commit()
        return db_customer
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el cliente: {str(e)}")
