const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    headless: 'new',
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 844 });
  await page.goto('https://sseohyunbum-ops.github.io/smoke-finder/index.html?demo=37.5533,126.97', { waitUntil: 'networkidle2', timeout: 40000 }).catch(()=>{});
  await new Promise(r => setTimeout(r, 11000));
  const s1 = await page.evaluate(() => ({
    chipShown: document.getElementById('listChip').classList.contains('show'),
    chipText: document.getElementById('listChip').textContent,
    sheetOpen: document.querySelector('aside').classList.contains('show'),
    mapH: Math.round(document.getElementById('mapWrap').getBoundingClientRect().height),
    cards: document.querySelectorAll('.card').length,
  }));
  await page.screenshot({ path: '../../ui1.png' });
  // 칩 탭 → 시트 열림
  await page.click('#listChip');
  await new Promise(r => setTimeout(r, 600));
  const s2 = await page.evaluate(() => document.querySelector('aside').classList.contains('show'));
  await page.screenshot({ path: '../../ui2.png' });
  // 닫기 → 마커(핀) 클릭 → 시트 다시 열림
  await page.click('#listClose');
  await new Promise(r => setTimeout(r, 500));
  const s3 = await page.evaluate(() => {
    const pin = document.querySelector('.pin');
    if (pin) pin.dispatchEvent(new MouseEvent('click', {bubbles:true}));
    return !!pin;
  });
  await new Promise(r => setTimeout(r, 4000));
  const s4 = await page.evaluate(() => ({
    sheetOpen: document.querySelector('aside').classList.contains('show'),
    routeBar: document.getElementById('routeBar').classList.contains('show'),
  }));
  console.log(JSON.stringify({ s1, chipOpensSheet: s2, pinFound: s3, afterPinClick: s4 }));
  await browser.close();
})();
