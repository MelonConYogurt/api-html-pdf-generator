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
