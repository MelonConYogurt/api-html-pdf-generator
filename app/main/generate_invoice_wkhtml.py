from jinja2 import Template
import datetime
import fnmatch
import pdfkit
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
    }
    body {
        font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
        -webkit-font-smoothing: antialiased;
        background: rgb(255, 255, 255);
        margin: 0;
        padding: 0;
    }

    h1 {
        font-size: 3.125rem;
    }

    h2 {
        text-align: center;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: white;
        padding: 30px 0;
    }

    .text-important {
        font-weight: bold; 
        font-size: 1.2em; 
        color: #333; 
    }

    .table-wrapper {
        margin: 10px 70px 70px;
        box-shadow: 0px 35px 50px rgba(0, 0, 0, 0.2);
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
    }

    .fl-table td, .fl-table th {
        text-align: center;
        padding: 8px;
    }

    .fl-table td {
        border-right: 1px solid #f8f8f8;
        font-size: 12px;
    }

    .fl-table thead th {
        color: #ffffff;
        background: #363737;
    }

    .fl-table tr:nth-child(even) {
        background: #F8F8F8;
    }
    
    .section-info{
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        margin: 0 auto;
        width: 100%;
    }
    
    .section-info img{
        border-radius: 10px ;
        float: right;
        margin-bottom: 20px;
    }
    
    .section-info-div-izquierda{
        display: flex;
        flex-direction: column;
    }
    .section-info-div-derecha{
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
    
    .section-info-div-izquierda,
    .section-info-div-derecha {
        width: 30%;
        
    }

    .section-info-div-izquierda {
        float: left;
    }

    .section-info-div-derecha {
        float: right;
        padding-bottom: 50px;
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
            "company_logo": "https://avatars.githubusercontent.com/u/141779507?v=4",
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
        
        path_wkhtmltopdf = r'C:\Users\alejo\Desktop\api_generator\api-generator\ven_entorno_virtual_api_invoice\wkhtmltopdf\bin\wkhtmltopdf.exe'
        
       
        # Configuración de pdfkit
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        
        directory_pdf = "generate_pdf"
        if not os.path.exists(directory_pdf):
            os.makedirs(directory_pdf)

        pdf_file_path = os.path.join(directory_pdf, f"Factura-{invoice_data['date']}-{invoice_data['company_name']}.pdf")
        
        # Convertir HTML a PDF
        pdfkit.from_file(html_file_path, pdf_file_path, configuration=config, options={
            'page-size': 'A4',
            'margin-top': '10mm',
            'margin-right': '10mm',
            'margin-bottom': '10mm',
            'margin-left': '10mm',
        })
    except Exception as e:
        print(e)
