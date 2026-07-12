const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    headless: 'new',
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 844 });
  const out = {};

  // 1) 구독 다이어트: 서비스 2개 선택(하나는 '거의 안 씀' 기본) → 진단
  await page.goto('http://127.0.0.1:8757/subscription-diet/index.html', { waitUntil: 'networkidle2' });
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: 'networkidle2' });
  await page.evaluate(() => { document.querySelectorAll('.svc')[0].click(); });
  await page.evaluate(() => { document.querySelectorAll('.svc')[1].click(); });
  await page.evaluate(() => { document.querySelectorAll('.svc.on')[1].querySelectorAll('.use button')[2].click(); });
  await new Promise(r => setTimeout(r, 200));
  await page.evaluate(() => document.getElementById('calcBtn').click());
  await new Promise(r => setTimeout(r, 600));
  out.sub = await page.evaluate(() => ({
    shown: document.getElementById('result').classList.contains('show'),
    year: document.getElementById('rYear').textContent,
    waste: document.getElementById('rWaste').textContent,
    kills: document.querySelectorAll('.k-item').length,
  }));
  await page.screenshot({ path: '../../mini1.png' });

  // 2) 축의금: 8개 질문 각각 첫 옵션 선택 → 계산
  await page.goto('http://127.0.0.1:8757/chukui-calc/index.html', { waitUntil: 'networkidle2' });
  await page.evaluate(() => { document.querySelectorAll('.q').forEach(q => q.querySelector('.opts button').click()); });
  await page.evaluate(() => document.getElementById('calcBtn').click());
  await new Promise(r => setTimeout(r, 600));
  out.chukui = await page.evaluate(() => ({
    shown: document.getElementById('result').classList.contains('show'),
    amt: document.getElementById('rAmt').textContent,
    whyRows: document.querySelectorAll('.w-item').length,
  }));
  await page.screenshot({ path: '../../mini2.png' });

  // 3) 로또: 1만원 / 10년 → 계산
  await page.goto('http://127.0.0.1:8757/lotto-instead/index.html', { waitUntil: 'networkidle2' });
  await page.evaluate(() => {
    document.querySelectorAll('#qSpend button')[1].click();
    document.querySelectorAll('#qYears button')[1].click();
  });
  await page.evaluate(() => document.getElementById('calcBtn').click());
  await new Promise(r => setTimeout(r, 1200));
  out.lotto = await page.evaluate(() => ({
    shown: document.getElementById('result').classList.contains('show'),
    main: document.getElementById('rMain').textContent.slice(0, 60),
    bars: document.querySelectorAll('.bar-fill').length,
  }));
  await page.screenshot({ path: '../../mini3.png' });

  console.log(JSON.stringify(out, null, 1));
  await browser.close();
})();
