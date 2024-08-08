## Generador de PDFs

Este proyecto incluye un generador de PDFs que permite crear facturas en formato PDF a partir de datos proporcionados. Puedes ver un ejemplo de factura generada a continuación.

### [Descargar PDF](https://github.com/user-attachments/files/16464937/Factura-2024-08-01-Tech.Solutions.S.A.pdf)

El enlace anterior te llevará a un ejemplo de factura generada por el sistema.

<h3>script puppeteer:</h3>

```
const puppeteer = require('puppeteer');
const fs = require('fs');

const [,, htmlPath, pdfPath] = process.argv;

(async () => {
  try {
    const browser = await puppeteer.launch(
      {args: ['--no-sandbox', '--disable-setuid-sandbox']}
    );
    const page = await browser.newPage();
    const htmlContent = fs.readFileSync(htmlPath, 'utf8');
    
    // Establecer el contenido de la página
    await page.setContent(htmlContent);

    // Generar el PDF
    await page.pdf({ path: pdfPath, format: 'A4' });
    
    await browser.close();
    console.log('PDF generado exitosamente');
  } catch (error) {
    console.error('Error al generar PDF:', error);
  }
})();

```
<img src="https://github.com/user-attachments/assets/f576d4bf-53f1-4b53-ae2b-4728d5e1be08" width="0px" height="0px">
<img src="https://github.com/user-attachments/assets/d715a40f-5e77-4135-b636-d664b59b17b4" width="0px" height="0px">
<img src="https://github.com/user-attachments/assets/f1b448e4-0c8f-4eb9-af67-2ffad6015a2d" width="0px" height="0px">
<h1>PDF de prueba con 20 items:</h1>

<img src="https://github.com/user-attachments/assets/27a64d9d-4f4e-40ed-bde7-260f96ccce92" alt="Factura_pruebas"  />
<hr>
<img src="https://github.com/user-attachments/assets/64fcff39-bfa3-447a-ac95-45c50b56e72f" alt="Factura_pruebas"  />



