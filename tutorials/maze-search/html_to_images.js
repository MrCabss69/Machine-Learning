const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Función para añadir ceros a la izquierda
function padWithZeros(number, length) {
    let numStr = String(number);
    while (numStr.length < length) {
        numStr = '0' + numStr;
    }
    return numStr;
}

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    const dirPath = path.join(__dirname, 'frames');
    const files = fs.readdirSync(dirPath);
    const htmlFiles = files.filter(file => path.extname(file).toLowerCase() === '.html');

    for (const file of htmlFiles) {
        const filePath = `file://${path.join(dirPath, file)}`;
        await page.goto(filePath, { waitUntil: 'networkidle0' });

        // Extrae el número del nombre del archivo
        const match = file.match(/\d+/); // Encuentra la secuencia de dígitos en el nombre del archivo
        const number = match ? parseInt(match[0], 10) : 0; // Convierte la secuencia de dígitos a un número entero
        const paddedNumber = padWithZeros(number, 3); // Añade el padding de ceros a la izquierda, ajusta la longitud según necesites

        // Construye el nombre del archivo de salida con el número formateado
        const screenshotPath = path.join(__dirname, 'temp_images', `capture_dijkstra_${paddedNumber}.png`);
        await page.screenshot({ path: screenshotPath, fullPage: true });
    }

    await browser.close();
})();
