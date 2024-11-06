from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

class UsuarioLogin(BaseModel):
    email: str
    password: str
    
class InventoryItemBase(BaseModel):
    name: str
    quantity: int
    price: float

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItem(InventoryItemBase):
    id: int

    class Config:
        orm_mode = True
        
class PurchaseOrderBase(BaseModel):
    item_name: str
    quantity: int 
    price: float

class PurchaseOrderCreate(PurchaseOrderBase):
    pass

class PurchaseOrder(PurchaseOrderBase):
    id: int

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True
