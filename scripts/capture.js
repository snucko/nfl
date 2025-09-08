const fs = require('fs');
const path = require('path');
const { launch } = require('puppeteer-core');

function guessChromiumPath() {
  const c = ['/usr/bin/chromium-browser','/usr/bin/chromium','/snap/bin/chromium'];
  for (const p of c) { try { fs.accessSync(p, fs.constants.X_OK); return p; } catch {} }
  throw new Error('Chromium not found');
}
function ts() {
  const d = new Date(), z = n => String(n).padStart(2,'0');
  return `${d.getFullYear()}${z(d.getMonth()+1)}${z(d.getDate())}${z(d.getHours())}${z(d.getMinutes())}${z(d.getSeconds())}`;
}
async function snap(url, width, height, dest) {
  const browser = await launch({
    executablePath: guessChromiumPath(),
    headless: true,
    args: ['--no-sandbox','--disable-gpu','--disable-dev-shm-usage',`--window-size=${width},${height}`],
    defaultViewport: { width, height, deviceScaleFactor: 2 }
  });
  try {
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
    try { await page.waitForSelector('.title_bar, table.table', { timeout: 15000 }); } catch {}
    await page.screenshot({ path: dest, fullPage: false });
  } finally {
    await browser.close();
  }
  console.log('[ok] screenshot ->', dest);
}

(async () => {
  const url = process.env.TRMNLP_URL || 'http://localhost:4567/full';
  const outDir = path.resolve(__dirname, '..', 'screenshots');
  fs.mkdirSync(outDir, { recursive: true });

  const stamp = ts();
  const small = path.join(outDir, `trmnl-${stamp}.png`);
  const large = path.join(outDir, `trmnl-${stamp}-hires.png`);

  await snap(url, 800, 480, small);
  await snap(url, 1600, 960, large);

  fs.copyFileSync(small, path.join(outDir, 'latest.png'));
  fs.copyFileSync(large, path.join(outDir, 'latest-hires.png'));
  console.log('[ok] latest ->', path.join(outDir, 'latest.png'));
  console.log('[ok] latest-hires ->', path.join(outDir, 'latest-hires.png'));
})();

