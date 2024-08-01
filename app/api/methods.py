#Modelos de respuesta
from app.api.models import *


# Version only using python
from app.main.generate_invoice_puppeter import *

# with go a error by doing the pdf whit this
# from ven_entorno_virtual_api_invoice.main.generate_invoice_puppeter import *

from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from typing import List
import datetime
import os

app = FastAPI()


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@app.post("/created/invoice/", response_model=InvoiceResponse)
async def invoice_data(products: List[model_product], client: model_client, seller: model_seller):
    try:
        generate(products, client, seller)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        file_name = f"Factura-{date}-{client.company_name}.pdf"
        return InvoiceResponse(
            file_name=file_name,
            products=products,
            client=client,
            seller=seller
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error generating invoice")

    
@app.get("/download_invoice/", response_class= FileResponse)
async def dowload_invoice(file_name:str):
    pdf_directory = "generate_pdf"
    file_path = os.path.join(pdf_directory, file_name)
    
    # Verifica si el archivo existe
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf', filename=file_name)
    else:
        return {"error": "File not found"}