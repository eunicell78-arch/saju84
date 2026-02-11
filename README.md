# 🔮 사주팔자 만세력 계산기 with AI 풀이

생년월일시를 입력하면 사주팔자를 계산하고, OpenAI ChatGPT가 전문적으로 풀이해주는 Streamlit 웹 애플리케이션입니다.

## ✨ 주요 기능

### 1. 사주팔자 계산
- 생년월일시 입력으로 사주팔자 자동 계산
- 천간(天干), 지지(地支) 표시
- 한자와 한글 병기
- 오행(五行) 분석 및 시각화

### 2. AI 사주 풀이 (OpenAI ChatGPT)
GPT-4를 활용한 전문적인 사주 해석:
- 🎯 **기본 성향**: 타고난 성격과 기질
- ⚖️ **오행 균형**: 오행의 강약과 조화
- 🍀 **길흉 판단**: 전반적인 운세
- 💼 **직업운**: 적합한 직업 분야
- 💰 **재물운**: 재물에 관한 운세
- 🏥 **건강운**: 주의할 건강 사항
- 👥 **대인관계**: 인간관계 특징
- 💡 **인생 조언**: 발전을 위한 조언

### 3. 결과 저장
- 사주 결과와 AI 풀이를 텍스트 파일로 다운로드
- 나중에 다시 참고 가능

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

`.streamlit/secrets.toml` 파일을 생성하고 다음 내용을 입력:
```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

API 키는 [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.

4. **앱 실행**
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하면 앱을 사용할 수 있습니다.

## ☁️ Streamlit Cloud 배포

### 1. GitHub 저장소 준비
- 이 저장소를 포크하거나 자신의 GitHub에 푸시합니다.

### 2. Streamlit Cloud 연결
1. [Streamlit Cloud](https://share.streamlit.io/)에 접속
2. "New app" 클릭
3. GitHub 저장소 연결
4. Main file: `app.py` 선택

### 3. API 키 설정 (중요!)
1. Streamlit Cloud 대시보드에서 앱 선택
2. **Settings** → **Secrets** 메뉴로 이동
3. 다음 형식으로 API 키 입력:
```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```
4. **Save** 클릭

### 4. 배포 완료
- 앱이 자동으로 빌드되고 배포됩니다
- 제공된 URL을 통해 어디서든 접속 가능합니다

## 📋 사용 방법

1. **생년월일 입력**
   - 연도, 월, 일 선택
   - 출생 시간 입력 (24시간 형식)
   - 성별 선택

2. **사주 계산**
   - "사주 계산하기" 버튼 클릭
   - 사주팔자 결과 확인

3. **AI 풀이 보기**
   - "AI 사주풀이 보기" 버튼 클릭
   - 약 10-20초 후 상세 풀이 확인

4. **결과 저장**
   - "풀이 결과 다운로드" 버튼으로 TXT 파일 저장

## 🔧 기술 스택

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4o-mini (or GPT-4)
- **Language**: Python 3.8+
- **Deployment**: Streamlit Cloud

## 📦 프로젝트 구조

```
saju84/
├── app.py                          # 메인 Streamlit 애플리케이션
├── saju_calculator.py              # 사주팔자 계산 로직
├── requirements.txt                # Python 의존성
├── .gitignore                      # Git 제외 파일
├── .streamlit/
│   └── secrets.toml.example       # API 키 설정 예시
└── README.md                       # 프로젝트 문서
```

## 💰 비용 안내

### OpenAI API 비용
- **GPT-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **GPT-4**: ~$30 per 1M input tokens, ~$60 per 1M output tokens
- 1회 풀이당 약 1,000-2,000 토큰 사용
- GPT-4o-mini 사용 시 1회당 약 $0.001 미만

### Streamlit Cloud
- 무료 플랜으로 충분히 사용 가능
- 개인 프로젝트 및 소규모 사용에 적합

## ⚠️ 주의사항

1. **API 키 보안**
   - 절대 GitHub에 API 키를 커밋하지 마세요
   - `.gitignore`에 `secrets.toml`이 포함되어 있는지 확인
   - API 키가 노출되면 즉시 재발급받으세요

2. **사용 한도**
   - OpenAI API의 Rate Limiting에 주의하세요
   - 과도한 사용 시 요금이 발생할 수 있습니다
   - API 사용량은 [OpenAI Dashboard](https://platform.openai.com/usage)에서 확인

3. **풀이의 한계**
   - AI 풀이는 참고용이며 전문가 상담을 대체하지 않습니다
   - 중요한 결정은 전문 명리학자와 상담하시기 바랍니다

## 🛠️ 문제 해결

### "OpenAI API 키가 설정되지 않았습니다" 오류
- `.streamlit/secrets.toml` 파일이 있는지 확인
- API 키 형식이 올바른지 확인
- Streamlit Cloud의 경우 Secrets 설정 확인

### "풀이 중 오류가 발생했습니다" 오류
- API 키가 유효한지 확인
- OpenAI 계정에 크레딧이 있는지 확인
- 네트워크 연결 상태 확인
- API Rate Limit 초과 여부 확인

### 앱이 느리게 실행됨
- AI 풀이는 10-20초 정도 소요됩니다
- 네트워크 상태에 따라 더 걸릴 수 있습니다
- 필요시 모델을 gpt-3.5-turbo로 변경하면 더 빠릅니다

## 📄 라이선스

이 프로젝트는 개인 및 비상업적 용도로 자유롭게 사용할 수 있습니다.

## 🤝 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다!

## 📞 문의

문제나 질문이 있으시면 GitHub Issues를 통해 문의해주세요.

---

**Made with ❤️ using Streamlit and OpenAI**
