"""
사주팔자 만세력 계산기 with OpenAI ChatGPT
Saju (Four Pillars) Calculator with AI Interpretation
"""
import streamlit as st
from datetime import datetime, time
from saju_calculator import (
    calculate_four_pillars, 
    get_element_count,
    lunar_to_solar,
    calculate_jijanggan,
    format_sipsin_distribution,
    format_current_daeun,
    format_daeun_table,
    format_gwiin_list,
    format_sal_list
)

# OpenAI 임포트 (선택적)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# 페이지 설정
st.set_page_config(
    page_title="AI 사주팔자 만세력",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 AI 사주팔자 만세력")
st.caption("생년월일시를 입력하면 사주팔자를 계산하고 AI가 풀이해드립니다.")


def get_comprehensive_saju_interpretation(result: dict, gender: str, is_student: bool = False) -> str:
    """전문가 수준의 상세 사주풀이"""
    
    # 일간 해석 매핑
    ILGAN_INTERPRETATION = {
        '甲': '큰 나무처럼 곧고 강인한 기질',
        '乙': '풀과 같이 유연하고 적응력 있는 기질',
        '丙': '태양과 같이 밝고 적극적인 기질',
        '丁': '촛불과 같이 섬세하고 따뜻한 기질',
        '戊': '산과 같이 안정적이고 중후한 기질',
        '己': '평야와 같이 너그럽고 포용력 있는 기질',
        '庚': '쇠와 같이 강하고 결단력 있는 기질',
        '辛': '보석과 같이 날카롭고 정교한 기질',
        '壬': '대양과 같이 광활하고 포용력 있는 기질',
        '癸': '이슬과 같이 섬세하고 지혜로운 기질'
    }
    
    # 일간 한자 추출
    day_hanja = result.get('day_hanja', '')
    ilgan = day_hanja[0] if day_hanja else ''
    ilgan_desc = ILGAN_INTERPRETATION.get(ilgan, '독특한 기질')
    
    # 지장간 계산
    jijanggan = calculate_jijanggan(result)
    
    # 오행 개수
    element_count = get_element_count(result)
    
    # 현재 연도
    current_year = datetime.now().year
    birth_year = result.get('birth_year', current_year)
    
    # 학생 전용 섹션
    student_section = ""
    if is_student:
        student_section = f"""

## 🎓 학생 전용 분석

### A. 연도별 학업운 및 시험운 흐름
- {current_year-2}년: 학업운 분석
- {current_year-1}년: 학업운 분석
- {current_year}년 (현재): 학업운 분석
- {current_year+1}년: 학업운 분석
- {current_year+2}년: 학업운 분석

각 연도별로:
- 집중력 및 암기력 상태
- 중요 시험 시기 (수능, 내신 등)
- 주의할 달/시기
- 학업 성취도 전망

### B. 학습 스타일 분석
**자기주도 학습 적합도:**
- 자기주도 학습 가능 여부 (상/중/하)
- 이유: (사주 구조 기반 설명)

**추천 학습 방법:**
- ✅ 적합: 과외 / 학원 / 자습 / 인강 / 스터디 그룹
- ❌ 부적합: 그 이유

**집중력 및 학습 패턴:**
- 집중 가능 시간대
- 효율적인 학습 방식 (시각형/청각형/체험형)
- 주의 산만 극복 방법

### C. 진로 적성 및 전공 추천

**타고난 재능 및 적성:**
- 강점 분야 (논리/언어/예술/사회성/실무 등)
- 약점 분야 및 보완 방법

**추천 전공 (우선순위):**
1. [전공명] - 이유: ...
2. [전공명] - 이유: ...
3. [전공명] - 이유: ...

**추천 진로 분야:**
- 대분류: (예: 이공계, 인문사회, 예체능)
- 구체적 직업 예시: ...
- 30대 이후 전망: ...

**비추천 분야:**
- 피해야 할 분야 및 이유
"""
    
    prompt = f"""
당신은 30년 경력의 전문 사주명리학자입니다.
아래 사주를 전문가 관점에서 깊이 있고 체계적으로 풀이해주세요.

---

## 1. 기본 정보
- **생년월일**: {birth_year}년 {result.get('birth_month', '?')}월 {result.get('birth_day', '?')}일
- **성별**: {gender}
- **출생시간**: {result.get('birth_hour', 0):02d}시 {result.get('birth_minute', 0):02d}분
{'- **학생 여부**: 예' if is_student else ''}

---

## 2. 사주 구성

### 사주팔자
```
시주   일주   월주   년주
{result['hour_hanja']}   {result['day_hanja']}   {result['month_hanja']}   {result['year_hanja']}
(시)   (일)   (월)   (년)
```

### 천간 (天干)
- 년간: {result['year_stem']} ({result['stems_elements'][0]})
- 월간: {result['month_stem']} ({result['stems_elements'][1]})
- 일간: {result['day_stem']} ({result['stems_elements'][2]}) ← 나 자신
- 시간: {result['hour_stem']} ({result['stems_elements'][3]})

### 지지 (地支)
- 년지: {result['year_branch']} ({result['branches_elements'][0]})
- 월지: {result['month_branch']} ({result['branches_elements'][1]})
- 일지: {result['day_branch']} ({result['branches_elements'][2]})
- 시지: {result['hour_branch']} ({result['branches_elements'][3]})

### 지장간 요약
{jijanggan}

### 일간 해석
일간 {ilgan}는 **{ilgan_desc}**을 의미합니다.
이 일간이 사주 전체에서 어떤 의미를 가지는지 구체적으로 설명해주세요.

---

## 3. 오행 분석

### 오행 분포
- 목(木): {element_count.get('목(木)', 0)}개
- 화(火): {element_count.get('화(火)', 0)}개
- 토(土): {element_count.get('토(土)', 0)}개
- 금(金): {element_count.get('금(金)', 0)}개
- 수(水): {element_count.get('수(水)', 0)}개

### 강약 판별
- 일간 {ilgan}의 강약을 판단하고 그 이유를 설명해주세요
- 신강/신약 여부
- 월령 득령 여부

### 용신 분석
- 이 사주의 용신은 무엇인가?
- 희신, 기신은 무엇인가?
- 용신을 어떻게 활용해야 하는가?

### 조후 및 균형
- 계절 및 기후 조화 (조후)
- 부족한 오행과 과다한 오행
- 보완 방법 (색상, 방향, 직업 등)

---

## 4. 십신 및 육친 관계

### 십신 분포
{format_sipsin_distribution(result)}

### 십신 해석
각 십신(비견, 겁재, 식신, 상관, 편재, 정재, 편관, 정관, 편인, 정인)이 이 사주에서 어떤 의미를 가지는지 설명해주세요.

### 육친 관계
- **부모**: 부모와의 관계, 효도운, 유산 등
- **형제자매**: 형제와의 인연 및 협력 가능성
- **배우자**: 배우자 복, 결혼 시기, 배우자 성향
- **자녀**: 자녀 복, 양육 스타일

---

## 5. 성격 및 기질 분석

### 외향성 vs 내향성
- 외향적인가 내향적인가?
- 사교성 정도
- 에너지 방향 (밖으로/안으로)

### 이성 vs 감성
- 논리적인가 감성적인가?
- 판단 기준 (머리/가슴)

### 주요 기질
- 주도성, 리더십
- 분석력, 사고력
- 감수성, 공감력
- 추진력, 실행력
- 인내심, 끈기

### 대인관계 스타일
- 사람들과의 관계 형성 방식
- 신뢰 구축 방법
- 갈등 해결 스타일

---

## 6. {current_year}년 (올해) 운세

### 연간 전체 흐름
{current_year}년 전반적인 운세와 주의할 점

### 월별 세부 운세
**1월**: ...
**2월**: ...
**3월**: ...
**4월**: ...
**5월**: ...
**6월**: ...
**7월**: ...
**8월**: ...
**9월**: ...
**10월**: ...
**11월**: ...
**12월**: ...

각 달별로:
- 운세 키워드 (상승/하강/안정 등)
- 주요 이벤트 가능성
- 주의할 점
- 추천 행동

---

## 7. 대운 및 세운 흐름

### 현재 대운
{format_current_daeun(result)}

### 10년 대운 정리
{format_daeun_table(result)}

### 최근 5년 세운 분석
- {current_year-2}년: ...
- {current_year-1}년: ...
- {current_year}년 (현재): ...
- {current_year+1}년: ...
- {current_year+2}년: ...

### 인생 흐름 요약
- 20대: ...
- 30대: ...
- 40대: ...
- 50대 이후: ...

---

## 8. 진로 / 재물 / 건강

### 진로 및 적성
**적성 직업 분야 (우선순위)**
1. [직업군] - 이유: ...
2. [직업군] - 이유: ...
3. [직업군] - 이유: ...

**구체적 직업 예시:**
- ...

**경력 개발 조언:**
- ...

### 재물운
- 재물 형성 스타일 (월급/사업/투자)
- 돈 버는 시기와 방법
- 재테크 추천 방식
- 주의할 투자 시기

### 건강
- 타고난 건강 상태
- 주의해야 할 신체 부위
- 연령대별 건강 주의점
- 건강 관리 방법

---

## 9. 귀인과 살

### 귀인 (吉神)
{format_gwiin_list(result)}

**영향:**
각 귀인이 인생에 미치는 긍정적 영향을 구체적으로 설명해주세요.

### 살 (凶殺)
{format_sal_list(result)}

**영향:**
각 살이 인생에 미치는 영향과 극복 방법을 설명해주세요.

---

## 10. 한 줄 총평 및 핵심 키워드

### 총평
이 사람을 한 문장으로 요약하면: "..."

### 핵심 키워드 (5개)
1. [키워드1]
2. [키워드2]
3. [키워드3]
4. [키워드4]
5. [키워드5]

### 인생 조언
인생을 살아가면서 가장 중요하게 여겨야 할 3가지:
1. ...
2. ...
3. ...

---

{student_section}

---

## 풀이 가이드라인
- 한국어로 정중하고 이해하기 쉽게 작성
- 전문 용어는 쉬운 설명 추가
- 긍정적이면서도 현실적인 조언
- 구체적인 예시와 시기 언급
- 각 섹션 충실히 작성 (생략 금지)
"""
    
    return prompt


def get_saju_interpretation(saju_result: dict, gender: str = '남', is_student: bool = False) -> str:
    """ChatGPT를 이용한 사주 풀이"""
    
    prompt = get_comprehensive_saju_interpretation(saju_result, gender, is_student)
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 30년 경력의 전문 사주명리학자입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    
    except openai.AuthenticationError:
        return "❌ OpenAI API 키가 유효하지 않습니다. Streamlit Secrets에서 올바른 API 키를 설정해주세요."
    except openai.RateLimitError:
        return "❌ API 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
    except Exception as e:
        return f"❌ 풀이 중 오류가 발생했습니다: {str(e)}"


# 메인 UI
st.markdown("### 📝 기본 정보 입력")

col1, col2 = st.columns([1, 2])

with col1:
    gender = st.selectbox("👤 성별", ["남", "여"])

with col2:
    is_student = st.checkbox("🎓 학생", value=False)

# 양력/음력 선택
calendar_type = st.radio(
    "📅 생년월일 종류",
    options=["양력", "음력"],
    horizontal=True
)

# 날짜 입력
col_date1, col_date2, col_date3 = st.columns(3)

with col_date1:
    birth_year = st.number_input(
        "년(年)",
        min_value=1900,
        max_value=2100,
        value=1990,
        step=1
    )

with col_date2:
    birth_month = st.number_input(
        "월(月)",
        min_value=1,
        max_value=12,
        value=1,
        step=1
    )

with col_date3:
    birth_day = st.number_input(
        "일(日)",
        min_value=1,
        max_value=31,
        value=1,
        step=1
    )

# 윤달 여부 (음력인 경우에만)
is_leap_month = False
if calendar_type == "음력":
    is_leap_month = st.checkbox("윤달 여부")

# 시간 입력 (1분 단위)
st.markdown("**⏰ 출생 시간**")
col_time1, col_time2 = st.columns(2)

with col_time1:
    birth_hour = st.number_input(
        "시(時)",
        min_value=0,
        max_value=23,
        value=12,
        step=1
    )

with col_time2:
    birth_minute = st.number_input(
        "분(分)",
        min_value=0,
        max_value=59,
        value=0,
        step=1
    )

birth_time_display = f"{birth_hour:02d}:{birth_minute:02d}"
st.caption(f"입력된 시간: {birth_time_display}")

# 계산 버튼
if st.button("🔮 사주팔자 계산하기", type="primary", use_container_width=True):
    # 양력/음력 변환
    if calendar_type == "음력":
        try:
            solar_date = lunar_to_solar(birth_year, birth_month, birth_day, is_leap_month)
            st.info(f"📌 변환된 양력: {solar_date['year']}년 {solar_date['month']}월 {solar_date['day']}일")
            birth_datetime = datetime(solar_date['year'], solar_date['month'], solar_date['day'], birth_hour, birth_minute)
            st.session_state['is_solar'] = False
        except Exception as e:
            st.error(f"❌ 음력 변환 중 오류가 발생했습니다: {str(e)}")
            st.stop()
    else:
        birth_datetime = datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute)
        st.session_state['is_solar'] = True
    
    st.session_state['saju_calculated'] = True
    st.session_state['birth_datetime'] = birth_datetime
    st.session_state['gender'] = gender
    st.session_state['is_student'] = is_student
    st.session_state['calendar_type'] = calendar_type

# 사주 계산 결과 표시
if st.session_state.get('saju_calculated', False):
    birth_datetime = st.session_state['birth_datetime']
    gender = st.session_state.get('gender', '남')
    is_student = st.session_state.get('is_student', False)
    
    with st.spinner("사주팔자를 계산하는 중..."):
        result = calculate_four_pillars(birth_datetime, gender)
    
    calendar_label = "양력" if st.session_state.get('is_solar', True) else "음력→양력"
    st.success(f"✅ {result['birth_date']} ({calendar_label}) 출생자의 사주팔자")
    
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
            st.metric(label=title, value=pillar)
            st.caption(f"한자: {hanja}")
    
    # 오행 분석
    st.subheader("🌟 오행 분석 (五行)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**천간(天干) 오행:**")
        for i, (stem, element) in enumerate(zip(['연간', '월간', '일간', '시간'], result['stems_elements'])):
            st.write(f"- {stem}: {element}")
    
    with col2:
        st.write("**지지(地支) 오행:**")
        for i, (branch, element) in enumerate(zip(['연지', '월지', '일지', '시지'], result['branches_elements'])):
            st.write(f"- {branch}: {element}")
    
    # 오행 개수 통계
    element_count = get_element_count(result)
    st.write("**오행 개수:**")
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
        if st.button("🤖 AI 사주풀이 보기", type="primary", use_container_width=True):
            with st.spinner("AI가 사주를 풀이하는 중... (약 30-60초 소요)"):
                # OpenAI 클라이언트 초기화
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                
                interpretation = get_saju_interpretation(result, gender, is_student)
                
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
            
            # 추가 질문 기능
            st.markdown("---")
            st.markdown("### 💬 추가로 궁금한 점이 있으신가요?")
            
            follow_up_question = st.text_area(
                "궁금한 점을 자유롭게 질문해주세요",
                placeholder="예: 이직 시기는 언제가 좋을까요?\n예: 결혼운은 어떤가요?\n예: 건강상 주의할 점은?",
                height=100,
                key="follow_up_question"
            )
            
            if st.button("🔮 추가 질문하기"):
                if follow_up_question.strip():
                    with st.spinner("답변 생성 중..."):
                        # 사주 정보 요약
                        original_saju_info = f"""
생년월일시: {result['birth_date']}
사주팔자: 
- 연주: {result['year_pillar']} ({result['year_hanja']})
- 월주: {result['month_pillar']} ({result['month_hanja']})
- 일주: {result['day_pillar']} ({result['day_hanja']})
- 시주: {result['hour_pillar']} ({result['hour_hanja']})

오행: {', '.join(result['stems_elements'] + result['branches_elements'])}
"""
                        
                        follow_up_prompt = f"""
당신은 30년 경력의 전문 사주명리학자입니다.

## 기존 사주 정보
{original_saju_info}

## 사용자 추가 질문
{follow_up_question}

위 사주 정보를 바탕으로 사용자의 질문에 구체적이고 깊이 있게 답변해주세요.
- 해당 질문과 관련된 십신, 신살, 대운, 세운을 중심으로 설명
- 구체적인 시기나 방법 제시
- 긍정적이면서도 현실적인 조언
"""
                        
                        openai.api_key = st.secrets["OPENAI_API_KEY"]
                        follow_up_response = openai.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "당신은 30년 경력의 전문 사주명리학자입니다."},
                                {"role": "user", "content": follow_up_prompt}
                            ],
                            temperature=0.7,
                            max_tokens=2000
                        )
                        
                        st.markdown("### 📖 추가 답변")
                        st.markdown(follow_up_response.choices[0].message.content)
                else:
                    st.warning("질문을 입력해주세요.")

# 푸터
st.divider()
st.caption("💡 본 서비스는 참고용이며, 전문가의 상담을 대체할 수 없습니다.")
st.caption("🤖 AI 풀이는 OpenAI GPT-4o-mini를 사용하며, API 비용이 발생할 수 있습니다.")
