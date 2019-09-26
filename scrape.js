const puppeteer = require('puppeteer');

(async () => {
  const url = process.argv[2];
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  page.on('request', (request) => {
    request.continue();
  });
  await page.goto(url, {waitUntil: 'load'});

  const html = await page.content();
  console.log(html);

  browser.close();
})();
