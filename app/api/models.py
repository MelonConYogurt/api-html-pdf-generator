from pydantic import BaseModel
from typing import List

class model_product(BaseModel):
    serial_number: int
    product_name : str
    units: int
    price: float 
    description: str

class model_client(BaseModel):
    full_name:str
    email:str
    celphone_number: int
    nit_company: int
    company_name: str
    
class model_seller(BaseModel):
    full_name:str
    id_number: int 
    
class InvoiceResponse(BaseModel):
    file_name: str
    products: List[model_product]
    client: model_client
    seller: model_seller