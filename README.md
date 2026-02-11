# 🔮 사주팔자 만세력 계산기 with AI

OpenAI ChatGPT를 활용한 사주팔자 만세력 계산 및 AI 풀이 서비스

## ✨ 주요 기능

### 1. 사주팔자 계산
- 생년월일시를 입력하면 사주팔자(四柱八字) 자동 계산
- 천간(天干)과 지지(地支) 표시
- 연주, 월주, 일주, 시주 구분 표시
- 한자 표기 지원

### 2. 오행(五行) 분석
- 천간과 지지의 오행 분석
- 목(木), 화(火), 토(土), 금(金), 수(水) 개수 통계
- 오행의 균형 상태 확인

### 3. 음양(陰陽) 분석
- 천간과 지지의 음양 속성 표시
- 음양 균형 확인

### 4. AI 사주 풀이 🤖
OpenAI GPT-4를 활용한 전문적인 사주 해석:
- **기본 성향**: 타고난 성격과 기질
- **오행 균형**: 오행의 강약과 조화
- **길흉 판단**: 사주의 전반적인 길흉
- **직업운**: 적합한 직업 분야
- **재물운**: 재물에 관한 운세
- **건강운**: 주의해야 할 건강 부분
- **조언**: 인생에서 주의할 점

### 5. 결과 다운로드
- 사주팔자 및 AI 풀이 결과를 텍스트 파일로 다운로드

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

3. **OpenAI API 키 설정**

`.streamlit/secrets.toml` 파일 생성:
```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

`.streamlit/secrets.toml` 파일 편집:
```toml
OPENAI_API_KEY = "sk-your-actual-api-key-here"
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
   ```
7. **Deploy** 클릭

### 3. 배포 완료
앱이 자동으로 배포되며 공개 URL이 생성됩니다.

## 💰 비용 안내

### OpenAI API 비용
- **GPT-4**: 약 $0.03/1K tokens (입력 기준)
- **GPT-3.5-turbo**: 약 $0.001/1K tokens (훨씬 저렴)

한 번의 풀이당 약 1,000-2,000 tokens 사용 (GPT-4 기준 약 $0.03-0.06)

비용을 절감하려면 `app.py`의 `get_saju_interpretation` 함수에서 모델을 변경:
```python
model="gpt-3.5-turbo"  # GPT-4 대신 사용
```

### 사용량 제한
OpenAI API는 분당 요청 수 제한(Rate Limit)이 있습니다:
- 무료 플랜: 분당 3 requests
- 유료 플랜: 플랜에 따라 다름

## 📁 프로젝트 구조

```
saju84/
├── app.py                          # 메인 Streamlit 앱
├── saju_calculator.py              # 사주팔자 계산 모듈
├── requirements.txt                # Python 의존성
├── .streamlit/
│   └── secrets.toml.example       # API 키 설정 예시
└── README.md                       # 프로젝트 문서
```

## 🛠️ 기술 스택

- **Python 3.8+**
- **Streamlit**: 웹 UI 프레임워크
- **OpenAI API**: GPT-4/GPT-3.5-turbo를 통한 AI 풀이
- **만세력 계산**: 천간지지 계산 알고리즘

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
3. **음력 변환**: 현재는 양력 기준으로 계산됩니다. 정확한 사주는 음력 변환이 필요할 수 있습니다.
4. **입춘 기준**: 전통 사주는 입춘을 기준으로 연도가 바뀌지만, 본 앱은 간단히 1월 1일을 기준으로 합니다.
5. **AI 정확도**: AI 풀이는 참고용이며, 실제 명리학자의 풀이와 다를 수 있습니다.

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
