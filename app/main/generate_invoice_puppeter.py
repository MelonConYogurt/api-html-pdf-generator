from jinja2 import Template
import subprocess
import datetime
import os


template_invoice = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice</title>
</head>
    <style>
    * {
        box-sizing: border-box;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        -webkit-print-color-adjust: exact; 
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
        -webkit-font-smoothing: antialiased;
        background: rgb(255, 255, 255);
        -webkit-print-color-adjust: exact; 
    }

    h1 {
        font-size: 3.125rem;
        -webkit-print-color-adjust: exact; 
    }

    h2 {
        text-align: center;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: white;
        padding: 30px 0;
        -webkit-print-color-adjust: exact; 
    }

    .text-important {
        font-weight: bold; 
        font-size: 1.2em; 
        color: #333; 
        -webkit-print-color-adjust: exact; 
    }

    .table-wrapper {
        margin: 10px 70px 70px;
        box-shadow: 0px 35px 50px rgba(0, 0, 0, 0.2);
        -webkit-print-color-adjust: exact; 
    }

    .fl-table {
        border-radius: 10px;
        font-size: .75rem;
        font-weight: normal;
        border: none;
        border-collapse: collapse;
        width: 100%;
        max-width: 100%;
        white-space: nowrap;
        background-color: white;
        -webkit-print-color-adjust: exact; 
    }

    .section-info {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        padding-bottom: 1.875rem;
        -webkit-print-color-adjust: exact; 
    }

    .section-info img {
        border-radius: 10px;
        -webkit-print-color-adjust: exact; 
    }

    .section-info-div-izquierda {
        display: flex;
        flex-direction: column;
        gap: 20px;
        -webkit-print-color-adjust: exact; 
    }

    .section-info-div-derecha {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 20px;
        -webkit-print-color-adjust: exact; 
    }

    .fl-table td, .fl-table th {
        text-align: center;
        padding: 8px;
        -webkit-print-color-adjust: exact; 
    }

    .fl-table td {
        border-right: 1px solid #f8f8f8;
        font-size: 12px;
        -webkit-print-color-adjust: exact; 
    }

    .fl-table thead th {
        color: #ffffff;
        background: #363737;
        -webkit-print-color-adjust: exact; 
    }

    .fl-table tr:nth-child(even) {
        background: #F8F8F8;
        -webkit-print-color-adjust: exact; 
    }

</style>
<body>
   <section class="section-info">
        <div class="section-info-div-izquierda">
            <h1>FACTURA</h1>
            <table class="fl-table">
                    <tr>
                        <td>Fecha:</td>
                        <td>{{ total_invoice.date }}</td>
                    </tr>
                    <tr>
                        <td class="text-important">Fecha de vencimiento:</td>
                        <td class="text-important">{{ total_invoice.due_date }}</td>
                    </tr>
                    <tr>
                        <td class="text-important">Total venta:</td>
                        <td class="text-important">{{ total_invoice.total }}</td>
                    </tr>
            </table>
        </div>
        <div class="section-info-div-derecha">
            <img src="{{ total_invoice.company_logo }}" width="200" height="200" alt="Logo">
            <table class="fl-table" >
                <tr>
                    <td>Empresa:</td>
                    <td class="text-important">{{ total_invoice.company_name }}</td>
                </tr>
                <tr>
                    <td>Nombre del vendedor:</td>
                    <td class="text-important">{{ total_invoice.salesperson_name }}</td>
                </tr>
            </table>
        </div>
    </section>
    <table class="fl-table">
        <thead>
            <tr>
                <th>Item</th>
                <th>Serial number</th>
                <th>Units</th>
                <th>Unit price</th>
                <th>Total price</th>
            </tr> 
        </thead>
        <tbody>
            {% for product in products %}
            <tr>
                <td>{{ product.product_name }}</td>
                <td>{{ product.serial_number }}</td>
                <td>{{ product.units }}</td>
                <td>{{ product.price }}</td>
                <td>{{ product.units * product.price }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

def generate(products, client, seller):
    total_invoice = 0
    try:
        # Calcular el total de la factura
        for product in products:
            total_invoice += product.units * product.price
        
        # Crear datos para el invoice
        invoice_data = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "due_date": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "total": f"{total_invoice:.2f}",
            "company_logo": "https://github.com/user-attachments/assets/d715a40f-5e77-4135-b636-d664b59b17b4",
            "company_name": client.company_name,
            "salesperson_name": f"{seller.full_name} ({seller.id_number})"
        }

        # Renderizar la plantilla
        jinja_template = Template(template_invoice)
        rendered_html = jinja_template.render(
            total_invoice=invoice_data,
            products=products,
            client=client,
            seller=seller
        )
        
        directory_html = "generate_templates"
        if not os.path.exists(directory_html):
            os.makedirs(directory_html)

        # Guardar el archivo HTML
        html_file_path = os.path.join(directory_html, f"Factura-{invoice_data['date']}-{invoice_data['company_name']}.html")

        with open(html_file_path, "w", encoding="utf-8") as file:
            file.write(rendered_html)
        
        directory_pdf = "generate_pdf"
        if not os.path.exists(directory_pdf):
            os.makedirs(directory_pdf)

        pdf_file_path = os.path.join(directory_pdf, f"Factura-{invoice_data['date']}-{invoice_data['company_name']}.pdf")
        
        # Ruta del directorio que contiene los archivos
        base_dir = os.path.dirname(__file__)

        # Ruta del archivo puppeteer.js
        puppeteer_path = os.path.join(base_dir, 'puppeteer-script.js')
        
        print(puppeteer_path)

        # Llamar al script de Puppeteer para convertir HTML a PDF
        node_script = puppeteer_path
        subprocess.run(['node', node_script, html_file_path, pdf_file_path], check=True)
            
    except Exception as e:
        print(e)
