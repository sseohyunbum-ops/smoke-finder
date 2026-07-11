# 📱 연기공간 — GitHub Pages 배포 & 아이폰 설치 가이드

앱 폴더 위치: `E:\downloads\클로드 자동화\smoking-area-finder`

배포에 필요한 파일 (이미 모두 준비됨):
```
index.html          ← 앱 본체
manifest.json       ← 홈 화면 앱 설정
sw.js               ← 오프라인 캐시
data/korea-spots.json   ← 전국 지자체 흡연구역 293곳 (공공데이터)
icons/icon-180.png / icon-192.png / icon-512.png
```
(`tools/` 폴더는 데이터 갱신용 스크립트라 올려도 되고 안 올려도 됩니다.)

---

## 1단계 — GitHub 저장소 만들기 (약 2분)

1. https://github.com 접속 → 로그인 (계정이 없으면 Sign up으로 가입)
2. 우측 상단 **+** 버튼 → **New repository**
3. 설정:
   - **Repository name**: `smoke-finder` (원하는 이름 아무거나, 영문 소문자 권장)
   - **Public** 선택 ← 중요! (무료 Pages는 Public 저장소만 가능)
   - 나머지는 그대로 두고 **Create repository** 클릭

## 2단계 — 파일 업로드 (약 2분)

1. 방금 만든 저장소 페이지에서 **"uploading an existing file"** 링크 클릭
   (또는 저장소에서 **Add file → Upload files**)
2. 윈도우 탐색기에서 `E:\downloads\클로드 자동화\smoking-area-finder` 폴더를 열고
   **안에 있는 파일과 폴더 전부**를 선택(Ctrl+A) → 브라우저 업로드 영역으로 **드래그&드롭**
   - `data`, `icons` 폴더도 통째로 드래그하면 하위 파일까지 올라갑니다
3. 아래 **Commit changes** 버튼 클릭

## 3단계 — Pages 켜기 (약 1분)

1. 저장소 상단 메뉴 **Settings** → 왼쪽 사이드바 **Pages**
2. **Source**: `Deploy from a branch`
3. **Branch**: `main` 선택, 폴더는 `/ (root)` → **Save**
4. 1~2분 기다린 후 페이지를 새로고침하면 상단에 주소가 나타납니다:
   ```
   https://<내아이디>.github.io/smoke-finder/
   ```

## 4단계 — 아이폰에 설치 (약 1분)

1. 아이폰 **Safari**에서 위 주소 접속 (⚠️ 크롬 말고 꼭 Safari)
2. 위치 권한을 물으면 **허용**
3. 하단 가운데 **공유 버튼(⬆️)** 탭 → 스크롤 내려서 **"홈 화면에 추가"** 탭
4. 이름 확인(연기공간) → **추가**

이제 홈 화면의 🚬 아이콘을 누르면 주소창 없는 전체 화면 앱으로 실행됩니다.
GPS로 현재 위치를 잡고 주변 흡연구역을 거리순으로 보여줘요.

---

## 데이터 갱신 방법 (선택, 몇 달에 한 번)

지자체 데이터가 업데이트되면 PC에서:
```
cd "E:\downloads\클로드 자동화\smoking-area-finder"
python tools\harvest_data.py
```
실행 후 새로 만들어진 `data/korea-spots.json` 파일만 GitHub 저장소에
다시 업로드(같은 위치에 덮어쓰기)하면 됩니다. **API 키 필요 없음.**

## 서울시 API 키 확장 (선택)

서울시 통합 데이터(`smkFclt`, 98건)는 좌표 없이 주소만 제공되어 현재 미포함.
포함하려면:
1. https://data.seoul.go.kr → 회원가입 → 나의 화면 → **인증키 신청** (즉시 무료 발급)
2. 발급받은 키를 저에게 알려주시면 주소→좌표 변환(지오코딩) 포함해서
   수집 스크립트에 병합해 드립니다.

## 문제 해결

- **위치를 못 잡아요**: 설정 → Safari → 위치 → 허용 확인. 실패해도 지도를 탭하면 그 지점 주변을 검색합니다.
- **결과가 없어요**: 반경을 2~3km로 넓혀보세요. 데이터가 없는 지역은 OSM(주황 마커)만 나옵니다.
- 파란 마커 🏛 = 지자체 공공데이터 / 주황 마커 = OpenStreetMap 등록 지점
