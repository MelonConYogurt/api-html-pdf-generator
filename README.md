---

# Generador de Facturas API

Esta API permite generar facturas en formato PDF a partir de datos proporcionados en formato JSON. Utiliza FastAPI para gestionar las peticiones y Puppeteer para convertir plantillas HTML a PDF.

## Estructura del Proyecto

- **`api`**: Contiene los modelos y la API de FastAPI.
- **`main`**: Incluye la lógica para generar la factura en formato HTML y convertirla a PDF utilizando Puppeteer.
- **`script`**: Archivo JavaScript que utiliza Puppeteer para convertir HTML a PDF.

## Modelos de Datos

Los modelos de datos se definen utilizando Pydantic y se utilizan para validar las solicitudes de entrada y las respuestas de la API.

```python
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
```

## API Endpoints

### Root Endpoint

- **GET `/`**
  - Redirige a la documentación de la API.

### Crear Factura

- **POST `/created/invoice/`**
  - **Descripción**: Genera una factura en formato PDF.
  - **Cuerpo de la Solicitud**: 
    ```json
    {
      "products": [
        {
          "serial_number": 1,
          "product_name": "Example Product",
          "units": 10,
          "price": 20.0,
          "description": "Product Description"
        }
      ],
      "client": {
        "full_name": "Client Name",
        "email": "client@example.com",
        "celphone_number": 1234567890,
        "nit_company": 123456789,
        "company_name": "Client Company"
      },
      "seller": {
        "full_name": "Seller Name",
        "id_number": 987654321
      }
    }
    ```
  - **Respuesta**: 
    ```json
    {
      "file_name": "Factura-YYYY-MM-DD-Client Company.pdf",
      "products": [...],
      "client": {...},
      "seller": {...}
    }
    ```
  - **Errores**: 500 - Error al generar la factura.

### Descargar Factura

- **GET `/download_invoice/`**
  - **Parámetros de Consulta**: `file_name` (nombre del archivo PDF).
  - **Descripción**: Descarga el archivo PDF generado.
  - **Respuesta**: Archivo PDF.
  - **Errores**: 404 - Archivo no encontrado.

## Generación de la Factura

1. **Renderización HTML**: Utiliza una plantilla Jinja2 para generar el HTML de la factura.
2. **Conversión a PDF**: Utiliza Puppeteer para convertir el HTML a PDF.

### `main.py`

```python
from jinja2 import Template
import subprocess
import datetime
import os

template_invoice = """
<!DOCTYPE html>...
"""

def generate(products, client, seller):
    ...
    # Lógica para calcular el total, renderizar el HTML y llamar a Puppeteer
    ...
```

### `puppeteer-script.js`

```javascript
const puppeteer = require('puppeteer');
const fs = require('fs');

const [,, htmlPath, pdfPath] = process.argv;

(async () => {
  ...
})();
```

## Requisitos

- Python 3.7 o superior
- Node.js
- Puppeteer
- FastAPI
- Jinja2

## Instalación

1. **Instalar dependencias**:
   ```bash
   pip install fastapi uvicorn jinja2 pydantic
   npm install puppeteer
   ```

2. **Ejecutar la API**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. **Ejecutar el script de Puppeteer**:
   Asegúrate de que el script `puppeteer-script.js` esté en la ruta correcta y usa el comando:
   ```bash
   node puppeteer-script.js <html_path> <pdf_path>
   ```

---

¡Espero que esto te sea útil! Si necesitas hacer algún ajuste o agregar más detalles, no dudes en decírmelo.


<img src="https://github.com/user-attachments/assets/f576d4bf-53f1-4b53-ae2b-4728d5e1be08" width="0px" height="0px">
<img src="https://github.com/user-attachments/assets/d715a40f-5e77-4135-b636-d664b59b17b4" width="0px" height="0px">
<img src="https://github.com/user-attachments/assets/f1b448e4-0c8f-4eb9-af67-2ffad6015a2d" width="0px" height="0px">
<h1>Los PDF generados se ven tal que asi:</h1>

<img src="https://github.com/user-attachments/assets/27a64d9d-4f4e-40ed-bde7-260f96ccce92" alt="Factura_pruebas"  />
<hr>
<img src="https://github.com/user-attachments/assets/64fcff39-bfa3-447a-ac95-45c50b56e72f" alt="Factura_pruebas"  />



