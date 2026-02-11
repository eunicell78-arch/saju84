"""
사주팔자 만세력 계산기 with OpenAI ChatGPT
Saju (Four Pillars) Calculator with AI Interpretation
"""
import streamlit as st
from datetime import datetime, time
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


def get_saju_interpretation(saju_result: dict) -> str:
    """ChatGPT를 이용한 사주 풀이"""
    
    # 오행 개수
    element_count = get_element_count(saju_result)
    element_str = ", ".join([f"{k}: {v}개" for k, v in element_count.items()])
    
    # 십신 정보
    sipsin_str = ""
    if 'sipsin' in saju_result:
        sipsin_str = f"""
## 십신 분포
- 년간: {saju_result['sipsin']['year_stem']}
- 월간: {saju_result['sipsin']['month_stem']}
- 일간: {saju_result['sipsin']['day_stem']}
- 시간: {saju_result['sipsin']['hour_stem']}
"""
    
    # 12운성 정보
    unsung_str = ""
    if 'unsung' in saju_result:
        unsung_str = f"""
## 12운성
- 년지: {saju_result['unsung']['year']}
- 월지: {saju_result['unsung']['month']}
- 일지: {saju_result['unsung']['day']}
- 시지: {saju_result['unsung']['hour']}
"""
    
    # 신살 정보
    sinsal_str = ""
    if 'sinsal' in saju_result:
        sinsal_list = []
        if saju_result['sinsal']['cheonul']:
            sinsal_list.append(f"천을귀인: {', '.join(saju_result['sinsal']['cheonul'])}")
        if saju_result['sinsal']['yeokma']:
            sinsal_list.append(f"역마살: {', '.join(saju_result['sinsal']['yeokma'])}")
        if saju_result['sinsal']['dohwa']:
            sinsal_list.append(f"도화살: {', '.join(saju_result['sinsal']['dohwa'])}")
        if saju_result['sinsal']['gongmang']:
            sinsal_list.append(f"공망: {', '.join(saju_result['sinsal']['gongmang'])}")
        
        if sinsal_list:
            sinsal_str = "## 신살\n" + "\n".join([f"- {s}" for s in sinsal_list])
    
    # 형충회합 정보
    hch_str = ""
    if 'hyungchunghap' in saju_result:
        hch = saju_result['hyungchunghap']
        hch_list = []
        if hch['chung']:
            hch_list.append(f"충(沖): {', '.join(hch['chung'])}")
        if hch['yukhap']:
            hch_list.append(f"육합(六合): {', '.join(hch['yukhap'])}")
        if hch['samhap']:
            hch_list.append(f"삼합(三合): {', '.join(hch['samhap'])}")
        if hch['hyung']:
            hch_list.append(f"형(刑): {', '.join(hch['hyung'])}")
        
        if hch_list:
            hch_str = "## 형충회합\n" + "\n".join([f"- {h}" for h in hch_list])
    
    # 대운 정보
    daeun_str = ""
    if 'daeun' in saju_result:
        daeun_str = f"""
## 대운
- 방향: {saju_result['daeun']['direction']}
- 시작: {saju_result['daeun']['start_age']}세
- 현재 대운 (예시): {saju_result['daeun']['list'][0]['간지']} ({saju_result['daeun']['list'][0]['나이']})
"""
    
    # 세운 정보
    seun_str = ""
    if 'seun' in saju_result:
        current = saju_result['seun']['current']
        seun_str = f"""
## 세운
- 현재: {current['년도']}년 {current['간지']} ({current['나이']}세)
"""
    
    prompt = f"""
당신은 30년 경력의 전문 사주명리학자입니다. 
다음 사주팔자를 깊이있고 전문적으로 풀이해주세요.

## 생년월일시
{saju_result['birth_date']}

## 사주팔자
- 연주(年柱): {saju_result['year_pillar']} ({saju_result['year_hanja']})
- 월주(月柱): {saju_result['month_pillar']} ({saju_result['month_hanja']})
- 일주(日柱): {saju_result['day_pillar']} ({saju_result['day_hanja']})
- 시주(時柱): {saju_result['hour_pillar']} ({saju_result['hour_hanja']})

## 오행 분석
- 천간: {', '.join(saju_result['stems_elements'])}
- 지지: {', '.join(saju_result['branches_elements'])}
- 오행 개수: {element_str}

## 음양 분석
- 천간: {', '.join(saju_result['stems_yin_yang'])}
- 지지: {', '.join(saju_result['branches_yin_yang'])}
{sipsin_str}{unsung_str}{sinsal_str}{hch_str}{daeun_str}{seun_str}

## 풀이 요청사항
다음 항목들을 구조화된 형식으로 풀이해주세요:

### 1. 사주 전체 구조 분석
일간의 강약과 사주 구조의 특징을 분석해주세요.

### 2. 십신으로 본 성격과 적성
십신 배치를 바탕으로 성격, 재능, 적성을 설명해주세요.

### 3. 오행 균형과 용신
오행의 강약과 조화를 분석하고, 필요한 용신을 제시해주세요.

### 4. 신살의 길흉
주요 신살의 의미와 영향을 설명해주세요.

### 5. 직업운과 재물운
적합한 직업 분야와 재물 운세를 분석해주세요.

### 6. 대운과 세운
현재 대운과 세운의 흐름을 해석해주세요.

### 7. 건강과 주의사항
건강 관련 주의사항과 개선 방향을 제시해주세요.

한국어로 정중하고 이해하기 쉽게 설명해주세요. 각 섹션은 제목(###)을 포함하여 구분해주세요.
"""
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 전문 사주명리학자입니다. 사주팔자를 깊이있고 정확하게 풀이합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    except openai.AuthenticationError:
        return "❌ OpenAI API 키가 유효하지 않습니다. Streamlit Secrets에서 올바른 API 키를 설정해주세요."
    except openai.RateLimitError:
        return "❌ API 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
    except Exception as e:
        return f"❌ 풀이 중 오류가 발생했습니다: {str(e)}"


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
    
    # 음력 선택 시에만 윤달 옵션 표시
    is_leap_month = False
    if calendar_type == "음력":
        if not LUNAR_CALENDAR_AVAILABLE:
            st.error("⚠️ 음력 변환 기능을 사용하려면 `korean-lunar-calendar` 라이브러리가 필요합니다.")
            st.stop()
        
        is_leap_month = st.checkbox(
            "윤달",
            value=False,
            help="해당 월이 윤달인 경우 체크하세요."
        )
    
    birth_date = st.date_input(
        f"생년월일 ({calendar_type})",
        value=datetime(1990, 1, 1),
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2100, 12, 31)
    )
    
    birth_time = st.time_input(
        "출생 시간",
        value=time(12, 0)
    )
    
    gender = st.radio(
        "성별",
        options=['남', '여'],
        horizontal=True
    )
    
    # datetime 객체 생성 (일단 입력된 날짜로 생성, 음력인 경우 아래에서 변환)
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day
    birth_hour = birth_time.hour
    birth_minute = birth_time.minute
    
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
        
        st.session_state['saju_calculated'] = True
        st.session_state['birth_datetime'] = birth_datetime
        st.session_state['gender'] = gender

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
    
    with st.spinner("사주팔자를 계산하는 중..."):
        result = calculate_four_pillars(birth_datetime, gender)
    
    st.success(f"✅ {result['birth_date']} 출생자의 사주팔자")
    
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
        if st.button("🔮 AI 사주풀이 보기", type="primary", use_container_width=True):
            with st.spinner("AI가 사주를 풀이하는 중... (약 10-20초 소요)"):
                # OpenAI 클라이언트 초기화
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                
                interpretation = get_saju_interpretation(result)
                
                st.session_state['interpretation'] = interpretation
        
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

# 푸터
st.divider()
st.caption("💡 본 서비스는 참고용이며, 전문가의 상담을 대체할 수 없습니다.")
st.caption("🤖 AI 풀이는 OpenAI GPT-4를 사용하며, API 비용이 발생할 수 있습니다.")
