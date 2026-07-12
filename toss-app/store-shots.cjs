const puppeteer = require('puppeteer-core');
const BASE = 'https://sseohyunbum-ops.github.io/smoke-finder/index.html';
const SHOTS = [
  { f: '스크린샷1-세로-검색결과.png', w: 636, h: 1048, q: '?demo=37.5533,126.9700', wait: 12000 },
  { f: '스크린샷2-세로-도보경로.png', w: 636, h: 1048, q: '?demo=37.5533,126.9700&sel=0', wait: 16000 },
  { f: '스크린샷3-세로-제보.png', w: 636, h: 1048, q: '?demo=37.5533,126.9700&report=1', wait: 12000 },
  { f: '스크린샷4-가로.png', w: 1504, h: 741, q: '?demo=37.5533,126.9700&sel=1', wait: 16000 },
];
(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    headless: 'new',
  });
  for (const s of SHOTS) {
    const page = await browser.newPage();
    await page.setViewport({ width: s.w, height: s.h });
    await page.goto(BASE + s.q + '&cb=' + Date.now(), { waitUntil: 'networkidle2', timeout: 40000 }).catch(()=>{});
    await new Promise(r => setTimeout(r, s.wait));
    await page.screenshot({ path: '../toss-assets/' + s.f });
    console.log(s.f, 'ok');
    await page.close();
  }
  await browser.close();
})();
