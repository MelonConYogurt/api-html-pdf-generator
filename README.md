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



<h1>PDF de prueba con 20 items:</h1>

<img src="https://github.com/user-attachments/assets/d557b6cb-5ae2-4348-9d5a-5c78b16cbbd9" alt="Factura_pruebas" />

