"""
사주팔자 만세력 계산기 with OpenAI ChatGPT
Saju (Four Pillars) Calculator with AI Interpretation
"""
import streamlit as st
import secrets as secrets_module
from datetime import datetime
from typing import Optional
from saju_calculator import calculate_four_pillars, get_element_count

# OpenAI 임포트 (선택적)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Korean Lunar Calendar 임포트 (선택적)
try:
    from korean_lunar_calendar import KoreanLunarCalendar
    LUNAR_CALENDAR_AVAILABLE = True
except ImportError:
    LUNAR_CALENDAR_AVAILABLE = False

# 세션 상태 초기화
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# 인증되지 않은 경우 로그인 화면 표시
if not st.session_state.authenticated:
    st.set_page_config(page_title="사주풀이 - 로그인", page_icon="🔐")
    
    st.title("🔐 사주팔자 풀이")
    st.markdown("---")
    
    st.info("💡 이 서비스는 인증된 사용자만 이용 가능합니다.")
    
    password = st.text_input(
        "비밀번호를 입력하세요",
        type="password",
        placeholder="패스워드 입력"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        login_button = st.button("🔓 로그인", use_container_width=True)
    
    if login_button:
        if secrets_module.compare_digest(password, st.secrets["APP_PASSWORD"]):
            st.session_state.authenticated = True
            st.success("✅ 로그인 성공!")
            st.rerun()
        else:
            st.error("❌ 비밀번호가 틀렸습니다")
    
    st.markdown("---")
    st.caption("🔒 문의: 관리자에게 연락하세요")
    
    st.stop()

# 여기부터 기존 앱 코드 실행
# (인증된 사용자만 여기까지 도달)

# 페이지 설정
st.set_page_config(
    page_title="사주팔자 만세력 계산기",
    page_icon="🔮",
    layout="wide"
)


def lunar_to_solar(year, month, day, is_leap_month=False):
    """
    음력을 양력으로 변환
    
    Args:
        year (int): 음력 연도
        month (int): 음력 월
        day (int): 음력 일
        is_leap_month (bool): 윤달 여부
    
    Returns:
        dict: 양력 날짜 정보 {'year': int, 'month': int, 'day': int} 또는 None
    """
    try:
        calendar = KoreanLunarCalendar()
        # setLunarDate() automatically populates solarYear, solarMonth, and solarDay attributes
        calendar.setLunarDate(year, month, day, is_leap_month)
        
        return {
            'year': calendar.solarYear,
            'month': calendar.solarMonth,
            'day': calendar.solarDay
        }
    except Exception as e:
        st.error(f"음력 변환 중 오류: {e}")
        return None

st.title("🔮 사주팔자 만세력 계산기")
st.caption("생년월일시를 입력하면 사주팔자를 계산하고 AI가 풀이해드립니다.")

# 사이드바에 로그아웃 버튼 추가
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 로그아웃"):
        st.session_state.authenticated = False
        st.rerun()


def get_saju_interpretation(saju_result: dict, gender: str, occupation: str, student_grade: Optional[str] = None) -> str:
    """
    샘플 스타일의 자연스러운 사주 풀이
    """
    
    is_student = occupation == "학생" and student_grade is not None
    time_unknown = saju_result.get('hour_pillar') == '시간미상' or saju_result.get('time_unknown', False)
    
    # 시스템 프롬프트
    system_prompt = """당신은 30년 경력의 전문 사주명리학자입니다.

## 풀이 철학
- 점괘식 단정 대신 **성향/패턴/전략 중심**으로 설명
- 자연스러운 대화체 사용 ("~입니다", "~이에요", "~해요" 혼용)
- 화살표(→) 사용으로 인과관계 명확히
- 구체적 예시와 실제 상황 묘사
- 단정적 표현("반드시", "무조건") 최소화
- 공포 조장, 의료/법률 단정 금지

## 작성 스타일
- 공감하고 따뜻한 어조
- "그래서", "하지만", "또" 같은 자연스러운 연결어
- 중요 개념은 쌍따옴표(" ")로 강조
- 구체적 역할·상황 나열 시 중점(·) 사용
- 줄바꿈으로 읽기 쉽게 구성"""
    
    # 사용자 프롬프트
    user_prompt = f"""다음 사주팔자를 분석하여 아래 양식에 맞춰 자연스럽게 풀이해주세요.

## 생년월일시
{saju_result['birth_date']}
성별: {gender}
{'학년: ' + student_grade if is_student else '직업: ' + occupation}
{'⚠️ 출생시간 정보 없음 (시주 기반 해석은 확률 표현으로)' if time_unknown else ''}

## 사주팔자
- 연주(年柱): {saju_result['year_pillar']} ({saju_result['year_hanja']})
- 월주(月柱): {saju_result['month_pillar']} ({saju_result['month_hanja']})
- 일주(日柱): {saju_result['day_pillar']} ({saju_result['day_hanja']})
- 시주(時柱): {saju_result['hour_pillar']} ({saju_result['hour_hanja']})

## 오행 분포
{' '.join([f'{k}: {v}개' for k, v in saju_result['elements'].items()])}

## 십신(十神)
- 연간: {saju_result['sipsin']['year_stem']}
- 월간: {saju_result['sipsin']['month_stem']}
- 일간: {saju_result['sipsin']['day_stem']} (본인)
- 시간: {saju_result['sipsin']['hour_stem']}

## 신살(神殺)
- 천을귀인: {', '.join(saju_result['sinsal']['cheonul']) if saju_result['sinsal']['cheonul'] else '없음'}
- 역마살: {', '.join(saju_result['sinsal']['yeokma']) if saju_result['sinsal']['yeokma'] else '없음'}
- 도화살: {', '.join(saju_result['sinsal']['dohwa']) if saju_result['sinsal']['dohwa'] else '없음'}

---

# 풀이 양식

## 1. 핵심 성향 요약

{saju_result['day_pillar'][0]} 일간의 핵심 성향을 3개 문단으로 요약해주세요.

**작성 패턴:**
```
[일간 한자(음양오행)] 일간, [주요 오행·십신]이 [강함/약함] "[비유적 표현]" 기질입니다.

[대인관계나 책임감 특징]하는 편이지만, [겉과 속의 차이나 습관].

[가치관이나 행동 패턴]하면서도 [내면 특징], [관심사나 고민거리].
```

**예시:**
신금(辛金) 일간, 토 기운(정인·편인)이 아주 강한 "단단한 금" 기질입니다.

내 사람과 해야 할 일은 끝까지 책임지는 편이지만, 겉으로 힘들다고 잘 내색하지 않습니다.

체면과 원칙을 중시하면서도 속으로는 걱정·생각이 많고, 가족과 자식 문제에 마음을 많이 쓰는 형입니다.

---

## 2. 기질과 심리 패턴

### 강점

3가지 강점을 자연스럽게 설명하세요. 각 강점마다:

**작성 패턴:**
```
[사주 구조 설명]
→ [구체적 역할·능력을 중점으로 나열]

[일간이나 오행 특징] [비유적 표현]라
[구체적 행동 패턴이나 습관]

[역할이나 분야]에서 [장점이나 능력]
```

**예시:**
사주 전체가 토(金을 생하는 인성) + 금(본인)으로 튼튼합니다.
→ 공부·분석·정리, 남들 챙기는 역할, 집안의 "기둥 역할"에 강합니다.

신금은 세공된 보석 같은 기운이라 깔끔함·정확함·성실함이 큰 장점이에요.
맡은 일은 끝까지 책임지려 하고, 약속을 어지간해서는 어기지 않습니다.

대충 넘어가는 것을 잘 못 해서, 집안일·재정·건강 관리 등 체계 잡는 능력이 좋습니다.

### 약점

3가지 주의할 점을 자연스럽게 설명하세요.

**작성 패턴:**
```
[오행 불균형 설명],
"[부정적 패턴1]"을/를 [동사]하기 쉽고
[부정적 결과]로 이어지기 쉽습니다.

[십신이나 구조 특징]해서,
"[가치관이나 기준]"을/를 [행동 패턴]합니다.
그래서 [부정적 영향이나 갈등 상황].

[심리 패턴]하다가
정작 [본인 상태]하고 [결과]하기 쉽습니다.
```

**예시:**
토·금이 강하고 목·화가 없어서,
"나만의 방식·생각"을 고집하기 쉽고
몸과 마음의 탄력이 떨어지면 우울감·무기력으로 이어지기 쉽습니다.

관성(불 기운)이 약해,
"이렇게 살아야 한다"는 사회적 기준보다는 내 기준을 더 따르려 합니다.
그래서 때로는 권위나 규칙을 받아들이는 게 답답하거나,
반대로 너무 책임을 혼자 짊어지고 피곤해지기도 해요.

걱정이 많고, 혹시라도 남에게 민폐 끼칠까 조심하다가
정작 본인 마음은 잘 표현하지 못하고 속 앓이로 남기기 쉽습니다.

---

## 3. 인간관계 / 연애·부부 패턴

자연스러운 흐름으로 작성하세요.

**작성 패턴:**
```
[십신 특징]이 [위치]에 있어서, 관계에서도 "[특징적 표현]"의 [가치]를 중요하게 여깁니다.
→ [행동 패턴], [스타일 설명].

[십신이나 오행 특징]라,
[과거나 현재 연애·결혼 태도].

[관계에서의 애정 표현 방식].

[오행이나 지지 설명]라 [내면 특징]한데,
[겉으로 보이는 모습]할 수 있어요.
→ 그래서 "[오해받는 상황]"는 오해를 받지만, 사실은 [진실].

나이 들어갈수록,
[예상되는 관계 패턴이나 갈등].
[조언]하면 좋습니다.
```

**예시:**
비견(辛)이 월간에 떠 있어서, 관계에서도 "나는 나, 당신은 당신"의 거리를 중요하게 여깁니다.
→ 간섭은 싫지만, 정이 깊어지면 끝까지 챙기는 스타일.

관성이 약한 편이라,
젊을 때는 연애·결혼 자체보다 생활 안정·가족 책임을 더 먼저 생각했을 가능성이 큽니다.

---

## 4. 직업 / 재물 운용 스타일

자연스럽게 연결하여 작성하세요.

**작성 패턴:**
```
사주에 [십신 구성]하고, [재성·관성 상태]
"[큰 것]"보다는 [작지만 확실한 것]에 더 맞는 타입입니다.

적성으로 보면
- [직업군1]
- [직업군2]
- [직업군3]
같은 쪽이 잘 맞는 구조예요.

[재성 위치나 상태]라
→ [투자 스타일이나 재테크 방향].

지금 대운이 [오행 설명]라,
[현재 시기 재물·직업 방향].
```

---

## 5. 현재 시기 고민에 대한 해석

### 1) 원인

**작성 패턴:**
```
지금 운은 [오행이나 십신]이 [강해지는/약해지는] 흐름이라
→ [현실 상황]도, [심리 상태]는 시기입니다.

[구체적 고민 예시].
```

### 2) 패턴

**작성 패턴:**
```
원국 자체가 '[특징]' 구조라서
[반복되는 행동 패턴1]하거나
[반복되는 행동 패턴2]하는 패턴이 강합니다.

또, [일간 특징]은 "[심리 패턴]" 성향이 있어서
[인지 왜곡이나 감정 패턴].
```

### 3) 전략

**작성 패턴:**
```
지금부터의 운은, [하지 말아야 할 것]보다 "[해야 할 것]"에 더 유리합니다.

[약한 오행]한 사주라, [보완 방법]할수록 전체 운도 같이 살아나요.

앞으로 몇 년 사이에 [들어오는 오행] 기운이 들어오는 해들이 있어
→ 그 시기에는 [구체적 기회나 변화].
이때 [주의사항]하면, [긍정적 결과].
```

---

## 6. 지금부터 실천하면 좋은 조언 3가지

각 조언을 **제목 + 설명 + 이유/방법** 구조로 작성하세요.

**작성 패턴:**
```
**"[짧고 구체적인 행동]"**

[구체적인 실천 방법 2-3문장].

"[관점의 전환이나 프레임]"는 관점으로,
[심리적 정당화나 동기부여].
```

**예시:**
**"하루 한 번 나를 위한 시간"을 의도적으로 만들기**

최소 20~30분은 오직 나를 위해만 쓰는 시간을 정해 두세요.
(가벼운 스트레칭, 산책, 찜질방·반신욕, 좋아하는 드라마·책 등)

"가족을 위해서라도 내가 먼저 버텨야 한다"는 관점으로,
나를 챙기는 걸 이기심이 아니라 '책임'으로 정의해보면 마음이 덜 불편합니다.

{"" if not is_student else f'''
---

# 학생 전용 추가 풀이

## 7. 문과 / 이과 성향

[오행·십신 구성]으로 보면, [적성 분야] 쪽 적성이 [강함/약함/균형].

추천 전공:

**[학과명1]**
→ [사주적 근거], [발휘할 강점]

**[학과명2]**
→ [사주적 근거], [발휘할 강점]

**[학과명3]**
→ [사주적 근거], [발휘할 강점]

---

## 8. 잘하는 과목 / 취약한 과목

### 잘하는 과목

**[과목1]**: [이유와 특징]
**[과목2]**: [이유와 특징]
**[과목3]**: [이유와 특징]

### 취약한 과목

**[과목1]**: [이유와 특징]
**[과목2]**: [이유와 특징]

### 보완·강화 방법

[취약 과목 보완 전략]
[강한 과목 강화 방법]
[전체 학습 밸런스 조언]

---

## 9. 공부 방법

[자기주도학습/과외/대형학원] 중 [선택] 방식이 더 잘 맞는 타입이에요.

[이유와 사주적 근거]

[구체적 학습 전략]

---

## 10. 앞으로 3년간 시험운 / 학업운

### {datetime.now().year}년 (현재)

[세운 분석]
→ [시험운·학업 전망]
[전략]

### {datetime.now().year + 1}년

[세운 분석]
→ [시험운·학업 전망]
[전략]

### {datetime.now().year + 2}년

[세운 분석]
→ [시험운·학업 전망]
[전략]
'''}

---

# 중요 작성 원칙

1. **제목에 괄호 표시 금지**: "(3줄)", "(5-7문장)" 등 절대 출력하지 마세요
2. **자연스러운 대화체**: "~입니다", "~이에요", "~해요" 자연스럽게 혼용
3. **화살표(→) 적극 사용**: 인과관계나 결과 연결 시
4. **중점(·) 사용**: 나열 시 (예: 공부·분석·정리)
5. **쌍따옴표 강조**: 핵심 개념이나 패턴 (예: "나는 나")
6. **줄바꿈 활용**: 읽기 쉽게 적절히 나누기
7. **구체적 예시**: 추상적 표현보다 실제 상황 묘사

{"출생시간 없을 때: 시주 기반 해석은 '~할 가능성', '~한 경향' 등 확률 표현" if time_unknown else ""}

**금지 표현:**
- ❌ "반드시", "무조건", "절대"
- ❌ "질병이 생깁니다", "사고가 납니다"
- ❌ 제목에 "(3줄)", "(몇 문장)" 등 괄호 표시

**권장 표현:**
- ✅ "~한 경향", "~하기 쉽습니다"
- ✅ "~에 더 유리합니다", "~하면 도움이 됩니다"
- ✅ 화살표(→), 중점(·), 쌍따옴표(" ")"""
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=16000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"풀이 중 오류가 발생했습니다: {str(e)}"


def get_followup_answer(question: str, previous_interpretation: str, saju_info: str) -> str:
    """
    자연스러운 대화체의 추가 질문 답변
    """
    
    system_prompt = """당신은 30년 경력의 전문 사주명리학자입니다.

## 답변 스타일
- 자연스러운 대화체 ("~입니다", "~이에요", "~해요" 혼용)
- 화살표(→) 사용으로 인과관계 명확히
- 구체적 예시와 실제 상황 묘사
- 단정적 표현 최소화, 패턴/경향 중심
- 공포 조장·의료·법률 단정 금지"""
    
    user_prompt = f"""## 이전 풀이
{previous_interpretation}

## 사주 정보
{saju_info}

## 추가 질문
{question}

---

위 질문에 대해 자연스러운 대화체로 답변해주세요.

**작성 원칙:**
- 화살표(→) 사용으로 결과 연결
- 중점(·) 사용으로 나열
- 쌍따옴표로 핵심 강조
- "~한 경향", "~에 더 유리" 같은 패턴 표현
- 구체적 예시와 실천 방법 제시

5-8문장 정도로, 사주 요소를 구체적으로 언급하며 설명해주세요."""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=3000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"추가 질문 처리 중 오류가 발생했습니다: {str(e)}"


# 메인 UI
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📅 생년월일시 입력")
    
    # 달력 유형 선택
    calendar_type = st.radio(
        "달력 유형",
        options=['양력', '음력'],
        horizontal=True,
        help="생년월일을 양력으로 입력할지, 음력으로 입력할지 선택하세요."
    )
    
    birth_date = st.date_input(
        f"생년월일 ({calendar_type})",
        value=datetime(1990, 1, 1),
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2100, 12, 31)
    )
    
    # 음력 선택 시에만 윤달 옵션 표시 (생년월일 입력 아래)
    is_leap_month = False
    if calendar_type == "음력":
        if not LUNAR_CALENDAR_AVAILABLE:
            st.error("⚠️ 음력 변환 기능을 사용하려면 `korean-lunar-calendar` 라이브러리가 필요합니다.")
            st.stop()
        
        is_leap_month = st.checkbox(
            "윤달 (閏月)",
            value=False,
            help="윤달인 경우 체크하세요"
        )
    
    # 시간 모름 체크박스 추가
    time_unknown = st.checkbox(
        "⏰ 출생 시간을 모르겠어요",
        value=False,
        help="시간을 모르시면 년주, 월주, 일주만으로 풀이합니다."
    )
    
    if time_unknown:
        st.info("💡 시주(時柱) 없이 3주(年月日)만으로 풀이합니다. 시간을 알면 더 정확한 풀이가 가능합니다.")
        # 기본 시간 설정 (정오 12시로 설정하되, 시주 계산은 건너뜀)
        birth_hour = 12
        birth_minute = 0
    else:
        # 시간 입력 (1분 단위)
        st.write("#### 출생 시간")
        col_time1, col_time2 = st.columns(2)
        with col_time1:
            birth_hour = st.number_input(
                "시간 (Hour)",
                min_value=0,
                max_value=23,
                value=12,
                step=1,
                help="0시~23시 사이 선택"
            )
        with col_time2:
            birth_minute = st.number_input(
                "분 (Minute)",
                min_value=0,
                max_value=59,
                value=0,
                step=1,
                help="0분~59분 사이 선택"
            )
    
    gender = st.radio(
        "성별",
        options=['남', '여'],
        horizontal=True
    )
    
    # 직업/학생 선택
    occupation_type = st.selectbox(
        "구분",
        options=['일반', '학생'],
        help="학생인 경우 '학생'을 선택하면 맞춤형 풀이를 받을 수 있습니다."
    )
    
    # 학생 선택 시 학년 입력
    grade_level = ""
    if occupation_type == "학생":
        grade_level = st.selectbox(
            "학년",
            options=['초등학생', '중학생', '고등학생', '대학생', '대학원생'],
            help="현재 학년을 선택해주세요."
        )
    
    # datetime 객체 생성 (일단 입력된 날짜로 생성, 음력인 경우 아래에서 변환)
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day
    
    if st.button("🔮 사주팔자 계산하기", type="primary", use_container_width=True):
        # 음력인 경우 양력으로 변환
        if calendar_type == "음력":
            st.info(f"🌙 음력 입력: {year}년 {month}월 {day}일 {'(윤달)' if is_leap_month else ''}")
            
            solar_result = lunar_to_solar(year, month, day, is_leap_month)
            
            if solar_result:
                year = solar_result['year']
                month = solar_result['month']
                day = solar_result['day']
                
                st.success(f"📌 변환된 양력: {year}년 {month}월 {day}일")
            else:
                st.error("음력 변환에 실패했습니다. 입력 값을 확인해주세요.")
                st.stop()
        
        # 양력 날짜로 datetime 객체 생성
        birth_datetime = datetime(year, month, day, birth_hour, birth_minute)
        
        # 이전 생년월일과 다르면 대화 히스토리 초기화
        if 'birth_datetime' in st.session_state and st.session_state['birth_datetime'] != birth_datetime:
            st.session_state['conversation_history'] = []
        
        st.session_state['saju_calculated'] = True
        st.session_state['birth_datetime'] = birth_datetime
        st.session_state['gender'] = gender
        st.session_state['occupation'] = occupation_type
        st.session_state['is_student'] = (occupation_type == "학생")
        st.session_state['grade_level'] = grade_level if occupation_type == "학생" else ""
        st.session_state['time_unknown'] = time_unknown
        # 대화 히스토리 초기화 (첫 계산 시에만)
        if 'conversation_history' not in st.session_state:
            st.session_state['conversation_history'] = []

with col2:
    st.subheader("ℹ️ 안내사항")
    st.info(
        "**사주팔자란?**\n\n"
        "태어난 년(年), 월(月), 일(日), 시(時)를 "
        "천간(天干)과 지지(地支)로 표현한 것으로, "
        "총 8개의 글자로 구성됩니다.\n\n"
        "**음력/양력 입력**\n\n"
        "음력 생일인 경우 '음력'을 선택하면 자동으로 양력으로 변환됩니다. "
        "윤달인 경우 '윤달' 체크박스를 선택하세요.\n\n"
        "**AI 풀이 기능**\n\n"
        "OpenAI ChatGPT를 활용하여 전문적인 사주 해석을 제공합니다."
    )

# 사주 계산 결과 표시
if st.session_state.get('saju_calculated', False):
    birth_datetime = st.session_state['birth_datetime']
    gender = st.session_state.get('gender', '남')
    time_unknown = st.session_state.get('time_unknown', False)
    
    with st.spinner("사주팔자를 계산하는 중..."):
        result = calculate_four_pillars(birth_datetime, gender, include_hour=not time_unknown)
    
    st.success(f"✅ {result['birth_date']} 출생자의 사주팔자")
    
    # 시간 미상 경고 메시지
    if result.get('time_unknown', False):
        st.warning("⚠️ 출생 시간을 모르시는 경우입니다. 년주, 월주, 일주만으로 풀이했습니다.")
    
    # 사주팔자 표시
    st.subheader("📊 사주팔자 (四柱八字)")
    
    cols = st.columns(4)
    pillars = [
        ("연주(年柱)", result['year_pillar'], result['year_hanja']),
        ("월주(月柱)", result['month_pillar'], result['month_hanja']),
        ("일주(日柱)", result['day_pillar'], result['day_hanja']),
        ("시주(時柱)", result['hour_pillar'], result['hour_hanja'])
    ]
    
    for col, (title, pillar, hanja) in zip(cols, pillars):
        with col:
            if title == "시주(時柱)" and result.get('time_unknown', False):
                st.metric(label=title, value=pillar, help="출생 시간을 모르는 경우")
            else:
                st.metric(label=title, value=pillar)
            st.caption(f"한자: {hanja}")
    
    # 오행 분석
    st.subheader("🌟 오행 분석 (五行)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**천간(天干) 오행:**")
        stem_labels = ['연간', '월간', '일간', '시간'] if not result.get('time_unknown', False) else ['연간', '월간', '일간']
        for i, (stem, element) in enumerate(zip(stem_labels, result['stems_elements'])):
            st.write(f"- {stem}: {element}")
    
    with col2:
        st.write("**지지(地支) 오행:**")
        branch_labels = ['연지', '월지', '일지', '시지'] if not result.get('time_unknown', False) else ['연지', '월지', '일지']
        for i, (branch, element) in enumerate(zip(branch_labels, result['branches_elements'])):
            st.write(f"- {branch}: {element}")
    
    # 오행 개수 통계
    element_count = get_element_count(result)
    st.write("**오행 개수:**")
    if result.get('time_unknown', False):
        st.caption("※ 시주가 없어 오행 분포가 불완전할 수 있습니다.")
    element_cols = st.columns(5)
    for col, (element, count) in zip(element_cols, element_count.items()):
        with col:
            st.metric(label=element, value=f"{count}개")
    
    # 십신 분석
    if 'sipsin' in result:
        st.subheader("🎭 십신 분석 (十神)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**천간 십신:**")
            st.write(f"- 년간: {result['sipsin']['year_stem']}")
            st.write(f"- 월간: {result['sipsin']['month_stem']}")
            st.write(f"- 일간: {result['sipsin']['day_stem']}")
            st.write(f"- 시간: {result['sipsin']['hour_stem']}")
        
        with col2:
            st.write("**지지 십신:**")
            st.write(f"- 년지: {result['sipsin']['year_branch']}")
            st.write(f"- 월지: {result['sipsin']['month_branch']}")
            st.write(f"- 일지: {result['sipsin']['day_branch']}")
            st.write(f"- 시지: {result['sipsin']['hour_branch']}")
    
    # 12운성
    if 'unsung' in result:
        st.subheader("⭐ 12운성 (十二運星)")
        unsung_cols = st.columns(4)
        unsung_data = [
            ('년지', result['unsung']['year']),
            ('월지', result['unsung']['month']),
            ('일지', result['unsung']['day']),
            ('시지', result['unsung']['hour'])
        ]
        for col, (pos, unsung) in zip(unsung_cols, unsung_data):
            with col:
                st.info(f"**{pos}**: {unsung}")
    
    # 신살
    if 'sinsal' in result:
        st.subheader("🔯 신살 (神殺)")
        sinsal_data = []
        if result['sinsal']['cheonul']:
            sinsal_data.append(('천을귀인', result['sinsal']['cheonul'], 'success'))
        if result['sinsal']['yeokma']:
            sinsal_data.append(('역마살', result['sinsal']['yeokma'], 'info'))
        if result['sinsal']['dohwa']:
            sinsal_data.append(('도화살', result['sinsal']['dohwa'], 'info'))
        if result['sinsal']['gongmang']:
            sinsal_data.append(('공망', result['sinsal']['gongmang'], 'warning'))
        if result['sinsal']['wonjin']:
            sinsal_data.append(('원진', result['sinsal']['wonjin'], 'warning'))
        if result['sinsal']['yangin']:
            sinsal_data.append(('양인', result['sinsal']['yangin'], 'warning'))
        
        if sinsal_data:
            for name, positions, style in sinsal_data:
                if style == 'success':
                    st.success(f"**{name}**: {', '.join(positions)}")
                elif style == 'info':
                    st.info(f"**{name}**: {', '.join(positions)}")
                else:
                    st.warning(f"**{name}**: {', '.join(positions)}")
        else:
            st.info("특별한 신살이 없습니다.")
    
    # 형충회합
    if 'hyungchunghap' in result:
        st.subheader("⚡ 형충회합 (刑沖會合)")
        
        hch = result['hyungchunghap']
        col1, col2 = st.columns(2)
        
        with col1:
            if hch['chung']:
                st.error(f"**충(沖)**: {', '.join(hch['chung'])}")
            else:
                st.info("**충(沖)**: 없음")
            
            if hch['hyung']:
                st.warning(f"**형(刑)**: {', '.join(hch['hyung'])}")
            else:
                st.info("**형(刑)**: 없음")
        
        with col2:
            if hch['yukhap']:
                st.success(f"**육합(六合)**: {', '.join(hch['yukhap'])}")
            else:
                st.info("**육합(六合)**: 없음")
            
            if hch['samhap']:
                st.success(f"**삼합(三合)**: {', '.join(hch['samhap'])}")
            else:
                st.info("**삼합(三合)**: 없음")
    
    # 납음오행
    if 'napeum' in result:
        with st.expander("🎨 납음오행 (納音五行)"):
            napeum_cols = st.columns(4)
            napeum_data = [
                ('년주', result['napeum']['year']),
                ('월주', result['napeum']['month']),
                ('일주', result['napeum']['day']),
                ('시주', result['napeum']['hour'])
            ]
            for col, (pos, napeum) in zip(napeum_cols, napeum_data):
                with col:
                    st.write(f"**{pos}**: {napeum}")
    
    # 대운
    if 'daeun' in result:
        st.subheader("🔮 대운 (大運)")
        st.caption(f"{result['daeun']['start_age']}세부터 시작, {result['daeun']['direction']}")
        
        import pandas as pd
        daeun_df = pd.DataFrame(result['daeun']['list'])
        st.dataframe(daeun_df, use_container_width=True, hide_index=True)
    
    # 세운
    if 'seun' in result:
        st.subheader("📅 세운 (歲運)")
        current_year = result['seun']['current']['년도']
        current_jiazi = result['seun']['current']['간지']
        current_age = result['seun']['current']['나이']
        
        st.info(f"**현재**: {current_year}년 {current_jiazi} ({current_age}세)")
        
        with st.expander("세운표 보기"):
            for seun in result['seun']['list']:
                marker = " ← 현재" if seun['현재'] else ""
                prefix = "**" if seun['현재'] else ""
                suffix = "**" if seun['현재'] else ""
                st.text(f"{prefix}{seun['년도']}년 {seun['간지']} ({seun['나이']}세){suffix}{marker}")
    
    st.divider()
    
    # 음양 분석
    with st.expander("☯️ 음양 분석"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**천간 음양:**")
            for stem, yy in zip(['연간', '월간', '일간', '시간'], result['stems_yin_yang']):
                st.write(f"- {stem}: {yy}")
        with col2:
            st.write("**지지 음양:**")
            for branch, yy in zip(['연지', '월지', '일지', '시지'], result['branches_yin_yang']):
                st.write(f"- {branch}: {yy}")
    
    st.divider()
    
    # AI 풀이 버튼
    # API 키 확인
    api_key_available = False
    try:
        if OPENAI_AVAILABLE and "OPENAI_API_KEY" in st.secrets:
            api_key_available = True
    except:
        pass
    
    if not OPENAI_AVAILABLE:
        st.warning("⚠️ OpenAI 라이브러리가 설치되지 않았습니다. `pip install openai`를 실행해주세요.")
    elif not api_key_available:
        st.warning(
            "⚠️ OpenAI API 키가 설정되지 않았습니다.\n\n"
            "Streamlit Cloud에서 배포 시 Settings → Secrets에서 다음과 같이 설정해주세요:\n\n"
            "```toml\n"
            "OPENAI_API_KEY = \"sk-...\"\n"
            "```\n\n"
            "로컬 실행 시 `.streamlit/secrets.toml` 파일을 생성하여 설정하세요."
        )
    else:
        if st.button("🔮 AI 사주풀이 보기", type="primary", use_container_width=True):
            with st.spinner("AI가 사주를 풀이하는 중... (약 10-20초 소요)"):
                # OpenAI 클라이언트 초기화
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                
                # 사주 풀이를 위한 정보 가져오기
                gender = st.session_state.get('gender', '남')
                occupation = st.session_state.get('occupation', '일반')
                student_grade = st.session_state.get('grade_level', None)
                
                interpretation = get_saju_interpretation(result, gender, occupation, student_grade)
                
                st.session_state['interpretation'] = interpretation
                st.session_state['saju_result'] = result
        
        # 풀이 결과 표시
        if 'interpretation' in st.session_state:
            st.markdown("### 📖 AI 사주 풀이")
            st.markdown(st.session_state['interpretation'])
            
            # 다운로드 버튼
            download_text = f"""
사주팔자 만세력 계산 결과
==================

생년월일시: {result['birth_date']}

사주팔자
-------
- 연주(年柱): {result['year_pillar']} ({result['year_hanja']})
- 월주(月柱): {result['month_pillar']} ({result['month_hanja']})
- 일주(日柱): {result['day_pillar']} ({result['day_hanja']})
- 시주(時柱): {result['hour_pillar']} ({result['hour_hanja']})

오행 분석
--------
천간: {', '.join(result['stems_elements'])}
지지: {', '.join(result['branches_elements'])}

AI 사주 풀이
-----------
{st.session_state['interpretation']}

※ 본 풀이는 AI에 의해 자동 생성된 것으로 참고용입니다.
"""
            
            st.download_button(
                label="📥 풀이 결과 다운로드",
                data=download_text.encode('utf-8'),
                file_name=f"사주풀이_{birth_datetime.strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            st.divider()
            
            # 추가 질문 기능
            st.markdown("### 💬 추가 질문하기")
            st.caption("사주와 관련하여 궁금한 점을 더 물어보세요. 이전 대화 내용이 유지됩니다.")
            
            # 추가 질문 입력
            user_question = st.text_input(
                "질문을 입력하세요",
                key="followup_question",
                placeholder="예: 올해 이직하기 좋은 시기는 언제인가요?"
            )
            
            if st.button("📤 질문하기", use_container_width=True):
                if user_question.strip():
                    with st.spinner("답변을 생성하는 중..."):
                        # OpenAI API 키 설정
                        openai.api_key = st.secrets["OPENAI_API_KEY"]
                        
                        # 사주 정보 문자열 생성
                        saju_result = st.session_state['saju_result']
                        element_count = get_element_count(saju_result)
                        elements_str = ' '.join([f'{k}: {v}개' for k, v in element_count.items()])
                        saju_info = f"""## 생년월일시
{saju_result['birth_date']}

## 사주팔자
- 연주: {saju_result['year_pillar']} ({saju_result['year_hanja']})
- 월주: {saju_result['month_pillar']} ({saju_result['month_hanja']})
- 일주: {saju_result['day_pillar']} ({saju_result['day_hanja']})
- 시주: {saju_result['hour_pillar']} ({saju_result['hour_hanja']})

## 오행: {elements_str}"""
                        
                        # 이전 풀이 가져오기
                        previous_interpretation = st.session_state.get('interpretation', '')
                        
                        # 답변 생성
                        answer = get_followup_answer(
                            user_question,
                            previous_interpretation,
                            saju_info
                        )
                        
                        # 대화 히스토리에 추가
                        st.session_state['conversation_history'].append({
                            'question': user_question,
                            'answer': answer
                        })
                        
                        # 답변 표시를 위해 rerun
                        st.rerun()
                else:
                    st.warning("질문을 입력해주세요.")
            
            # 최신 답변 표시 (답변이 있을 때만)
            if st.session_state.get('conversation_history', []):
                latest = st.session_state['conversation_history'][-1]
                st.markdown("#### 💡 답변")
                st.info(f"**Q: {latest['question']}**")
                st.markdown(latest['answer'])
                
                # 이전 대화 내역이 2개 이상일 때만 히스토리 표시
                if len(st.session_state['conversation_history']) > 1:
                    with st.expander(f"📜 이전 대화 내역 보기 ({len(st.session_state['conversation_history']) - 1}개)", expanded=False):
                        for idx, conv in enumerate(st.session_state['conversation_history'][:-1], 1):
                            st.markdown(f"**Q{idx}: {conv['question']}**")
                            st.markdown(f"A{idx}: {conv['answer']}")
                            if idx < len(st.session_state['conversation_history']) - 1:
                                st.markdown("---")

# 푸터
st.divider()
st.caption("💡 본 서비스는 참고용이며, 전문가의 상담을 대체할 수 없습니다.")
st.caption("🤖 AI 풀이는 OpenAI GPT-4o 모델을 사용하며, API 비용이 발생할 수 있습니다.")
