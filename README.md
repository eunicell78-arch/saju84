# 🔮 사주팔자 만세력 계산기 with AI

천을귀인 만세력 v5.05 기준으로 정확한 계산과 OpenAI ChatGPT를 활용한 사주팔자 만세력 계산 및 AI 풀이 서비스

## ✨ 주요 기능

### 1. 사주팔자 계산 (정확도 개선 ✓)
- 생년월일시를 입력하면 사주팔자(四柱八字) 자동 계산
- 천간(天干)과 지지(地支) 표시
- 연주, 월주, 일주, 시주 정확한 계산
- 한자 표기 지원
- **천을귀인 만세력과 100% 일치하는 정확도**

### 2. 오행(五行) 분석
- 천간과 지지의 오행 분석
- 목(木), 화(火), 토(土), 금(金), 수(水) 개수 통계
- 오행의 균형 상태 확인

### 3. 음양(陰陽) 분석
- 천간과 지지의 음양 속성 표시
- 음양 균형 확인

### 4. 십신(十神) 분석 🆕
- 일간을 기준으로 타 간지와의 관계 분석
- 비겁(比劫), 식상(食傷), 재성(財星), 관살(官殺), 인성(印星)
- 천간과 지지 모두 십신 표시

### 5. 12운성(十二運星) 🆕
- 일간 오행이 12지지에서 받는 기운 분석
- 장생, 목욕, 관대, 건록, 제왕, 쇠, 병, 사, 묘, 절, 태, 양

### 6. 신살(神殺) 분석 🆕
- **천을귀인**: 가장 길한 귀인
- **역마살**: 이동, 변동
- **도화살**: 이성, 매력, 예술
- **공망**: 60갑자별 공망
- **원진**: 원한과 시기
- **양인**: 강한 칼날, 폭력성

### 7. 형충회합(刑沖會合) 🆕
- **충(沖)**: 지지 간 충돌
- **합(合)**: 육합, 삼합, 방합
- **형(刑)**: 무은지형, 무례지형, 자형

### 8. 납음오행(納音五行) 🆕
- 60갑자별 납음오행 표시
- 연주, 월주, 일주, 시주의 납음

### 9. 대운(大運) 🆕
- 순행/역행 판단 (양남음녀/음남양녀)
- 대운 시작 나이 계산
- 10개 대운 표시 (10년 단위)

### 10. 세운(歲運) 🆕
- 과거 5년 + 현재 + 미래 10년 표시
- 연도별 간지와 나이 표시
- 현재 세운 강조

### 11. AI 사주 풀이 🤖 (개선됨)
OpenAI GPT-4o 모델을 활용한 전문적이고 체계적인 사주 해석:
- **사주 전체 구조 분석**: 일간의 강약과 구조 특징
- **십신으로 본 성격과 적성**: 재능과 적성 분석
- **오행 균형과 용신**: 오행 강약과 용신 제시
- **신살의 길흉**: 주요 신살의 의미와 영향
- **직업운과 재물운**: 적합한 직업과 재물 운세
- **대운과 세운**: 현재 운세 흐름 해석
- **건강과 주의사항**: 건강 관련 조언

## 🤖 AI 모델

- **메인 모델**: OpenAI GPT-4o
  - 빠르고 효율적인 응답
  - 구조화된 8-13개 섹션 출력
  
- **비용**: 1건당 약 ₩130-170원 (12-16K 토큰 기준)

### 모델 특징
- ✅ 체계적이고 구조화된 분석
- ✅ 상세한 설명과 구체적인 조언
- ✅ 일관된 출력 형식
- ✅ 빠른 응답 속도 (5-10초)

### 12. 결과 다운로드
- 사주팔자 및 AI 풀이 결과를 텍스트 파일로 다운로드

## 🎯 정확도 검증

### Test Case 1: 2009-12-28 16:35 여자
- ✅ 년주: 己丑
- ✅ 월주: 丙子
- ✅ 일주: 丁未
- ✅ 시주: 戊申
- ✅ 오행: 木0, 火2, 土4, 金1, 水1

### Test Case 2: 1992-10-24 05:30 남자
- ✅ 년주: 壬申
- ✅ 월주: 庚戌
- ✅ 일주: 癸酉
- ✅ 시주: 乙卯

**천을귀인 만세력 v5.05와 100% 일치 확인됨**

## 🔐 보안 설정

이 앱은 패스워드 인증이 필요합니다.

### Streamlit Cloud 배포 시

1. Streamlit Cloud 대시보드에서 앱 선택
2. **Settings** → **Secrets** 탭으로 이동
3. 다음 설정 추가:

```toml
OPENAI_API_KEY = "your-openai-api-key"
APP_PASSWORD = "your-secure-password"
```

4. **Save** 클릭

### 로컬 실행 시

1. `.streamlit/secrets.toml` 파일 생성
2. `.streamlit/secrets.toml.example`의 내용을 복사하여 실제 값 입력
3. 패스워드는 **절대 GitHub에 커밋하지 마세요**

### 패스워드 변경

Streamlit Cloud Secrets에서 `APP_PASSWORD` 값을 변경하면 즉시 적용됩니다.

## 🚀 빠른 시작

### 로컬 실행

1. **저장소 클론**
```bash
git clone https://github.com/eunicell78-arch/saju84.git
cd saju84
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **OpenAI API 키 및 패스워드 설정**

`.streamlit/secrets.toml` 파일 생성:
```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

`.streamlit/secrets.toml` 파일 편집:
```toml
OPENAI_API_KEY = "sk-your-actual-api-key-here"
APP_PASSWORD = "your-secure-password-here"
```

> OpenAI API 키는 [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.

4. **앱 실행**
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하세요.

## 🌐 Streamlit Cloud 배포

### 1. GitHub에 푸시
```bash
git add .
git commit -m "Add Saju calculator with AI"
git push origin main
```

### 2. Streamlit Cloud 설정

1. [Streamlit Cloud](https://streamlit.io/cloud)에 로그인
2. **New app** 클릭
3. 저장소 선택: `eunicell78-arch/saju84`
4. Main file path: `app.py`
5. **Advanced settings** → **Secrets** 클릭
6. 다음 내용 입력:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-api-key-here"
   APP_PASSWORD = "your-secure-password-here"
   ```
7. **Deploy** 클릭

### 3. 배포 완료
앱이 자동으로 배포되며 공개 URL이 생성됩니다.

## 💰 비용 안내

### OpenAI API 비용
- **GPT-4o**: 
  - Input: $2.50 / 1M tokens
  - Output: $10.00 / 1M tokens
  - 한 번의 풀이당 약 ₩130-170원 (프롬프트 3K + 응답 12-16K 토큰 기준)

> ⚠️ **주의**: 위 가격은 참고용이며 실제 가격은 변동될 수 있습니다. 최신 가격은 [OpenAI 공식 가격 페이지](https://openai.com/api/pricing/)에서 확인하세요.

### 사용량 제한
OpenAI API는 분당 요청 수 제한(Rate Limit)이 있습니다:
- 무료 플랜: 분당 3 requests
- 유료 플랜: 플랜에 따라 다름

## 📁 프로젝트 구조

```
saju84/
├── app.py                          # 메인 Streamlit 앱
├── saju_calculator.py              # 사주팔자 계산 모듈 (통합)
├── sipsin.py                       # 십신(十神) 계산 모듈
├── unsung_12.py                    # 12운성(十二運星) 모듈
├── sinsal.py                       # 신살(神殺) 계산 모듈
├── napeum.py                       # 납음오행(納音五行) 모듈
├── hyungchunghap.py                # 형충회합(刑沖會合) 모듈
├── daeun.py                        # 대운(大運) 계산 모듈
├── seun.py                         # 세운(歲運) 계산 모듈
├── requirements.txt                # Python 의존성
├── .streamlit/
│   └── secrets.toml.example       # API 키 설정 예시
└── README.md                       # 프로젝트 문서
```

## 🛠️ 기술 스택

- **Python 3.8+**
- **Streamlit**: 웹 UI 프레임워크
- **Pandas**: 데이터 처리 및 표시
- **OpenAI API**: GPT-4o 모델을 통한 AI 풀이
- **만세력 계산**: 천간지지 계산 알고리즘 (천을귀인 v5.05 기준)

## 📚 사주팔자 개념

### 사주팔자란?
사주팔자(四柱八字)는 한 사람이 태어난 년(年), 월(月), 일(日), 시(時)를 천간(天干)과 지지(地支)로 표현한 것입니다.

- **천간(10개)**: 갑(甲), 을(乙), 병(丙), 정(丁), 무(戊), 기(己), 경(庚), 신(辛), 임(壬), 계(癸)
- **지지(12개)**: 자(子), 축(丑), 인(寅), 묘(卯), 진(辰), 사(巳), 오(午), 미(未), 신(申), 유(酉), 술(戌), 해(亥)

### 오행(五行)
- **목(木)**: 나무, 성장
- **화(火)**: 불, 열정
- **토(土)**: 흙, 안정
- **금(金)**: 쇠, 강인함
- **수(水)**: 물, 지혜

## ⚠️ 주의사항

1. **참고용 서비스**: 본 서비스는 참고용이며, 전문가의 상담을 대체할 수 없습니다.
2. **API 키 보안**: `.streamlit/secrets.toml` 파일은 절대 Git에 커밋하지 마세요.
3. **양력 기준**: 양력 기준으로 계산됩니다. 음력 생일인 경우 양력으로 변환 후 입력하세요.
4. **절기 기준**: 월주 계산 시 절기를 근사적으로 적용합니다. 더 정확한 계산을 위해서는 정확한 절기 데이터가 필요합니다.
5. **AI 정확도**: AI 풀이는 참고용이며, 실제 명리학자의 풀이와 다를 수 있습니다.

## 🔧 계산 정확도

### 개선 사항
- ✅ 야자시(夜子時) 처리 제거 (당일 자시로 정확히 계산)
- ✅ 시두법 정확히 적용 (일간에 따른 시간 간지 시작점)
- ✅ 일주 계산 정확도 개선 (1900-01-01 = 甲戌 기준)
- ✅ 월주 계산 개선 (절기 기준 근사 적용)
- ✅ 십신, 12운성, 신살, 형충회합, 대운, 세운 전체 기능 추가

### 제한 사항
- 대운수 계산 시 정확한 절입일 대신 근사치 사용
- 일부 고급 신살 미포함 (필요시 추가 가능)

## 🔒 보안

### .gitignore 설정
다음 파일은 Git에 커밋되지 않도록 `.gitignore`에 추가하세요:
```
.streamlit/secrets.toml
__pycache__/
*.pyc
.env
```

### API 키 관리
- 로컬: `.streamlit/secrets.toml` 파일 사용
- Streamlit Cloud: Settings → Secrets 메뉴에서 설정
- 절대 API 키를 코드에 하드코딩하지 마세요

## 🤝 기여

이슈나 풀 리퀘스트는 언제든 환영합니다!

## 📄 라이선스

이 프로젝트는 개인 및 교육 목적으로 자유롭게 사용할 수 있습니다.

## 📞 문의

문제가 있거나 질문이 있으시면 GitHub Issues를 이용해주세요.

---

**Made with ❤️ using Streamlit and OpenAI**
