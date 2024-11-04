from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter()

@router.get("/inventory", response_model=list[schemas.InventoryItem])
def read_inventory_items(db: Session = Depends(get_db)):
    try:
        return db.query(models.InventoryItem).all()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al obtener los items del inventario: {str(e)}")

@router.post("/inventory", response_model=schemas.InventoryItem)
def create_inventory_item(item: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    try:
        db_item = models.InventoryItem(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el item en el inventario: {str(e)}")

@router.put("/inventory/{item_id}", response_model=schemas.InventoryItem)
def update_inventory_item(item_id: int, item: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    try:
        db_item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el item del inventario: {str(e)}")

@router.delete("/inventory/{item_id}", response_model=schemas.InventoryItem)
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    try:
        db_item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        db.delete(db_item)
        db.commit()
        return db_item
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el item del inventario: {str(e)}")