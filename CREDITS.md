# 제작 자료

- 앱 아이콘: 내장 이미지 생성 도구로 제작한 `game/images/app_icon.png`. 생성 방향: 짙은 회색 배경, 중앙의 살짝 열린 문, 문틈과 바닥에 새는 아이보리빛, 낡은 질감, 작은 크기에서 읽히는 실루엣, 글자·인물·문양 없음. `tools/windows_icon.py`로 Windows ICO 변환.

- 시나리오와 인물 설정: 사용자 제공 원고 및 확정 기획.
- 윤서아 이미지: 사용자 제공 기본 / 옅은 미소 / 다정한 미소 3종. 원본 파일은 유지하며, AI 배경 제거로 만든 대화 패널용 투명 배경 버전 3종을 추가했다. 로비 회상에는 위쪽 여백과 공통 좌표를 갖는 `seoa_lobby_*.png` 3종을 사용해 표정을 바꿔도 몸 위치가 흔들리지 않게 했다.
- 방 배경: 기존 프로젝트의 `room_cold.png`를 보존하고, Lanczos 보간으로 1920×1080 확대본 `room_cold_fhd.png`를 제작해 사용. 구도·색감·사물 배치는 재생성하지 않았다. 제작 스크립트: `tools/prepare_room_background.py`.
- 열린 문 근접 배경: 내장 이미지 생성 도구로 제작한 `game/images/door_threshold.png`. 기존 방을 화풍·문 형태 참고 이미지로 사용. 최종 생성 프롬프트는 `docs/문틈-이미지-프롬프트.md`에 보관.
- 로비 회상 배경: 내장 이미지 생성 도구로 제작한 `game/images/lobby_day.png` (1920×1080). 개방적이고 평화로운 온결 접수 공간. 생성 지시: 늦은 오후 자연광, 큰 창과 정돈된 접수대, 낮은 채도의 회백색·밝은 나무·식물, 절제된 디지털 페인팅, 오른쪽 인물 배치와 하단 대사창을 위한 여백, 인물·글자·로고 없음.
- 대사창 그라데이션: `game/images/dialogue_gradient.png`. 프로젝트 내에서 생성한 1×303 알파 그라데이션으로, 화면에서 1920×303으로 늘려 사용.
- 메인 메뉴 배경: AI 생성 `game/images/menu_corridor.png`. 온결 시설의 텅 빈 복도와 중앙 UI 여백을 위한 배경.
- 메인 메뉴 로고: 사용자 제공 `game/images/title_logo.png` 사용.
- 김수혁 인물 탭: 사용자 제공 원본을 `game/images/suhyeok_profile.png`로 복사해 상반신 크롭으로 표시.
- 효과음과 안내 음악: 이 프로젝트용 합성 음원. `tools/make_audio.py`로 재생성 가능. 인물 음성 없음.
- 복도 데모: 기존 메뉴 복도를 어둡게 보정해 재사용. 발소리 2종과 둔한 타격음은 같은 합성 스크립트의 `--corridor-only` 옵션으로 생성한다.
- 복도 정적 연출의 마지막 발소리와 낮은 불협화음은 `tools/make_audio.py --tension-only`로 생성한 합성 음원이다.
- 복도 긴박한 선택의 `ticking_urgent.wav`는 `tools/make_audio.py --urgent-only`로 생성한다. 0.32초 간격의 틱/톡이며 문 앞 선택에는 사용하지 않는다.
- 글꼴: 아래 표와 라이선스 안내 참고.
- 엔진: Ren’Py 8.5.3.

## 이미지 제작 출처

2026-10-22 제작자 확인: 제공한 서아·수혁·로고·기존 방 이미지를 포함한 이미지 에셋은 생성형 AI로 제작한 자료다. 외부 작품이나 구매 이미지 에셋을 제공한 것은 아니다. UI 그라데이션 등은 코드로 생성했다. 이 출처 기록이 AI 결과물의 독점적 권리나 제3자 권리 비침해를 보증하는 것은 아니며, 생성 서비스의 이용 조건이 적용된다.

## 글꼴과 재배포 조건

파일 이름이 아니라 TTF 내부의 글꼴 이름과 저작권 표시를 확인했다. 글꼴은 게임에 동봉하며 별도로 판매하지 않는다.

| 파일 | 실제 글꼴 · 권리자 | 동봉 라이선스 |
| --- | --- | --- |
| `NanumGothic-Regular.ttf` | 나눔고딕 · NHN | `game/fonts/NanumGothic-OFL.txt` |
| `NanumMyeongjo.ttf` | 나눔명조 · NHN, FONTRIX 디자인 | `game/fonts/NanumMyeongjo-OFL.txt` |
| `NanumPenScript-Regular.ttf` | 나눔손글씨 펜 · NHN | `game/fonts/NanumPenScript-OFL.txt` |
| `NanumSmile.ttf` | 나눔손글씨 기쁨밝음 (Nanum GiBbeumBarkEum) · NAVER, CLOVA AI OCR Team | `game/fonts/NanumSmile-OFL.txt` |

[네이버 공식 글꼴 안내](https://hangeul.naver.com/font)는 나눔글꼴과 클로바 나눔손글씨의 사용·프로그램 동봉·재배포를 허용하며, 재배포 시 저작권 안내와 라이선스 전문을 포함하도록 안내한다. [공식 라이선스 전문](https://help.naver.com/service/30016/contents/18088?osType=PC&lang=ko)은 SIL Open Font License 1.1이다. 해당 고지와 전문을 배포 ZIP의 `game/fonts/`에도 포함한다. 확인일: 2026-10-22.
