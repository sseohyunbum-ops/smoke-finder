// 토스 미니앱 환경 어댑터: SDK 위치 API를 본체 앱에 주입한다.
// 본체(index.html)의 locateMe()는 window.TossLocation이 있으면 이를 우선 사용한다.
import { Accuracy, getCurrentLocation } from '@apps-in-toss/web-framework';

window.TossLocation = {
  getCurrentLocation: async () => {
    // 'allowed'가 아니면(최초 미결정 포함) 토스 표준 다이얼로그로 권한 요청
    const perm = await getCurrentLocation.getPermission();
    if (perm !== 'allowed') {
      const result = await getCurrentLocation.openPermissionDialog();
      if (result !== 'allowed') throw new Error('위치 권한이 거부되었어요');
    }
    const loc = await getCurrentLocation({ accuracy: Accuracy.High });
    return loc.coords; // { latitude, longitude, ... }
  },
};
