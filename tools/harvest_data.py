# -*- coding: utf-8 -*-
"""
data.go.kr 에서 '흡연구역' 관련 파일 데이터셋(CSV)을 검색·다운로드하여
위경도 좌표가 있는 항목만 data/korea-spots.json 으로 병합한다.
API 키 불필요 (공공누리 오픈 파일 데이터 직접 다운로드).

사용법:  python tools/harvest_data.py
"""
import json, re, csv, io, sys, time, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "korea-spots.json"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
KEYWORDS = ["흡연구역", "흡연시설", "흡연부스"]
MAX_PAGES = 3          # 키워드당 검색 페이지 수 (페이지당 40건)
SLEEP = 0.15           # 요청 간 대기 (서버 예의)

def fetch(url, data=None, timeout=25):
    req = urllib.request.Request(url, data=data, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def search_datasets():
    """검색 결과에서 fileData 상세페이지 ID 목록 수집"""
    ids = {}
    for kw in KEYWORDS:
        for page in range(1, MAX_PAGES + 1):
            q = urllib.parse.urlencode({
                "dType": "FILE", "keyword": kw, "operator": "AND",
                "currentPage": page, "perPage": 40,
            })
            try:
                html = fetch(f"https://www.data.go.kr/tcs/dss/selectDataSetList.do?{q}").decode("utf-8", "ignore")
            except Exception as e:
                print(f"  검색 실패({kw} p{page}): {e}"); continue
            blocks = re.findall(r'/data/(\d+)/fileData\.do"\s*>(.*?)</a>', html, re.S)
            for i, block in blocks:
                text = re.sub(r'<[^>]+>', '', block)          # 태그 제거
                text = re.sub(r'\s+', ' ', text).strip()       # 공백 정리
                ids[i] = text
            if not blocks:
                break
            time.sleep(SLEEP)
    return ids

def get_file_info(ds_id):
    """상세페이지에서 atchFileId / fileDetailSn / 제목 추출"""
    html = fetch(f"https://www.data.go.kr/data/{ds_id}/fileData.do").decode("utf-8", "ignore")
    m = re.search(r'atchFileId=(FILE_[0-9]+)', html)
    if not m:
        m = re.search(r'"atchFileId"\s*[:=]\s*"(FILE_[0-9]+)"', html)
    sn = re.search(r'fileDetailSn=(\d+)', html)
    title = re.search(r'<title>([^<|]+)', html)
    ext = "CSV" if re.search(r'recommendExtsn=CSV|\.csv', html, re.I) else ""
    return (m.group(1) if m else None,
            sn.group(1) if sn else "1",
            title.group(1).strip() if title else ds_id,
            ext)

def download_csv(atch_id, sn):
    raw = fetch(f"https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId={atch_id}&fileDetailSn={sn}")
    for enc in ("utf-8-sig", "cp949", "utf-8", "euc-kr"):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return None

LAT_PAT = re.compile(r'위도|(?<![a-z])lat|LA$', re.I)
LNG_PAT = re.compile(r'경도|(?<![a-z])(lng|lon)|LO$', re.I)
NAME_PAT = ["명칭", "시설명", "장소명", "설치 위치", "설치위치", "위치", "상세위치", "주소", "소재지", "장소", "건물명"]

def parse_rows(text, source):
    try:
        rows = list(csv.reader(io.StringIO(text)))
    except Exception:
        return []
    if len(rows) < 2:
        return []
    header = [h.strip() for h in rows[0]]
    lat_i = lng_i = None
    for i, h in enumerate(header):
        if lat_i is None and LAT_PAT.search(h): lat_i = i
        if lng_i is None and LNG_PAT.search(h): lng_i = i
    if lat_i is None or lng_i is None or lat_i == lng_i:
        return []
    name_i = None
    for key in NAME_PAT:
        for i, h in enumerate(header):
            if key in h and i not in (lat_i, lng_i):
                name_i = i; break
        if name_i is not None: break
    out = []
    for r in rows[1:]:
        if len(r) <= max(lat_i, lng_i): continue
        try:
            lat, lng = float(r[lat_i]), float(r[lng_i])
        except ValueError:
            continue
        if lat > 90 and lng < 90:  # 위경도 뒤바뀐 파일 보정
            lat, lng = lng, lat
        if not (33.0 <= lat <= 39.5 and 124.0 <= lng <= 132.0):
            continue
        name = (r[name_i].strip() if name_i is not None and len(r) > name_i else "") or "흡연구역"
        out.append({"n": name[:60], "la": round(lat, 6), "lo": round(lng, 6), "s": source})
    return out

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("1) data.go.kr 검색 중…")
    ids = search_datasets()
    print(f"   후보 데이터셋 {len(ids)}건")
    spots, sources = [], []
    INCLUDE = re.compile(r'흡연\s*(구역|시설|부스|실)|실외\s*흡연')
    EXCLUDE = re.compile(r'금연|단속|민원|소매|통계|건강|할인|카페|와이파이')
    INCLUDE = re.compile(r'흡연\s*(구역|시설|부스|실)|실외\s*흡연')
    EXCLUDE = re.compile(r'금연|단속|민원|소매|통계|건강|할인|카페|와이파이')
    # 검색 결과 제목으로 먼저 필터링 → 다운로드 대상 최소화
    targets = {i: t for i, t in ids.items() if INCLUDE.search(t) and not EXCLUDE.search(t)}
    print(f"   제목 필터 통과: {len(targets)}건 (다운로드 대상)")
    for n, (ds_id, hint) in enumerate(sorted(targets.items()), 1):
        try:
            atch, sn, title, ext = get_file_info(ds_id)
            if not INCLUDE.search(title) or EXCLUDE.search(title):
                continue
            if not INCLUDE.search(title) or EXCLUDE.search(title):
                continue
            time.sleep(SLEEP)
            if not atch:
                print(f"   [{n}] {title}: 파일ID 없음(스킵)"); continue
            text = download_csv(atch, sn)
            time.sleep(SLEEP)
            if not text:
                print(f"   [{n}] {title}: 디코딩 실패"); continue
            got = parse_rows(text, title)
            if got:
                spots.extend(got)
                sources.append({"id": ds_id, "title": title, "count": len(got)})
                print(f"   [{n}] {title}: {len(got)}개 좌표 확보")
            else:
                print(f"   [{n}] {title}: 좌표 컬럼 없음(스킵)")
        except Exception as e:
            print(f"   [{n}] {ds_id}: 오류 {e}")
    # 중복 제거 (약 11m 격자)
    seen, uniq = set(), []
    for s in spots:
        key = (round(s["la"], 4), round(s["lo"], 4))
        if key in seen: continue
        seen.add(key); uniq.append(s)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "updated": time.strftime("%Y-%m-%d"),
        "license": "공공누리 (data.go.kr 지자체 개방 데이터)",
        "sources": sources,
        "spots": uniq,
    }, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"\n완료: {len(uniq)}개 지점 → {OUT}")

if __name__ == "__main__":
    main()
