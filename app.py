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
    GPT-4o 모델을 사용한 사주팔자 풀이 (성향/패턴/전략 중심)
    """
    
    is_student = occupation == "학생" and student_grade is not None and student_grade != ""
    time_unknown = saju_result.get('time_unknown', False) or saju_result.get('hour_pillar') == '시간미상'
    
    # 오행 개수 계산
    element_count = get_element_count(saju_result)
    elements_str = ' '.join([f'{k}: {v}개' for k, v in element_count.items()])
    
    # 시스템 프롬프트
    system_prompt = """당신은 30년 경력의 전문 사주명리학자입니다.

## 풀이 철학
- 점괘식 단정 대신 **성향/패턴/전략 중심**으로 설명합니다
- 내담자가 **자기 이해와 행동 계획**을 얻도록 돕습니다
- "반드시/무조건" 같은 단정적 표현은 최소화합니다
- 공포 조장, 의료/법률 단정은 절대 하지 않습니다

## 작성 스타일
- 공감하고 따뜻한 어조
- 구체적이고 실천 가능한 조언
- 장단점을 균형있게 설명
- 희망적이면서도 현실적인 메시지"""
    
    # 학생 모드인 경우 나이 정보 추출
    current_age_raw = saju_result.get('seun', {}).get('current', {}).get('나이', '-')
    # 나이를 정수로 변환 시도, 실패하면 '-'로 설정
    try:
        current_age = int(current_age_raw) if current_age_raw != '-' else '-'
    except (ValueError, TypeError):
        current_age = '-'
    
    # 사용자 프롬프트
    occupation_info = f'학년: {student_grade}' if is_student else f'직업: {occupation}'
    current_year = datetime.now().year
    
    user_prompt = f"""다음 사주팔자를 분석하여 아래 양식에 맞춰 풀이해주세요.

## 생년월일시
{saju_result['birth_date']}
성별: {gender}
{occupation_info}
{'⚠️ 출생시간 정보 없음 (시주 기반 해석은 확률로 표현)' if time_unknown else ''}

## 사주팔자
- 연주(年柱): {saju_result['year_pillar']} ({saju_result['year_hanja']})
- 월주(月柱): {saju_result['month_pillar']} ({saju_result['month_hanja']})
- 일주(日柱): {saju_result['day_pillar']} ({saju_result['day_hanja']})
- 시주(時柱): {saju_result['hour_pillar']} ({saju_result['hour_hanja']})

## 오행 분포
{elements_str}

## 십신(十神)
- 연간: {saju_result.get('sipsin', {}).get('year_stem', '-')}
- 월간: {saju_result.get('sipsin', {}).get('month_stem', '-')}
- 일간: {saju_result.get('sipsin', {}).get('day_stem', '-')} (본인)
- 시간: {saju_result.get('sipsin', {}).get('hour_stem', '-')}

## 신살(神殺)
- 천을귀인: {', '.join(saju_result.get('sinsal', {}).get('cheonul', [])) if saju_result.get('sinsal', {}).get('cheonul') else '없음'}
- 역마살: {', '.join(saju_result.get('sinsal', {}).get('yeokma', [])) if saju_result.get('sinsal', {}).get('yeokma') else '없음'}
- 도화살: {', '.join(saju_result.get('sinsal', {}).get('dohwa', [])) if saju_result.get('sinsal', {}).get('dohwa') else '없음'}

---

# 풀이 양식

## 1. 핵심 성향 요약 (3줄)
일간 {saju_result['day_pillar'][0]}을 중심으로 이 사주의 핵심 성향을 3가지로 요약해주세요.
- 1줄: [가장 두드러진 성향]
- 2줄: [주요 강점이나 특성]
- 3줄: [주의할 점이나 과제]

각 줄은 한 문장으로, 구체적이고 이해하기 쉽게 작성하세요.

---

## 2. 기질과 심리 패턴

### 기본 기질 (5-7문장)
- 일간과 월지, 일지를 중심으로 타고난 기질을 설명하세요
- 오행 균형/불균형이 성격에 미치는 영향을 구체적으로 설명하세요
- "~한 경향이 있습니다", "~한 면이 강합니다" 같은 패턴 중심 표현 사용

### 강점 (3가지, 각 2-3문장)
**강점 1: [제목]**
- [구체적 설명과 실제 상황 예시]

**강점 2: [제목]**
- [구체적 설명과 실제 상황 예시]

**강점 3: [제목]**
- [구체적 설명과 실제 상황 예시]

### 약점/주의할 점 (3가지, 각 2-3문장)
**주의할 점 1: [제목]**
- [구체적 설명]
- [개선 전략: "~하면 도움이 될 수 있습니다"]

**주의할 점 2: [제목]**
- [구체적 설명]
- [개선 전략: "~을 시도해볼 만합니다"]

**주의할 점 3: [제목]**
- [구체적 설명]
- [개선 전략: "~하는 것을 고려해보세요"]

---

## 3. 인간관계 / 연애 패턴

### 인간관계 스타일 (5-7문장)
- 십신 구성(비겁, 식상, 재성, 관성, 인성)을 바탕으로 관계 맺는 방식 설명
- 도화살, 역마살이 있다면 관계에서의 특징 언급
- 잘 맞는 사람 유형 2-3가지 제시
- 관계에서 주의할 패턴 설명

### 연애 패턴 (5-7문장)
- 재성/관성을 중심으로 연애 스타일 설명
- 이상형의 특징 (구체적으로)
- 연애할 때 나타나는 패턴
- 좋은 관계를 위한 조언 ("~하면 더 좋은 관계를 만들 수 있습니다")

---

## 4. 직업 / 재물 운용 스타일

### 직업·진로 성향 (6-8문장)
- 월지와 시지의 십신을 중심으로 업무 스타일 설명
- 오행과 신살을 바탕으로 적합한 직업 분야 3-5가지 제시
- 조직 vs 독립 적성 설명
- 커리어에서 성공하기 위한 전략 제시

### 돈·재물 감각 (5-7문장)
- 재성의 유무와 위치로 재물운 패턴 설명
- 돈을 버는 방식과 쓰는 방식의 특징
- 재테크 스타일 (안정형/공격형/균형형)
- 재물 관리 조언 ("~하면 재물을 지키는 데 도움이 됩니다")

---

## 5. 현재 고민에 대한 해석

### 원인 (3-4문장)
- 현재 세운과 대운을 바탕으로 지금 시기의 특징 설명
- 왜 이런 고민이 생기는지 사주적 배경 설명

### 반복되는 패턴 (3-4문장)
- 사주 구조상 반복될 가능성이 있는 패턴 설명
- 이 패턴이 나타나는 근본 원인

### 전략 (4-5문장)
- 이 시기를 어떻게 보내면 좋을지 구체적 전략 제시
- "~할 때입니다" 대신 "~하면 도움이 될 것으로 보입니다" 사용

---

## 6. 실천 조언 3가지

**조언 1: [제목]**
- [구체적이고 실천 가능한 행동 지침]
- [왜 이것이 도움이 되는지 간단히 설명]

**조언 2: [제목]**
- [구체적이고 실천 가능한 행동 지침]
- [왜 이것이 도움이 되는지 간단히 설명]

**조언 3: [제목]**
- [구체적이고 실천 가능한 행동 지침]
- [왜 이것이 도움이 되는지 간단히 설명]

{"" if not is_student else f'''
---

# 학생 전용 추가 풀이

## 7. 문과 / 이과 성향

### 진로 적성 (4-5문장)
- 오행과 십신 구성으로 문과/이과/예체능 적성 분석
- 구체적인 이유와 근거 제시

### 전공 추천 (3가지, 각 2-3문장)
**추천 1: [구체적 학과명]**
- [왜 적합한지 사주적 근거]
- [이 분야에서 어떤 강점을 발휘할 수 있는지]

**추천 2: [구체적 학과명]**
- [왜 적합한지 사주적 근거]
- [이 분야에서 어떤 강점을 발휘할 수 있는지]

**추천 3: [구체적 학과명]**
- [왜 적합한지 사주적 근거]
- [이 분야에서 어떤 강점을 발휘할 수 있는지]

---

## 8. 잘하는 과목들 / 취약한 과목들

### 잘하는 과목들 (3-4과목, 각 2문장)
**[구체적 과목명 1]**: [이유와 특징]
**[구체적 과목명 2]**: [이유와 특징]
**[구체적 과목명 3]**: [이유와 특징]

### 취약한 과목들 (2-3과목, 각 2문장)
**[구체적 과목명 1]**: [이유와 특징]
**[구체적 과목명 2]**: [이유와 특징]

### 보완·강화 방법 (5-6문장)
- 취약 과목 보완 전략 2가지
- 강한 과목 더 강화하는 방법 1가지
- 전체적인 학습 밸런스 조언

---

## 9. 공부 방법

### 최적의 학습 환경 (4-5문장)
- 자기주도학습 / 과외 / 대형학원 중 적합한 방식 선택
- 왜 그 방식이 적합한지 사주적 근거 설명
- 각 방식의 장단점을 이 사주에 맞춰 설명

### 효과적인 공부 전략 (5-6문장)
- 집중력 패턴 (아침형/저녁형, 단기집중/장기지구력)
- 암기 vs 이해 중 어느 쪽이 강한지
- 혼자 vs 함께 중 어느 환경이 좋은지
- 구체적인 공부 시간 배분 조언

---

## 10. 앞으로 3년간 시험운 / 학업운

### {current_year}년 (현재, {current_age}세)
- [현재 세운 분석 3-4문장]
- [시험운과 학업 성취 가능성]
- [이 시기 전략: "~하면 좋은 결과를 기대할 수 있습니다"]

### {current_year + 1}년 ({current_age + 1 if isinstance(current_age, int) else '-'}세)
- [다음 해 세운 분석 3-4문장]
- [시험운과 학업 성취 가능성]
- [이 시기 전략]

### {current_year + 2}년 ({current_age + 2 if isinstance(current_age, int) else '-'}세)
- [다다음 해 세운 분석 3-4문장]
- [시험운과 학업 성취 가능성]
- [이 시기 전략]
'''}

---

# 중요 지침

1. **출생시간 없을 때**: {"시주 기반 해석은 '~일 가능성이 높습니다', '~한 경향을 보일 수 있습니다'처럼 확률 표현 사용" if time_unknown else "시주 정보 있음 - 정확히 분석"}

2. **금지 표현**:
   - ❌ "반드시 ~해야 합니다"
   - ❌ "무조건 ~입니다"
   - ❌ "절대 ~하지 마세요"
   - ❌ "질병이 생깁니다"
   - ❌ "사고가 날 것입니다"
   
3. **권장 표현**:
   - ✅ "~한 경향이 있습니다"
   - ✅ "~하면 도움이 될 수 있습니다"
   - ✅ "~을 고려해보시면 좋겠습니다"
   - ✅ "~한 패턴이 보입니다"

4. **구체성**: 모든 조언은 실천 가능한 구체적 행동으로 표현

5. **균형**: 장점과 단점을 균형있게, 희망적이되 현실적으로

6. **공감**: 따뜻하고 이해하는 어조 유지"""
    
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
    추가 질문 답변 (성향/패턴/전략 중심)
    """
    
    system_prompt = """당신은 30년 경력의 전문 사주명리학자입니다.

## 답변 원칙
- 점괘식 단정 대신 **성향/패턴/전략 중심**으로 답변
- 단정적 표현("반드시/무조건") 최소화
- 공포 조장, 의료/법률 단정 금지
- 구체적이고 실천 가능한 조언 제공"""
    
    user_prompt = f"""## 이전 풀이
{previous_interpretation}

## 사주 정보
{saju_info}

## 추가 질문
{question}

---

위 질문에 대해 다음 원칙으로 답변해주세요:

1. **성향/패턴 중심**: "~할 가능성이 높습니다", "~한 경향이 있습니다"
2. **전략 제시**: "~하면 도움이 될 것입니다", "~을 고려해보세요"
3. **구체적 조언**: 실천 가능한 행동 지침 제공
4. **금지 표현**: "반드시", "무조건", "절대" 사용 금지

답변은 5-7문장으로, 사주 요소를 구체적으로 언급하며 설명해주세요."""

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
